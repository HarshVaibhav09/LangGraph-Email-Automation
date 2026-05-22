from colorama import Fore, Style
from .agents import Agents
from .tools.GmailTools import GmailToolsClass
from .state import GraphState, Email


class Nodes:
    def __init__(self):
        self.agents = Agents()
        self.gmail_tools = GmailToolsClass()

    def load_new_emails(self, state: GraphState) -> GraphState:
        """Loads new emails from Gmail and updates the state."""
        print(Fore.YELLOW + "Loading new emails...\n" + Style.RESET_ALL)
        recent_emails = self.gmail_tools.fetch_unanswered_emails()
        emails = [Email(**email) for email in recent_emails]
        print(Fore.CYAN + f"Found {len(emails)} new email(s) to process" + Style.RESET_ALL)
        return {"emails": emails}

    def check_new_emails(self, state: GraphState) -> str:
        """Checks if there are new emails to process."""
        if len(state['emails']) == 0:
            print(Fore.RED + "No new emails" + Style.RESET_ALL)
            return "empty"
        else:
            print(Fore.GREEN + "New emails to process" + Style.RESET_ALL)
            return "process"
        
    def is_email_inbox_empty(self, state: GraphState) -> GraphState:
        return state

    def categorize_email(self, state: GraphState) -> GraphState:
        """Categorizes the current email using the categorize_email agent."""
        print(Fore.YELLOW + "Checking email category...\n" + Style.RESET_ALL)
        
        # Get the last email
        current_email = state["emails"][-1]
        
        # Debug: Show email details
        print(Fore.CYAN + f"From: {current_email.sender}" + Style.RESET_ALL)
        print(Fore.CYAN + f"Subject: {current_email.subject}" + Style.RESET_ALL)
        print(Fore.CYAN + f"Body preview: {current_email.body[:100]}..." + Style.RESET_ALL if len(current_email.body) > 100 else Fore.CYAN + f"Body: {current_email.body}" + Style.RESET_ALL)
        print()
        
        result = self.agents.categorize_email.invoke({"email": current_email.body})
        print(Fore.MAGENTA + f"Email category: {result.category.value}" + Style.RESET_ALL)
        
        return {
            "email_category": result.category.value,
            "current_email": current_email
        }

    def route_email_based_on_category(self, state: GraphState) -> str:
        """Routes the email based on its category."""
        print(Fore.YELLOW + "Routing email based on category...\n" + Style.RESET_ALL)
        category = state["email_category"]
        if category == "product_enquiry":
            return "product related"
        elif category == "unrelated":
            return "unrelated"
        else:
            return "not product related"

    def construct_rag_queries(self, state: GraphState) -> GraphState:
        """Constructs RAG queries based on the email content."""
        print(Fore.YELLOW + "Designing RAG query...\n" + Style.RESET_ALL)
        email_content = state["current_email"].body
        query_result = self.agents.design_rag_queries.invoke({"email": email_content})
        
        return {"rag_queries": query_result.queries}

    def retrieve_from_rag(self, state: GraphState) -> GraphState:
        """Retrieves information from internal knowledge based on RAG questions."""
        print(Fore.YELLOW + "Retrieving information from internal knowledge...\n" + Style.RESET_ALL)
        final_answer = ""
        for query in state["rag_queries"]:
            rag_result = self.agents.generate_rag_answer.invoke(query)
            final_answer += query + "\n" + rag_result + "\n\n"
        
        return {"retrieved_documents": final_answer}

    def write_draft_email(self, state: GraphState) -> GraphState:
        """Writes a draft email based on the current email and retrieved information."""
        print(Fore.YELLOW + "Writing draft email...\n" + Style.RESET_ALL)
        
        # Format input to the writer agent
        inputs = (
            f'# **EMAIL CATEGORY:** {state["email_category"]}\n\n'
            f'# **EMAIL CONTENT:**\n{state["current_email"].body}\n\n'
            f'# **INFORMATION:**\n{state["retrieved_documents"]}' # Empty for feedback or complaint
        )
        
        # Get messages history for current email
        writer_messages = state.get('writer_messages', [])
        
        # Write email
        draft_result = self.agents.email_writer.invoke({
            "email_information": inputs,
            "history": writer_messages
        })
        email = draft_result.email
        trials = state.get('trials', 0) + 1

        # Append writer's draft to the message list
        writer_messages.append(f"**Draft {trials}:**\n{email}")

        return {
            "generated_email": email, 
            "trials": trials,
            "writer_messages": writer_messages
        }

    def verify_generated_email(self, state: GraphState) -> GraphState:
        """Verifies the generated email using the proofreader agent."""
        print(Fore.YELLOW + "Verifying generated email...\n" + Style.RESET_ALL)
        review = self.agents.email_proofreader.invoke({
            "initial_email": state["current_email"].body,
            "generated_email": state["generated_email"],
        })

        writer_messages = state.get('writer_messages', [])
        writer_messages.append(f"**Proofreader Feedback:**\n{review.feedback}")

        return {
            "sendable": review.send,
            "writer_messages": writer_messages
        }

    def must_rewrite(self, state: GraphState) -> str:
        """Determines if the email needs to be rewritten based on the review and trial count."""
        email_sendable = state["sendable"]
        if email_sendable:
            print(Fore.GREEN + "Email is good, ready to be sent!!!" + Style.RESET_ALL)
            state["emails"].pop()
            state["writer_messages"] = []
            return "send"
        elif state["trials"] >= 3:
            print(Fore.RED + "Email is not good, we reached max trials must stop!!!" + Style.RESET_ALL)
            state["emails"].pop()
            state["writer_messages"] = []
            return "stop"
        else:
            print(Fore.RED + "Email is not good, must rewrite it..." + Style.RESET_ALL)
            return "rewrite"

    def create_draft_response(self, state: GraphState) -> GraphState:
        """Creates a draft response in Gmail."""
        print(Fore.YELLOW + "Creating draft email...\n" + Style.RESET_ALL)
        try:
            draft = self.gmail_tools.create_draft_reply(state["current_email"], state["generated_email"])
            if draft:
                print(Fore.GREEN + "✓ Draft created successfully" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"✗ Error creating draft: {e}" + Style.RESET_ALL)
        
        return {"retrieved_documents": "", "trials": 0}

    def send_email_response(self, state: GraphState) -> GraphState:
        """Sends the email response directly using Gmail."""
        print(Fore.YELLOW + "Sending email...\n" + Style.RESET_ALL)
        try:
            result = self.gmail_tools.send_reply(state["current_email"], state["generated_email"])
            if result:
                print(Fore.GREEN + "✓ Email sent successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "✗ Failed to send email" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"✗ Error sending email: {e}" + Style.RESET_ALL)
        
        return {"retrieved_documents": "", "trials": 0}
    
    def skip_unrelated_email(self, state: GraphState) -> GraphState:
        """Handle unrelated email by sending a polite response instead of skipping."""
        print(Fore.YELLOW + "Processing unrelated email (sending polite response)...\n" + Style.RESET_ALL)
        
        current_email = state["current_email"]
        
        # Generate a polite response for unrelated emails
        unrelated_response = f"""Dear Customer,

Thank you for contacting us. We appreciate you reaching out.

We've received your message, but it appears to be outside the scope of our customer support services. If you have any questions about our products, services, or need assistance, please feel free to reach out to us with more details.

We're here to help and would be happy to assist you with any inquiries related to our services.

Best regards,
The Agentia Team"""
        
        # Send the response
        try:
            self.gmail_tools.send_reply(current_email, unrelated_response)
            print(Fore.GREEN + "✓ Polite response sent for unrelated email" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"✗ Error sending response: {e}" + Style.RESET_ALL)
        
        # Remove from emails list
        state["emails"].pop()
        return state
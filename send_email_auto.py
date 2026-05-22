"""
Auto-send a test email without prompts.
This will automatically send a test email to your MY_EMAIL address.
"""
from colorama import Fore, Style, init
from dotenv import load_dotenv
import os
from datetime import datetime

# Initialize colorama for Windows
init(autoreset=True)

# Load environment variables
load_dotenv()

def send_test_email_auto():
    """Automatically send a test email."""
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)
    print(Fore.GREEN + "  Auto Email Sender - Test Email" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL + "\n")
    
    # Check prerequisites
    if not os.path.exists('token.json'):
        print(Fore.RED + "✗ token.json not found. Please authenticate first." + Style.RESET_ALL)
        return False
    
    my_email = os.getenv('MY_EMAIL', '')
    if not my_email:
        print(Fore.RED + "✗ MY_EMAIL not set in .env file" + Style.RESET_ALL)
        return False
    
    print(Fore.GREEN + f"✓ Sending test email to: {my_email}" + Style.RESET_ALL)
    
    # Import and initialize
    try:
        from src.tools.GmailTools import GmailToolsClass
        gmail_tools = GmailToolsClass()
        print(Fore.GREEN + "✓ Gmail service initialized" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"✗ Error: {e}" + Style.RESET_ALL)
        return False
    
    # Prepare email
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"✅ Test Email - Email Automation System - {timestamp}"
    body = f"""Hello!

🎉 SUCCESS! Your Email Automation System is working!

This is a test email sent automatically to verify the email sending functionality.

📧 Email Details:
- Sent at: {timestamp}
- System: LangGraph Email Automation
- Status: ✓ Operational and Ready

✨ Features Available:
- Send standalone emails
- Reply to customer emails
- Automated email processing
- RAG-powered responses

The email sending feature has been successfully implemented and tested!

Best regards,
Your Email Automation System
"""
    
    print(Fore.YELLOW + "\n📧 Email Details:" + Style.RESET_ALL)
    print(f"  To: {my_email}")
    print(f"  Subject: {subject}")
    print()
    
    # Send email
    print(Fore.YELLOW + "Sending email..." + Style.RESET_ALL)
    try:
        result = gmail_tools.send_email(my_email, subject, body)
        
        if result:
            print(Fore.GREEN + "\n✅ Email sent successfully!" + Style.RESET_ALL)
            print(Fore.CYAN + f"Message ID: {result.get('id', 'N/A')}" + Style.RESET_ALL)
            print(Fore.CYAN + f"Thread ID: {result.get('threadId', 'N/A')}" + Style.RESET_ALL)
            print(Fore.GREEN + "\n✓ Check your inbox for the test email!" + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + "\n✗ Failed to send email" + Style.RESET_ALL)
            return False
            
    except Exception as e:
        print(Fore.RED + f"\n✗ Error: {e}" + Style.RESET_ALL)
        return False

if __name__ == "__main__":
    try:
        send_test_email_auto()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nOperation cancelled" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nError: {e}" + Style.RESET_ALL)


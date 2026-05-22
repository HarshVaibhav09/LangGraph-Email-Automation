"""
Simple script to send a test email using Gmail API.
"""
from colorama import Fore, Style
from dotenv import load_dotenv
from src.tools.GmailTools import GmailToolsClass

# Load environment variables
load_dotenv()

def send_test_email():
    """Send a test email to a specified recipient."""
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "Gmail Email Sender" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    
    # Get email details from user
    recipient = input(Fore.YELLOW + "Enter recipient email address: " + Style.RESET_ALL)
    subject = input(Fore.YELLOW + "Enter email subject: " + Style.RESET_ALL)
    
    print(Fore.YELLOW + "Enter email body (press Enter twice to finish):" + Style.RESET_ALL)
    body_lines = []
    while True:
        line = input()
        if line == "" and body_lines and body_lines[-1] == "":
            break
        body_lines.append(line)
    
    body_text = "\n".join(body_lines).strip()
    
    if not recipient or not subject or not body_text:
        print(Fore.RED + "Error: All fields (recipient, subject, body) are required!" + Style.RESET_ALL)
        return
    
    # Initialize Gmail tools
    print(Fore.YELLOW + "\nInitializing Gmail service..." + Style.RESET_ALL)
    gmail_tools = GmailToolsClass()
    
    # Send the email
    print(Fore.YELLOW + "Sending email..." + Style.RESET_ALL)
    result = gmail_tools.send_email(recipient, subject, body_text)
    
    if result:
        print(Fore.GREEN + "\n✓ Email sent successfully!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n✗ Failed to send email. Please check the error above." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        send_test_email()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nOperation cancelled by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nAn error occurred: {e}" + Style.RESET_ALL)


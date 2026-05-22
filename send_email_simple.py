"""
Simple script to send an email using command-line arguments.
Usage: python send_email_simple.py recipient@example.com "Subject" "Email body text"
"""
import sys
from colorama import Fore, Style
from dotenv import load_dotenv
from src.tools.GmailTools import GmailToolsClass

# Load environment variables
load_dotenv()

def send_email(recipient, subject, body):
    """Send an email to the specified recipient."""
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "Sending Email..." + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.YELLOW + f"To: {recipient}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Subject: {subject}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Body: {body[:50]}..." + Style.RESET_ALL if len(body) > 50 else f"Body: {body}" + Style.RESET_ALL)
    print()
    
    # Initialize Gmail tools
    print(Fore.YELLOW + "Initializing Gmail service..." + Style.RESET_ALL)
    gmail_tools = GmailToolsClass()
    
    # Send the email
    print(Fore.YELLOW + "Sending email..." + Style.RESET_ALL)
    result = gmail_tools.send_email(recipient, subject, body)
    
    if result:
        print(Fore.GREEN + "\n✓ Email sent successfully!" + Style.RESET_ALL)
        print(Fore.CYAN + f"Message ID: {result.get('id', 'N/A')}" + Style.RESET_ALL)
        return True
    else:
        print(Fore.RED + "\n✗ Failed to send email." + Style.RESET_ALL)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(Fore.RED + "Usage: python send_email_simple.py <recipient> <subject> <body>" + Style.RESET_ALL)
        print(Fore.YELLOW + "Example: python send_email_simple.py user@example.com \"Test Subject\" \"This is a test email\"" + Style.RESET_ALL)
        sys.exit(1)
    
    recipient = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    
    try:
        send_email(recipient, subject, body)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nOperation cancelled by user." + Style.RESET_ALL)
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"\nAn error occurred: {e}" + Style.RESET_ALL)
        sys.exit(1)


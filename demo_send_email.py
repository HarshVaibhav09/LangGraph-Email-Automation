"""
Demo script to test email sending functionality.
This will send a test email to demonstrate the email sending feature.
"""
from colorama import Fore, Style, init
from dotenv import load_dotenv
import os
from datetime import datetime

# Initialize colorama for Windows
init(autoreset=True)

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header."""
    print("\n" + Fore.CYAN + "=" * 60 + Style.RESET_ALL)
    print(Fore.GREEN + f"  {text}" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL + "\n")

def print_success(text):
    """Print success message."""
    print(Fore.GREEN + f"✓ {text}" + Style.RESET_ALL)

def print_error(text):
    """Print error message."""
    print(Fore.RED + f"✗ {text}" + Style.RESET_ALL)

def print_info(text):
    """Print info message."""
    print(Fore.YELLOW + f"ℹ {text}" + Style.RESET_ALL)

def demo_send_email():
    """Demonstrate email sending functionality."""
    print_header("Email Sending Demo")
    
    # Check for required files
    print_info("Checking prerequisites...")
    
    if not os.path.exists('token.json'):
        print_error("token.json not found. You need to authenticate with Gmail first.")
        print_info("Run the main.py script once to authenticate, or ensure credentials.json exists.")
        return False
    
    print_success("token.json found")
    
    # Get email from environment or use a default test
    my_email = os.getenv('MY_EMAIL', '')
    if not my_email:
        print_error("MY_EMAIL not set in .env file")
        print_info("Please set MY_EMAIL in your .env file")
        return False
    
    print_success(f"MY_EMAIL configured: {my_email}")
    
    # Import Gmail tools
    try:
        from src.tools.GmailTools import GmailToolsClass
        print_success("GmailTools imported successfully")
    except Exception as e:
        print_error(f"Failed to import GmailTools: {e}")
        return False
    
    # Initialize Gmail service
    print_info("Initializing Gmail service...")
    try:
        gmail_tools = GmailToolsClass()
        print_success("Gmail service initialized")
    except Exception as e:
        print_error(f"Failed to initialize Gmail service: {e}")
        print_info("Make sure you have credentials.json and have authenticated")
        return False
    
    # Prepare test email
    recipient = my_email  # Send to yourself for testing
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Test Email - Email Automation System - {timestamp}"
    body = f"""Hello!

This is a test email from your Email Automation System.

The email sending functionality is working correctly!

Details:
- Sent at: {timestamp}
- System: LangGraph Email Automation
- Status: ✓ Operational

This email was sent using the Gmail API integration.

Best regards,
Your Email Automation System
"""
    
    # Display email details
    print_header("Email Details")
    print(f"{Fore.CYAN}To:{Style.RESET_ALL} {recipient}")
    print(f"{Fore.CYAN}Subject:{Style.RESET_ALL} {subject}")
    print(f"{Fore.CYAN}Body:{Style.RESET_ALL}")
    print(Fore.WHITE + body + Style.RESET_ALL)
    print()
    
    # Ask for confirmation
    print_info("Ready to send test email...")
    response = input(f"{Fore.YELLOW}Send email to {recipient}? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if response != 'y':
        print_info("Email sending cancelled by user")
        return False
    
    # Send the email
    print_header("Sending Email")
    print_info("Sending email via Gmail API...")
    
    try:
        result = gmail_tools.send_email(recipient, subject, body)
        
        if result:
            print_success("Email sent successfully!")
            print(f"{Fore.CYAN}Message ID:{Style.RESET_ALL} {result.get('id', 'N/A')}")
            print(f"{Fore.CYAN}Thread ID:{Style.RESET_ALL} {result.get('threadId', 'N/A')}")
            print()
            print_success("Check your inbox for the test email!")
            return True
        else:
            print_error("Failed to send email (no result returned)")
            return False
            
    except Exception as e:
        print_error(f"Error sending email: {e}")
        import traceback
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        return False

if __name__ == "__main__":
    try:
        success = demo_send_email()
        if success:
            print_header("Demo Completed Successfully")
        else:
            print_header("Demo Failed")
            print_info("Please check the errors above and try again")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation cancelled by user{Style.RESET_ALL}")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)


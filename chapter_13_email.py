#!/usr/bin/env python3
"""
Chapter 13: Sending Emails with Python
This script demonstrates sending emails using smtplib and Gmail.
SMTP (Simple Mail Transfer Protocol) is the standard for email transmission.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # TLS port

def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Sends an email using Gmail's SMTP server.
    
    Args:
        sender_email (str): Your Gmail address
        sender_password (str): Your Gmail app password
        recipient_email (str): Recipient's email address
        subject (str): Email subject
        body (str): Email body content
    
    Returns:
        bool: True if successful, False otherwise
    
    How SMTP works:
    1. Connect to SMTP server
    2. Start TLS encryption
    3. Login with credentials
    4. Send email data
    5. Close connection
    """
    
    print("="*60)
    print("Sending Email")
    print("="*60)
    
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        
        # Attach body as plain text
        message.attach(MIMEText(body, 'plain'))
        
        print(f"[*] Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        # Enable debug output (optional)
        # server.set_debuglevel(1)
        
        print("[*] Starting TLS encryption...")
        server.starttls()  # Secure the connection
        
        print("[*] Logging in...")
        server.login(sender_email, sender_password)
        
        print("[*] Sending email...")
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        
        print("[+] Email sent successfully!")
        
        # Close connection
        server.quit()
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("[-] Authentication failed")
        print("[-] Make sure you're using an App Password, not your regular password")
        return False
    except smtplib.SMTPException as e:
        print(f"[-] SMTP error: {e}")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False


def main():
    """
    Main function for email sending demonstration.
    """
    
    print("\n" + "💧"*30)
    print("Chapter 13: The Peaceful Cascade - Email Quest")
    print("💧"*30 + "\n")
    
    print("[*] You rest by the cascade...")
    print("[*] Time to master email communication!\n")
    
    # Important instructions
    print("="*60)
    print("IMPORTANT: Gmail App Password Setup")
    print("="*60)
    print("\nTo use this script with Gmail, you need an App Password:")
    print("1. Go to your Google Account settings")
    print("2. Security > 2-Step Verification (must be enabled)")
    print("3. App passwords > Select 'Mail' and 'Other'")
    print("4. Generate password and use it here")
    print("\nNOTE: Google removed 'Less Secure Apps' option in 2022")
    print("      You MUST use App Passwords now")
    print("="*60 + "\n")
    
    # Get email configuration
    print("Email Configuration:")
    sender_email = input("Your Gmail address: ").strip()
    sender_password = input("Your App Password: ").strip()
    recipient_email = input("Recipient email: ").strip()
    
    # Email content
    subject = "Greetings from the Arrakis Quest!"
    
    body = """Dear Adventurer,

This email is sent from Chapter 13 of the Arrakis Quest.

You have successfully:
- Configured SMTP settings
- Authenticated with Gmail
- Sent an email using Python's smtplib

The journey continues through the cascade...

May your code be bug-free,
The Cascade Spirit
"""
    
    # Send the email
    print("\n")
    success = send_email(sender_email, sender_password, recipient_email, subject, body)
    
    if success:
        print("\n" + "="*60)
        print("Quest Complete!")
        print("="*60)
        print("[✓] Configured Gmail App Password")
        print("[✓] Connected to SMTP server")
        print("[✓] Sent email successfully")
        print("[*] Check your inbox!")
        print("="*60 + "\n")
    else:
        print("\n[-] Email sending failed")
        print("[-] Please check your credentials and try again")


if __name__ == "__main__":
    main()

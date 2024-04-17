import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Gmail SMTP port

    # Create a message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message
    msg.attach(MIMEText(message, 'plain'))

    # Start the SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Log in to the SMTP server
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Quit the SMTP server
    server.quit()

# Get email credentials from environment variables
sender_email = os.environ.get('SENDER_EMAIL')
sender_password = os.environ.get('SENDER_PASSWORD')

receiver_email = os.environ.get('RECEIVER_EMAIL')
subject = "Test Email"
message = "This is a test email sent from Python."

if sender_email and sender_password:
    send_email(sender_email, sender_password, receiver_email, subject, message)
    print("Email sent successfully")
else:
    print("Sender email or password not provided.")

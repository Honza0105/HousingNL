import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pararius
import kamernet

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


if __name__ == '__main__':
    # Run Pararius scraping
    pararius.scrape()

    # Run Kamernet notification logic
    kamernet.run(send_email)

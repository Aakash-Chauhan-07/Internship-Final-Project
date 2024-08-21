import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from load_attachment_address import load_attachment_address

def email(reciever, subject, body, attachment=False):
    # SMTP server configuration
    smtp_server = "smtp-mail.outlook.com"
    port = 587  # For STARTTLS
    sender_email = "chequekar@outlook.com"
    password = "Asdfg54321$"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = reciever
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach files if necessary
    if attachment:
        attachments = load_attachment_address()
        for file_path in attachments:
            with open(file_path, "rb") as attachment_file:
                part = MIMEApplication(attachment_file.read(), Name=os.path.basename(file_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, reciever, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def bulk_email(recievers: str, subject, body, attachment=False):
    # SMTP server configuration
    smtp_server = "smtp-mail.outlook.com"
    port = 587  # For STARTTLS
    sender_email = "chequekar@outlook.com"
    password = "Asdfg54321$"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create the email template
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach files if necessary
    if attachment:
        attachments = load_attachment_address()
        for file_path in attachments:
            with open(file_path, "rb") as attachment_file:
                part = MIMEApplication(attachment_file.read(), Name=os.path.basename(file_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)

    # Send the email to each recipient
    recipients = recievers.split(',')
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            for recipient in recipients:
                msg["To"] = recipient
                server.sendmail(sender_email, recipient, msg.as_string())
        print("Bulk email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
email("aakashchauhan9636@gmail.com", "Happy Exams", "Hope you are doing well and pass the exam.")

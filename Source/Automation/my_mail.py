import yagmail
from load_attachment_address import load_attachment_address

def email(reciever, subject, body, attachment = False):

    # Initialize the Yagmail client
    yag = yagmail.SMTP('aakinsta389@gmail.com', 'mvwx qslu tthd ygbl')

    # Define the recipient, subject, contents, and attachment
    recipient = reciever
    subject = subject
    body = body

    if attachment:
        attachment = list(load_attachment_address())

        # Send the email with the attachment
        yag.send(
            to=recipient,
            subject=subject,
            contents=body,
            attachments=attachment
        )
    else:
        # Send the email without the attachment
        yag.send(
            to=recipient,
            subject=subject,
            contents=body
        )

    print("Email sent successfully!")



def bulk_email(recievers: str, subject, body, attachment = False): # task comma seperated emails

    # Initialize the Yagmail client
    yag = yagmail.SMTP('aakinsta389@gmail.com', 'mvwx qslu tthd ygbl')

    # Define the recipient, subject, contents, and attachment
    recipients = recievers.split(',')
    subject = subject
    body = body

    if attachment:
        attachment = list(load_attachment_address())

        # Send the email with the attachment
        for i in recipients:
            yag.send(
                to=i,
                subject=subject,
                contents=body,
                attachments=attachment
            )
    else:
        # Send the email without the attachment
        for i in recipients:
            yag.send(
                to=i,
                subject=subject,
                contents=body
            )

    print("Email sent successfully!")



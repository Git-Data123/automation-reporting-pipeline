import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_email_with_attachment(
    smtp_server,
    smtp_port,
    sender_email,
    sender_password,
    recipient_email,
    subject,
    body,
    attachment_path,
):
    attachment_path = Path(attachment_path)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(body)

    with open(attachment_path, "rb") as file:
        file_data = file.read()
        file_name = attachment_path.name

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=file_name,
    )

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
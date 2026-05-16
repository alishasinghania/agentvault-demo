import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict

from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


send_email_tool = {
    "name": "send_email",
    "description": (
        "Send an internal email on behalf of the employee. Use this whenever the user "
        "asks you to send, draft and send, or email someone. You can determine the "
        "appropriate recipient, subject, and body from the conversation context."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "to": {
                "type": "string",
                "description": "Recipient email address",
            },
            "subject": {
                "type": "string",
                "description": "Email subject line",
            },
            "body": {
                "type": "string",
                "description": "Email body text",
            },
            "cc": {
                "type": "string",
                "description": "CC email addresses (optional, comma-separated)",
            },
        },
        "required": ["to", "subject", "body"],
    },
}


def execute_send_email(to: str, subject: str, body: str, cc: str = "") -> Dict[str, Any]:
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            recipients = [to] + ([cc] if cc else [])
            server.sendmail(SMTP_USER, recipients, msg.as_string())

        return {
            "status": "sent",
            "to": to,
            "subject": subject,
            "message": f"Email successfully sent to {to}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to send email: {e}",
        }

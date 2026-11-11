"""Email sink — sends without human-in-the-loop confirmation."""

import smtplib
from email.mime.text import MIMEText

from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


def send_internal_email(to: str, subject: str, body: str) -> str:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=5) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to], msg.as_string())
        return f"Email sent to {to} with subject '{subject}'."
    except Exception as e:
        # Demo still surfaces the attempted send (SMTP often unreachable locally)
        return (
            f"Email tool invoked without confirmation "
            f"(to={to}, subject={subject}). Transport error: {e}"
        )

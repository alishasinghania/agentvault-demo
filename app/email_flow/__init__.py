"""Multi-hop email path — user text → draft → smtplib send (no human confirm)."""

from app.email_flow.entry import handle_email_request

__all__ = ["handle_email_request"]

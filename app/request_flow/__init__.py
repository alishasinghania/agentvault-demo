"""Multi-hop request flow — several intentional cross-file taint paths.

Shared entry:
  app/main.py (body.message)
    → request_flow/intake.accept_user_message
      → request_flow/pass_through.forward_user_query
        → LLM:  llm_sink.invoke_chat_model (llm.invoke)
        → SQL:  sql_flow … → cursor.execute
        → RCE:  code_flow … → exec
        → Email: email_flow … → smtplib.sendmail
"""

from app.request_flow.intake import accept_user_message

__all__ = ["accept_user_message"]

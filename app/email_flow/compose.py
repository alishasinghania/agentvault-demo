from app.email_flow.send import send_internal_email
from app.llm import get_langchain_llm


def compose_and_send(user_text: str) -> str:
    llm = get_langchain_llm()
    draft = llm.invoke(
        "Draft an internal email from this request. "
        "Reply with three lines: TO:, SUBJECT:, BODY:\n\n"
        f"{user_text}"
    )
    to_addr = "hr@meridian.com"
    subject = "AgentVault draft"
    body = draft
    for line in draft.splitlines():
        if line.upper().startswith("TO:"):
            to_addr = line.split(":", 1)[1].strip() or to_addr
        elif line.upper().startswith("SUBJECT:"):
            subject = line.split(":", 1)[1].strip() or subject
        elif line.upper().startswith("BODY:"):
            body = line.split(":", 1)[1].strip() or body
    return send_internal_email(to_addr, subject, body)

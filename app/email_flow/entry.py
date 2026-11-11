from app.email_flow.compose import compose_and_send


def handle_email_request(message: str) -> str:
    return compose_and_send(message)

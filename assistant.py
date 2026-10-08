"""Assistant logic: where the "thinking" and tasks will live.

For now this just echoes. Later, replace handle_message with a call to an LLM
(e.g. the Claude API) plus whatever tools/tasks the assistant should perform.
"""


async def handle_message(user_id: int, text: str) -> str:
    return f"You said: {text}"

from cohere import AsyncClient

from app.config import settings

from app.services.transcript_context import format_transcript_context


def format_chat_history(chat_history: list[dict] | None) -> str:
    if not chat_history:
        return "No previous chat history."

    lines = []

    for row in chat_history:
        sender = row.get("sender", "unknown")
        message = row.get("message", "").strip()

        if not message:
            continue

        lines.append(f"{sender}: {message}")

    return "\n".join(lines) if lines else "No previous chat history."


async def generate_agent_reply(
    *,
    user_message: str,
    transcript_context: str | None = None,
    chat_history: list[dict] | None = None,
) -> str:
    cohere = AsyncClient(settings.cohere_api_key)

    history_text = format_chat_history(chat_history)

    transcript_text = format_transcript_context(transcript_context)

    prompt = f"""
You are Agent v1 for a personal AI note-taking app.

You help users talk naturally with their saved recordings, transcripts, and chat history.

Important rules:
- You DO have access to the recent chat history shown below.
- Treat the recent chat history as real previous messages in this conversation.
- If the user asks what they said earlier, answer from the recent chat history.
- Do not say you cannot access previous messages unless the recent chat history is empty.
- If transcript context is missing, answer from chat history only.
- Be helpful, conversational, and concise.

Recent chat history for this recording, oldest to newest:
{history_text}

Transcript context:
{transcript_text}

Current user message:
{user_message}
""".strip()

    response = await cohere.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.3,
    )

    return response.text.strip()
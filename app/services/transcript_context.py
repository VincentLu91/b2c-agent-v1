MAX_TRANSCRIPT_CONTEXT_CHARS = 12000


def was_transcript_truncated(transcript_context: str | None) -> bool:
    return (
        transcript_context is not None
        and len(transcript_context.strip()) > MAX_TRANSCRIPT_CONTEXT_CHARS
    )


def format_transcript_context(transcript_context: str | None) -> str:
    if not transcript_context or not transcript_context.strip():
        return "No transcript context provided yet."

    cleaned = transcript_context.strip()

    if len(cleaned) <= MAX_TRANSCRIPT_CONTEXT_CHARS:
        return cleaned

    return (
        cleaned[:MAX_TRANSCRIPT_CONTEXT_CHARS]
        + "\n\n[Transcript was truncated because it was too long for this Agent v1 request.]"
    )
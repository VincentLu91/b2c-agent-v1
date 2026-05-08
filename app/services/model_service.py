async def generate_agent_reply(user_message: str, transcript_context: str | None = None) -> str:
    """
    Provider-neutral model function.

    Today this is a stub.
    Later this can call Cohere, OpenAI, Anthropic, etc.
    The rest of the app should not care which provider is used.
    """

    return f"Stub model reply: {user_message}"
from typing import Literal

from supabase import Client, create_client

from app.config import settings


def get_supabase_client() -> Client:
    if not settings.supabase_url:
        raise RuntimeError("Missing SUPABASE_URL environment variable.")

    if not settings.supabase_service_role_key:
        raise RuntimeError("Missing SUPABASE_SERVICE_ROLE_KEY environment variable.")

    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
    )


def save_chat_message(
    *,
    user_id: str,
    sound_url: str,
    sender: Literal["user", "assistant"],
    message: str,
) -> dict:
    cleaned_message = message.strip()

    if not cleaned_message:
        raise ValueError("Cannot save an empty chat message.")

    supabase = get_supabase_client()

    response = (
        supabase.table("chat_history")
        .insert(
            {
                "user_id": user_id,
                "soundUrl": sound_url,
                "sender": sender,
                "message": cleaned_message,
            }
        )
        .execute()
    )

    if not response.data:
        raise RuntimeError("Supabase insert returned no saved chat message.")

    return response.data[0]

# helper to load previous messages for the recording
def get_chat_history(
    *,
    user_id: str,
    sound_url: str,
    limit: int = 12, # short term memory for now, load the last 12 messages for context
    # stored memory != model prompt memory
) -> list[dict]:
    supabase = get_supabase_client()

    response = (
        supabase.table("chat_history")
        .select("sender,message,created_at")
        .eq("user_id", user_id)
        .eq("soundUrl", sound_url)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    rows = response.data or []

    return list(reversed(rows))
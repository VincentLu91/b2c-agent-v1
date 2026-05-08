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
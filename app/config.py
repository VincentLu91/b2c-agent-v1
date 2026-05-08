import os

from dotenv import load_dotenv

load_dotenv()

# So later, instead of reading secrets randomly across files, we always import:
# xfrom app.config import settings
class Settings:
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_service_role_key: str | None = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    model_provider: str = os.getenv("MODEL_PROVIDER", "cohere")
    cohere_api_key: str | None = os.getenv("COHERE_API_KEY")

settings = Settings()
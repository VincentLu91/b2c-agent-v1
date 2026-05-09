from fastapi import FastAPI

from uuid import uuid4

import logging

from app.schemas import AgentRespondRequest, AgentRespondResponse, AgentError
from app.services.model_service import generate_agent_reply
from app.services.supabase_service import get_chat_history, save_chat_message
from app.services.transcript_context import was_transcript_truncated

# create backend application
app = FastAPI(
    title="B2C Agent v1",
    version="0.1.0"
)

logger = logging.getLogger(__name__)

@app.get("/")
def root():
    return {
        "service": "b2c-agent-v1",
        "status": "running",
    }

# health check route
@app.get("/healthz")
def health_check():
    return {
        "status": "healthy",
    }

@app.post("/v1/agent/respond", response_model=AgentRespondResponse)
async def agent_respond(request: AgentRespondRequest):
    conversation_id = request.conversation_id or f"{request.user_id}:{request.sound_url}"
    assistant_message_id = f"msg_{uuid4()}"
    transcript_was_truncated = was_transcript_truncated(request.transcript_context)

    try:
        chat_history = get_chat_history(
            user_id=request.user_id,
            sound_url=request.sound_url,
        )

        save_chat_message(
            user_id=request.user_id,
            sound_url=request.sound_url,
            sender="user",
            message=request.user_message,
        )

        assistant_message = await generate_agent_reply(
            user_message=request.user_message,
            transcript_context=request.transcript_context,
            chat_history=chat_history,
        )

        save_chat_message(
            user_id=request.user_id,
            sound_url=request.sound_url,
            sender="assistant",
            message=assistant_message,
        )

        return AgentRespondResponse(
            status="ok",
            conversation_id=conversation_id,
            assistant_message_id=assistant_message_id,
            assistant_message=assistant_message,
            transcript_was_truncated=transcript_was_truncated,
            error=None,
        )

    except Exception:
        logger.exception("Agent response failed")

        return AgentRespondResponse(
            status="error",
            conversation_id=conversation_id,
            assistant_message_id=None,
            assistant_message=None,
            transcript_was_truncated=transcript_was_truncated,
            error=AgentError(
                code="agent_response_failed",
                message="Agent response failed. Please try again.",
            ),
        )
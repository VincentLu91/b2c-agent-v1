from typing import Literal, Optional

from pydantic import BaseModel
# BaseModel is the Pydantic class that lets us define the shape of JSON data. ^^

# turn the request contract into a Python model.
# FastAPI uses Pydantic models to validate incoming JSON.


class AgentRespondRequest(BaseModel):
    # The app may send an existing conversation ID, but it can also be missing for a brand-new chat.
    # what if you're in a brand new chat and there's nothing there to begin with?
    conversation_id: Optional[str] = None
    
    # The app must send a recording ID.
    recording_id: str
    sound_url: str
    
    # only "mic" or "call" are allowed values
    recording_type: Literal["mic", "call"]
    user_id: str
    user_message: str
    
    # Only "web" or "expo" are allowed.
    platform: Literal["web", "expo"]


class AgentError(BaseModel):
    code: str
    message: str


class AgentRespondResponse(BaseModel):
    status: Literal["ok", "error"]
    conversation_id: Optional[str] = None
    assistant_message_id: Optional[str] = None
    assistant_message: Optional[str] = None
    error: Optional[AgentError] = None
# Agent v1 Contract

## Endpoint

POST /v1/agent/respond

## Purpose

Given a user message and a recording transcript context, return one assistant response and save the conversation.

## Request body

```json
{
  "conversation_id": "optional-reserved-for-future",
  "recording_id": "required-recording-id",
  "recording_type": "mic_or_call",
  "sound_url": "required-existing-soundUrl-thread-key",
  "user_id": "required-user-id",
  "user_message": "What did we decide in this call?",
  "platform": "web_or_expo"
}

## Agent v1 conversation identity

For Agent v1, chat history is grouped using the existing Supabase `chat_history` table:

```txt
user_id + soundUrl

## Response body

```json
{
  "status": "ok",
  "conversation_id": "conversation-id",
  "assistant_message_id": "assistant-message-id",
  "assistant_message": "The main decision was...",
  "error": null
}
```

## Error response body

```json
{
  "status": "error",
  "conversation_id": null,
  "assistant_message_id": null,
  "assistant_message": null,
  "error": {
    "code": "TRANSCRIPT_NOT_FOUND",
    "message": "Could not find the transcript for this recording."
  }
}
```
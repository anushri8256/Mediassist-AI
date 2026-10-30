
"""
MediAssist AI - FastAPI Backend
Uses our locally trained Random Forest model.
No external AI API or Qwen inference.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chat_engine import ChatEngine


# Initialize application
app = FastAPI(
    title="MediAssist AI Backend",
    description="Educational Symptom-Based ML Assistant",
    version="3.0.0"
)

# Allow local frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load our trained model
print("[Server] Starting MediAssist AI...")

try:
    engine = ChatEngine()
    print("[Server] MediAssist ML Engine Ready!")

except Exception as error:
    print("[Server Error]", error)
    engine = None


# Request and response models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    reply: str


# Home endpoint
@app.get("/")
def home():
    return {
        "status": "online",
        "service": "MediAssist AI",
        "model": "Self-trained Random Forest",
        "external_ai_api": False
    }


# Health check
@app.get("/health")
def health():
    return {
        "healthy": engine is not None,
        "engine_ready": engine is not None
    }


# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if engine is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MediAssist model is not ready."
        )

    user_message = request.message.strip()

    if not user_message:
        return ChatResponse(
            reply="Please enter your symptoms."
        )

    try:
        response = engine.chat(user_message)

        return ChatResponse(reply=response)

    except Exception as error:
        print("[Chat Error]", error)

        return ChatResponse(
            reply="Sorry, something went wrong. Please try again."
        )

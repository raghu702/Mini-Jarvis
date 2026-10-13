from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_services import process_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    conversation_id: str


@app.get("/")
def home():
    return {
        "message": "SAH-AI backend is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    reply = process_message(
        request.message,
        request.conversation_id
    )

    return {
        "reply": reply
    }
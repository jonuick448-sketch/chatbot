import os
from collections import deque

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store conversation history (last 10 messages)
conversation_history = deque(maxlen=10)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": request.message
    })
    
    # Create messages list for API call
    messages = list(conversation_history)
    
    # Call OpenAI API with conversation history
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    
    assistant_message = response.choices[0].message.content
    
    # Add assistant response to history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return {"reply": assistant_message}
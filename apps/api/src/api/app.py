from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import os

from api.config.settings import config
from api.domain.llm import LLMProvider as LLM

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    provider_name: str
    model_name: str
    messages: list[dict]

class ChatResponse(BaseModel):
    message: str

app = FastAPI()

@app.post("/chat")
def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    #print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
    #print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
    #print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
    client = LLM.create_client(config, payload.provider_name, payload.model_name)
    result = client.send(payload.messages)
    return ChatResponse(message=result)



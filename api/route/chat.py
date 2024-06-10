import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from api.service import shell
from api.service.ollama import ChatBot

import requests

router = APIRouter()
prefix = "/chat"

chat_model = os.environ.get("CHAT_MODEL", "llama3")
ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
chroma_host = os.environ.get("CHROMA_HOST", "localhost")
chroma_port = os.environ.get("CHROMA_PORT", 8000)
chroma_collection = os.environ.get("CHROMA_COLLECTION", "ecosoc")

chatbot = ChatBot(
    ollama_base_url=ollama_base_url,
    chat_model=chat_model,
    chroma_host=chroma_host,
    chroma_port=chroma_port,
    chroma_collection=chroma_collection
)


def check_connection():
    try:
        requests.get(ollama_base_url)
    except requests.exceptions.ConnectionError:
        return False
    return True


@router.get("/ecosoc-resolutions", response_class=StreamingResponse)
async def ecosoc_resolutions(query: str):
    return StreamingResponse(chatbot.invoke(query))


def setup(app):
    if check_connection():
        shell.print_yellow_message(f"Connected to Ollama at {ollama_base_url}")
    else:
        shell.print_red_message(f"Failed to connect to Ollama at {ollama_base_url}")
        raise ConnectionError("Failed to connect to Ollama")

    app.include_router(router, prefix=prefix)

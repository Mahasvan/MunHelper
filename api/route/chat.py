import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from api.service import shell
from api.service.ollama import ChatBot

router = APIRouter()
prefix = "/chat"


chat_model = os.environ.get("CHAT_MODEL", "llama3")
ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
chroma_host = os.environ.get("CHROMA_HOST", "localhost")
chroma_port = os.environ.get("CHROMA_PORT", 8000)

chatbot = ChatBot(chat_model=chat_model, chroma_host=chroma_host, chroma_port=chroma_port, chroma_collection="ecosoc")


@router.get("/ecosoc-resolutions", response_class=StreamingResponse)
async def ecosoc_resolutions(query: str):
    return StreamingResponse(chatbot.invoke(query))


def setup(app):
    app.include_router(router, prefix=prefix)

from fastapi import APIRouter

from src.api.schemas import ChatRequest, ChatResponse
from src.rag.service import RAG_Ko4rut

router = APIRouter()

rag_service = RAG_Ko4rut()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = rag_service.ask(request.question)
    return ChatResponse(**result)
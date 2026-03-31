from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class SourceItem(BaseModel):
    filename: str | None = None
    source: str | None = None
    chunk_id: int | None = None
    start_index: int | None = None


class Timings(BaseModel):
    retrieve_s: float
    filter_s: float
    llm_s: float
    total_s: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceItem]
    timings: Timings
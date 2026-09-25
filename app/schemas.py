from typing import List

from pydantic import BaseModel


class DocumentAnalysis(BaseModel):
    title: str
    summary: str
    topics: List[str]
    entities: List[str]
    key_points: List[str]
    dates: List[str]
    important_numbers: List[str]

class DocumentChunk(BaseModel):
    chunk_id: str
    page: int
    text: str
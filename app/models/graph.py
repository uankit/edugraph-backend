from typing import List
from pydantic import BaseModel


class GraphNode(BaseModel):
    title: str
    description: str
    category: str
    type: str

class GraphEdge(BaseModel):
    source: str
    target: str
    similarity: float | None

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class GraphDataSubtopics(BaseModel):
    topic: str
    subtopics: List[str]
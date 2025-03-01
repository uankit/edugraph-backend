from pydantic import BaseModel, Field
from typing import List

class Topic(BaseModel):
    topic: str = Field(..., description="The title of the topic")
    description: str = Field(..., description="The description of the topic")
    category: str = Field(..., description="The category of the topic")
    subtopics: List[str] = Field(..., description="The subtopics of the topic")

class MapTopics(BaseModel):
    topics: List[Topic]

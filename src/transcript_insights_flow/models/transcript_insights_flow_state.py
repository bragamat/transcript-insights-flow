
from typing import List, Optional
from pydantic import BaseModel, Field


class TranscriptInsightsState(BaseModel):
    question: str = Field(default="", description="The question to analyze the transcript for.")
    errors: Optional[List[str]] = Field(default_factory=list, description="List of error messages encountered during processing.")


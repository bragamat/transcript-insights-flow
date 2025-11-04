
from pydantic import BaseModel, Field


class TranscriptAnalystCrewOutput(BaseModel):
    answer: str = Field(..., description="The synthesized answer to the question based on the transcript")
    relevant_quotes: str = Field(..., description="Relevant quotes from the transcript that support the answer")

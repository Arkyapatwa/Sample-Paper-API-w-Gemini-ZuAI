from pydantic import BaseModel, field_validator, Field
from typing import List, Dict


class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: str
    reference_id: str
    hint: str
    params: Dict = {}

    @field_validator('type')
    def validate_type(cls, v):
        if v not in ['short', 'long']:
            raise ValueError('Type must be either short or long')
        return v

class Section(BaseModel):
    marks_per_question: int
    type: str
    questions: List[Question]

class SamplePaper(BaseModel):
    title: str
    type: str
    time: int = Field(...,ge=1, description="Time must be greater than or equal to 1")
    marks: int = Field(...,ge=1, description="Marks must be greater than or equal to 1")
    params: Dict
    tags: List[str]
    chapters: List[str]
    sections: List[Section]
    

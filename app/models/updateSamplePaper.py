from pydantic import BaseModel, field_validator, Field
from typing import List, Dict, Optional

class UpdateQuestion(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    type: Optional[str] = None
    question_slug: Optional[str] = None
    reference_id: Optional[str] = None
    hint: Optional[str] = None
    params: Optional[Dict] = None

    @field_validator('type')
    def validate_type(cls, v):
        if v not in ['short', 'long']:
            raise ValueError('Type must be either short or long')
        return v

class UpdateSection(BaseModel):
    marks_per_question: Optional[int] = None
    type: Optional[str] = None
    questions: Optional[List[UpdateQuestion]] = None

class UpdateSamplePaper(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    time: Optional[int] = Field(None, ge=1, description="Time must be greater than or equal to 1")
    marks: Optional[int] = Field(None, ge=1, description="Marks must be greater than or equal to 1")
    params: Optional[Dict] = None
    tags: Optional[List[str]] = None
    chapters: Optional[List[str]] = None
    sections: Optional[List[UpdateSection]] = None
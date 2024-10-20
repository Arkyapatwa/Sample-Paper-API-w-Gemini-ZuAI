import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
# from app.models.samplePaper import SamplePaper, Section, Question
import os

load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="You are a Teacher. Analyze the context and extract the sample paper data in JSON format.")

from pydantic import BaseModel, Field
from typing import List, Dict

class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: str
    reference_id: str
    hint: str
    params: Dict = {}


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
    
def model_to_json(model_instance: SamplePaper):
        """
        Converts a Pydantic model instance to a JSON string.
        Args:
            model_instance (Model): An instance of Pydantic model.
        Returns:
            str: A JSON string representation of the model.
        """
        return model_instance.model_dump()

def extract_from_text(text: str):
    """
    Extaract the sample Paper JSON from the text
    """
    
        
    base_prompt = f"Based on the following descriptive context, extract the relevant information in JSON. Context: {text}"
    json_model = model_to_json(SamplePaper(title="title1", type="type1", time=1, marks=1, params={}, tags=[], chapters=[], sections=[Section(marks_per_question=1, type="type1", questions=[Question(question="question1", answer="answer1", type="type1", question_slug="question1", reference_id="reference1", hint="hint1", params={})])]))
    optimized_prompt = base_prompt + f'.Please provide a response in a structured JSON format that matches the following model: {json_model}'
    
    
    response = model.generate_content(optimized_prompt, generation_config=genai.types.GenerationConfig(
        temperature=0.1,
        
    ))
    
    result = json.loads(response.text.split('json')[1].replace("```","").strip())
    
    return result


async def extract_from_pdf(file_path: str):
    print(file_path)
    
    base_prompt = f"Based on the following file content, extract the relevant information in JSON."
    json_model = model_to_json(SamplePaper(title="title1", type="type1", time=1, marks=1, params={}, tags=[], chapters=[], sections=[Section(marks_per_question=1, type="type1", questions=[Question(question="question1", answer="answer1", type="type1", question_slug="question1", reference_id="reference1", hint="hint1", params={})])]))
    optimized_prompt = base_prompt + f'.Please provide a response in a structured JSON format that matches the following model: {json_model}'
    
    sample_pdf = genai.upload_file(path=file_path, display_name="sample_pdf")
    response = model.generate_content([optimized_prompt, sample_pdf], generation_config=genai.types.GenerationConfig(
        temperature=0.1,
    ))
    
    result = str(response.text.replace('json', "").replace("```","").strip()).replace("'","\"")
    print(result)
    return json.loads(result)
    
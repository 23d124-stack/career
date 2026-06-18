from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    skills: str

class LoginUser(BaseModel):
    email: str
    password: str
class ProfileUpdate(BaseModel):
    email: str
    degree: str
    college: str
    graduation_year: str
class ResumeResponse(BaseModel):
    skills: str
from typing import List

class SkillInput(BaseModel):
    skills: List[str]
class PreferenceUpdate(BaseModel):
    email: str
    preferred_company: str
    preferred_domain: str
    preferred_location: str
    job_type: str
from typing import List

class SkillGapRequest(BaseModel):
    current_skills: List[str]
    target_role: str
class RoadmapRequest(BaseModel):
    target_role: str
from pydantic import BaseModel
class PreferenceCreate(BaseModel):
    email: str
    preferred_company: str
    preferred_domain: str
    preferred_location: str
    job_type: str
from pydantic import BaseModel
from pydantic import BaseModel

class MockInterviewStart(BaseModel):
    role: str
    experience: str

class MockAnswerRequest(BaseModel):
    question: str
    answer: str
    role: str

class ResumeScoreRequest(BaseModel):
    target_role: str
    skills: list[str]
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
class ApplyJobRequest(BaseModel):
    email: str
    company: str
    role: str
    apply_link: str
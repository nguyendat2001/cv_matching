from typing import TypedDict, Annotated, Any, List, Optional
from pydantic import BaseModel, create_model, Field

class UserInfo(BaseModel):
    name: str
    date_of_birth: Optional[str] = Field(None, description="Date of birth (optional)")
    position: Optional[str] = Field(None, description="Current position (optional)")
    email: str
    phone_number: str
    university: List[str] = Field(..., description="List of universities attended")
    technical_skill: List[str] = Field(..., description="List of technical skills")
    certificate: List[str] = Field(..., description="List of certificates")
    degree: List[str] = Field(..., description="List of degrees")
    soft_skill: List[str] = Field(..., description="List of soft skills")
    year_experience: List[str] = Field(..., description="Years of experience")
    responsibility: str
    english_level: List[str] = Field(..., description="English proficiency levels")

def create_dynamic_userinfo(num_answers: int):
    """Creates a dynamic UserInfo model with additional answer fields."""
    dynamic_fields = {
        f"answer_{i}": (Optional[str], Field(None, description=f"Answer to question {i} (optional)"))
        for i in range(1, num_answers + 1)
    }
    DynamicUserInfo = create_model(
        "DynamicUserInfo", __base__=UserInfo, **dynamic_fields
    )
    return DynamicUserInfo


class JobDescription(TypedDict):
    degree: List[Any]
    year_experience: List[Any]
    technical_skill: List[Any]
    responsibility: List[Any]
    certificate: List[Any]
    soft_skill: List[Any]
    english_level: List[Any]


def create_dynamic_job_des(num_answers: int):
    """Creates a dynamic JobDescription model with additional answer fields."""
    dynamic_fields = {
        f"correct_answer_{i}": (Optional[str], Field(None, description=f"Correct answer to question {i} (optional)"))
        for i in range(1, num_answers + 1)
    }
    DynamicJobDescription = create_model(
        "DynamicJobDescription", __base__=JobDescription, **dynamic_fields  # type: ignore
    )
    return DynamicJobDescription

class Skill(TypedDict):
    code:str
    name:str
    score:int

class SkillRequirementScore(TypedDict):
    university:list[Skill]
    degree:list[Skill]
    english_level:list[Skill]
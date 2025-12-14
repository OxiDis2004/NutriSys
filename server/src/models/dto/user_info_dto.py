from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.property.activity import Activity
from src.models.property.goal import Goal


class UserInfoDTO(BaseModel):
    id: UUID = Field(..., description="Unique user identifier")
    name: str = Field(None, max_length=55, pattern=r"^[a-zA-Z\- ]+$", description="First name")
    lastname: str = Field(None, max_length=55, pattern=r"^[a-zA-Z\- ]+$", description="Last name")
    birthday: date = Field(None, description="Date of birth")
    weight: int = Field(None, ge=0, le=500, description="Weight in kilograms")
    height: int = Field(None, ge=0, le=300, description="Height in centimeters")
    sex: str = Field(None, max_length=10, pattern=r"^(male|female|other)$", description="Sex")
    count_of_sport_in_week: Activity = Field(None, description="Level of weekly activity")
    goal: Goal = Field(None, description="User goal")
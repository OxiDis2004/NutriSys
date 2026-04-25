from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from src.models.property.activity import Activity
from src.models.property.goal import Goal


class UserInfoDTO(BaseModel):
    id: UUID | None = Field(..., description="Unique user identifier")
    name: str | None = Field(
        None, max_length=55, pattern=r"^[a-zA-Z\- ]+$", description="First name"
    )
    lastname: str | None = Field(
        None, max_length=55, pattern=r"^[a-zA-Z\- ]+$", description="Last name"
    )
    birthday: date | None = Field(None, description="Date of birth")
    weight: int | None = Field(None, ge=0, le=500, description="Weight in kilograms")
    height: int | None = Field(None, ge=0, le=300, description="Height in centimeters")
    sex: str | None = Field(None, max_length=1, pattern=r"^(m|w)$", description="Sex")
    activity: Activity | None = Field(None, description="Level of weekly activity")
    goal: Goal | None = Field(None, description="User goal")

    @property
    def user_id(self):
        return str(self.id)

    @field_serializer("id")
    def serialize_id(self, id) -> str:
        return str(id)

    @field_serializer("activity")
    def serialize_activity(self, activity):
        return activity.value if activity is not None else None

    @field_serializer("goal")
    def serialize_goal(self, goal):
        return goal.value if goal is not None else None

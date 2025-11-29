from pydantic import BaseModel
from datetime import date


class UserLoginSchema(BaseModel):
    email: str
    password: str

class PatientHistoryItem(BaseModel):
    id: int
    doctor_id: int
    last_name: str
    first_name: str
    middle_name: str | None
    exam_date: date
    description: str | None
    file_name: str | None

    class Config:
        orm_mode = True

class UserProfileSchema(BaseModel):
    id: int
    email: str
    last_name: str
    first_name: str
    middle_name: str | None

    model_config = {"from_attributes": True}
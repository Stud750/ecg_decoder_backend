from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey, Text
from postgres_db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    exam_date = Column(Date, nullable=False)
    raw_file = Column(LargeBinary)
    image_png = Column(LargeBinary)
    description = Column(Text)
    file_name = Column(String(255))


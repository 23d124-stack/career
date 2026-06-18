from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    skills = Column(String)

    degree = Column(String)
    college = Column(String)
    graduation_year = Column(String)

    preferred_company = Column(String)
    preferred_domain = Column(String)
    preferred_location = Column(String)
    job_type = Column(String)
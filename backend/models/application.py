from sqlalchemy import Column, Integer, String
from database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    apply_link = Column(String)
    status = Column(String, default="Applied")
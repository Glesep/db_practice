from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE

class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)

class User(BaseModel):
    id: int
    name: str
    age: int 
from sqlalchemy import Column, Integer, String                                                      # DB 모델을 정의할 때 사용되는 클래스
from pydantic import BaseModel                                                                      # pydantic 중 BaseModel 클래스 사용
from db import Base                                                                                 # db.py에서 Base 클래스 사용
from db import ENGINE                                                                               # db.py에서 ENGINE 클래스 사용

class UserTable(Base):                                                                              # Base 클래스를 상속하여 만든 DB모델인 UserTable 클래스
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)

class User(BaseModel):                                                                              # BaseModel 클래스를 상속하여 만든 User 클래스, 데이터 유효성 검사(데이터 생성 시 거름망 역할), 데이터 구조화를 실행
    id: int
    name: str
    age: int 
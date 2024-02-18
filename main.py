from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware

# 같은 이름, 다른 종류의 파일이 같은 경로에 있을 때 파일 충돌 가능성 높음, 주의하자
from db import session
from model import UserTable, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 앞에 골뱅이 제발 붙여!!
@app.get("/users/")
async def read_users():
    users = session.query(UserTable).all()

    return users

@app.get("/users/{user_id}")
async def read_user(user_id: int):

    user = session.query(UserTable).filter(UserTable.id == user_id).first()

    return user

@app.post("/user")
async def create_user(name:str, age: int):

    user = UserTable()                                                                      # ORM 객체를 만듦 (서버와 DB의 중간다리 역할), ORM 객체에는 __tablename__에 해당하는 테이블의 정보가 있음
    user.name = name                                                                        # name 입력          
    user.age = age                                                                          # age 입력  

    session.add(user)                                                                       # session에 user ORM객체 추가
    session.commit()                                                                        # session 실행 (데이터베이스에 위의 name, age 추가)

    return f"{name} created..."

@app.put("/users")
async def update_users(users: List[User]):

    for i in users:
        user = session.query(UserTable).filter(UserTable.id == i.id).first()
        user.name = i.name
        user.age = i.age
        session.commit()

        return f"{users[0].name} updated..."
    
@app.delete("/user")
async def delete_users(userid: int): 
    user = session.query(UserTable).filter(UserTable.id == userid).delete()
    session.commit()

    return "User deleted..."
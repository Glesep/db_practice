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

app.get("/users/{user_id}")
async def read_user(user_id: int):

    user = session.query(UserTable).filter(UserTable.id == user_id).first()

    return user
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from typing import List
from starlette.middleware.cors import CORSMiddleware

# 같은 이름, 다른 종류의 파일이 같은 경로에 있을 때 파일 충돌 가능성 높음, 주의하자
from db import session
from model import UserTable, User

templetes = Jinja2Templates(directory="templates")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "/users 에서 사용자관리"}

# 앞에 골뱅이 제발 붙여!! 경로 표기는 /도 정확히!
@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    context= {}
    users = session.query(UserTable).all()

    context["request"] = request
    context["users"] = users

    return templetes.TemplateResponse("user_list.html", context)


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):

    context= {}

    user = session.query(UserTable).filter(UserTable.id == user_id).first()

    context["name"] = user.name
    context["age"] = user.age
    context["request"] = request

    return templetes.TemplateResponse("user_detail.html", context)


@app.post("/users")
async def create_user(users: User):

    userlist = list(users)
    uname = userlist[1][1]
    uage = userlist[2][1]


    user = UserTable()                                                                      # ORM 객체를 만듦 (서버와 DB의 중간다리 역할), ORM 객체에는 __tablename__에 해당하는 테이블의 정보가 있음
    user.name = uname                                                                        # name 입력          
    user.age = uage                                                                          # age 입력  

    session.add(user)                                                                       # session에 user ORM객체 추가
    session.commit()                                                                        # session 실행 (데이터베이스에 위의 name, age 추가)

    return {"result_msg", f"{uname} Registered..."}

@app.put("/users")
async def update_users(users: User):

    userlist = list(users)
    uid = userlist[0][1]
    uname = userlist[1][1]
    uage = userlist[2][1]
                       
   
    user = session.query(UserTable).filter(UserTable.id == uid).first()
    user.name = uname
    user.age = uage
    session.commit()

    return {"result_msg", f"{uname} updated..."}
    
@app.delete("/users")
async def delete_users(users: User): 

    userlist = list(users)
    uid = userlist[0][1]

    user = session.query(UserTable).filter(UserTable.id == uid).delete()
    session.commit()

    return {"result_msg", "User deleted..."}
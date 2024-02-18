from fastapi import FastAPI, Request                                                                # Request: 클라이언트로부터의 HTTP 요창을 처리하는데 사용, 각 엔드포인트 함수의 첫 번째 매개변수로 Request 객체를 사용하여 클라이언트로부터의 요청을 처리
from fastapi.responses import HTMLResponse                                                          # FastAPI에서 HTML을 반환하는데 사용하는 응답 클래스
from fastapi.templating import Jinja2Templates                                                      # FastAPI에서 HTML 템플릿을 사용할 수 있도록 만드는 클래스


from typing import List                                                                             # List 타입 힌트를 주는 클래스
from starlette.middleware.cors import CORSMiddleware                                                # CORS를 지원하기 위해 만들어진 클래스(CORS: 웹 애플리캐이션이 다른 도메인에 있는 리소스를 요청할 수 있도록 허용하는 정책)

# 같은 이름, 다른 종류의 파일이 같은 경로에 있을 때 파일 충돌 가능성 높음, 주의하자
from db import session                                                                              # db.py에서 session 들고 옴
from model import UserTable, User                                                                   # model.py에서 UserTable, User 들고 옴

templetes = Jinja2Templates(directory="templates")                                                  # templates 경로에 있는 템플릿을 렌더링할 수 있도록 허용

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                                                                            # 모든 도메인에서의 요청 허용
    allow_credentials=True,                                                                         # 인증 정보를 포함한 요청 허용
    allow_methods=["*"],                                                                            # 모든 HTTP methods 허용
    allow_headers=["*"],                                                                            # 모든 HTTP headers 허용
)

@app.get("/")
async def root():
    return {"message": "/users 에서 사용자관리"}

# 앞에 골뱅이 제발 붙여!! 경로 표기는 /도 정확히!
@app.get("/users", response_class=HTMLResponse)                                                     # response_class=HTMLResponse: 해당 엔드포인트의 응답 클래스를 HTMLResponse로 설정 -> FastAPI가 해당 엔드포인트의 응답이 HTML임을 인식 후 적절한 형식으로 반환
async def read_users(request: Request):                                                             # 엔드포인트 함수의 첫번째 매개변수로 Request 객체를 사용하여 클라이언트로부터의 요청 처리
    context= {}                                                                                     # context라는 딕셔너리 생성
    users = session.query(UserTable).all()                                                          # UserTable 클래스에 속해있는 테이블의 모든 데이터 조회

    context["request"] = request                                                                    # key: request, value: request인 첫 번째 딕셔너리 요소 생성
    context["users"] = users                                                                        # key: users, value: users인 두 번째 딕셔너리 요소 생성

    return templetes.TemplateResponse("user_list.html", context)                                    # 응답으로 user_list.html 템플릿 불러옴, 이 템플릿에 context 딕셔너리를 전달(request 정보, users(테이블 속 데이터 정보))


@app.get("/users/{user_id}", response_class=HTMLResponse)                                           # user_id: 경로 매개변수, response_class=HTMLResponse: 해당 엔드포인트의 응답 클래스를 HTMLResponse로 설정 -> FastAPI가 해당 엔드포인트의 응답이 HTML임을 인식 후 적절한 형식으로 반환
async def read_user(request: Request, user_id: int):                                                # 엔드포인트 함수의 첫번째 매개변수로 Request 객체를 사용하여 클라이언트로부터의 요청 처리, user_id 매개변수 타입을 int로 설정 

    context= {}                                                                                     # context라는 딕셔너리 생성

    user = session.query(UserTable).filter(UserTable.id == user_id).first()                         # UserTable 클래스에 속해있는 테이블에서 filter 속 조건에 맞는 데이터들 중 첫 번째로 반환되는 항목을 가져옴

    context["name"] = user.name                                                                     # key: name, value: user.name인 첫 번째 딕셔너리 요소 생성
    context["age"] = user.age                                                                       # key: age, value: user.age인 두 번째 딕셔너리 요소 생성
    context["request"] = request                                                                    # key: request, value: request인 세 번째 딕셔너리 요소 생성

    return templetes.TemplateResponse("user_detail.html", context)                                  # 응답으로 user_detail.html 템플릿 불러옴, 이 템플릿에 context 딕셔너리를 전달


@app.post("/users")
async def create_user(users: User):                                                                 # FastAPI에선 클라이언트 측에서 온 JSON파일을 처리하기 위해 자동으로 괄호 안에 있는 모델 타입인 파이썬 객체를 만들어 사용할 수 있도록 함

    userlist = list(users)                                                                          # users(User) 클래스를 타입으로 가지는 속성으로 하는 리스트 , 딕셔너리를 요소로 가지는 리스트와 유사
    uname = userlist[1][1]                                                                          # 클라이언트 측에서 온 name 속성의 value 를 uname 변수에 저장 
    uage = userlist[2][1]                                                                           # 클라이언트 측에서 온 age 속성의 value를 uage 변수에 저장


    user = UserTable()                                                                              # ORM 객체를 생성 (서버와 DB의 중간다리 역할), ORM 객체에는 __tablename__에 해당하는 테이블의 정보가 있음
    user.name = uname                                                                               # user.name에 uname 저장 (ORM 객체에 저장 중)          
    user.age = uage                                                                                 # user.age에 uage 저장 (ORM 객체에 저장 중)  

    session.add(user)                                                                               # session에 user ORM 객체 추가
    session.commit()                                                                                # session 실행 (데이터베이스에 위의 name, age 추가)

    return {"result_msg", f"{uname} Registered..."}

@app.put("/users")
async def update_users(users: User):                                                                # FastAPI에선 클라이언트 측에서 온 JSON파일을 처리하기 위해 자동으로 괄호 안에 있는 모델 타입인 파이썬 객체를 만들어 사용할 수 있도록 함

    userlist = list(users)                                                                          # users(User) 클래스를 타입으로 가지는 속성으로 하는 리스트 , 딕셔너리를 요소로 가지는 리스트와 유사
    uid = userlist[0][1]                                                                            # 클라이언트 측에서 온 id 속성의 value 를 uid 변수에 저장 
    uname = userlist[1][1]                                                                          # 클라이언트 측에서 온 name 속성의 value 를 uname 변수에 저장 
    uage = userlist[2][1]                                                                           # 클라이언트 측에서 온 age 속성의 value 를 uage 변수에 저장 
                       
   
    user = session.query(UserTable).filter(UserTable.id == uid).first()                             # UserTable 클래스에 속해있는 테이블에서 filter 속 조건에 맞는 데이터들 중 첫 번째로 반환되는 항목을 가져옴  
    user.name = uname                                                                               # user.name(지정된 데이터)에 uname 저장 
    user.age = uage                                                                                 # user.age(지정된 데이터)에 uage 저장
    session.commit()                                                                                # session 실행 (데이터베이스에 위의 name, age 추가)

    return {"result_msg", f"{uname} updated..."}
    
@app.delete("/users")
async def delete_users(users: User):                                                                # FastAPI에선 클라이언트 측에서 온 JSON파일을 처리하기 위해 자동으로 괄호 안에 있는 모델 타입인 파이썬 객체를 만들어 사용할 수 있도록 함

    userlist = list(users)                                                                          # users(User) 클래스를 타입으로 가지는 속성으로 하는 리스트 , 딕셔너리를 요소로 가지는 리스트와 유사
    uid = userlist[0][1]                                                                            # 클라이언트 측에서 온 id 속성의 value 를 uid 변수에 저장

    session.query(UserTable).filter(UserTable.id == uid).delete()                                   # UserTable 클래스에 속해있는 테이블에서 filter 속 조건에 맞는 데이터를 삭제
    session.commit()                                                                                # session 실행 (삭제 사항 데이터베이스에 적용)

    return {"result_msg", "User deleted..."}
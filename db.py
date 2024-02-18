from sqlalchemy import create_engine                                                            # 데이터베이스와의 연결을 위해 사용하는 모듈
from sqlalchemy.ext.declarative import declarative_base                                         # 객체지향적으로 데이터베이스 모델을 정의하는데 사용하는 모듈
from sqlalchemy.orm import sessionmaker, scoped_session                                         # sessionmaker: 주어진 연결 엔진에 대한 세션을 생성, scoped_session: sessionmaker를 기반으로 하는 스레드로부터 안전한 세션을 생성하는 도구

user_name = "yoon"                                                                              # 데이터베이스 사용자 이름
user_pwd = "1234"                                                                               # 데이터베이스 사용자 비밀번호
db_host = "127.0.0.1:3306"                                                                      # 데이터베이스 호스트
db_name = "studyschema"                                                                         # 데이터베이스 이름(mysql: 스키마 이름)

DATABASE = "mysql+pymysql://%s:%s@%s/%s?charset=utf8" % (                                       # DB URL
    user_name,
    user_pwd,
    db_host,
    db_name,
)

ENGINE = create_engine(                                                                         # 엔진 생성
    DATABASE,                                                                                   # 엔진이 사용할 DB URL
    encoding="utf-8",                                                                           # utf-8로 인코딩
    echo=True,                                                                                  # DB에 실행하는 모든 SQL 쿼리들이 콘솔에 출력되도록 설정
)

session = scoped_session(                                                                       # 세션 제작
    sessionmaker(
        autocommit=False,                                                                       # SQLAlchemy의 autocommit(자동으로 DB에 변경 사항 반영) 모드 비활성화
        autoflush=False,                                                                        # autoflush(세션 내의 객체 상태와 DB 상태를 동기화하는데 사용하는 내부 버퍼링 메커니즘인 flush를 자동으로 활성화)를 비활성화
        bind=ENGINE,                                                                            # ENGINE이라는 엔진을 연결하여 세션을 생성
    )
)

Base = declarative_base()                                                                       # 객체지향적으로 데이터베이스 모델을 생성하기 위해 만드는 기본적인 클래스 Base, 모든 DB 모델 클래스는 Base클래스를 상속받아야 함
#Base.query = session.query_property()                                                          # Base 클래스를 상속받은 모든 모델 클래스에서 Base.query를 이용하여 쿼리 수행 가능(이해가 잘 ...)
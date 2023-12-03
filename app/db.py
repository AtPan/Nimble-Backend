import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQL_DB_URL = "maa-2.cb23pnbzjijy.us-east-1.rds.amazonaws.com"
SQL_DB_URL = "mysql-db"
#SQL_DB_URL = "localhost"
SQL_DB_PASS = "1qaz2wsx!QAZ@WSX"  #Has Original Password
#SQL_DB_PASS = "Daliilad3"
#SQL_DB_PASS_NOAT = "1qaz2wsx!QAZ%40WSX"


SQL_DB = sqlalchemy.engine.URL.create(
        drivername="mysql+pymysql",
        username="root",
        password=SQL_DB_PASS,
        host=SQL_DB_URL,
        port = 3306,
        database="academicAlly",
)
#SQL_DB = "mysql+pymysql://test1234:academicA!!y24@mysql-db:3306/academicAlly"

engine = create_engine(
    SQL_DB
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

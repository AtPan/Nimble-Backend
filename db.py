import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DB_URL = "maa-2.cb23pnbzjijy.us-east-1.rds.amazonaws.com"
SQL_DB_URL = "localhost"
SQL_DB_PASS = "1qaz2wsx!QAZ@WSX"
SQL_DB_PASS = "Daliilad3"
SQL_DB_PASS_NOAT = "1qaz2wsx!QAZ%40WSX"

SQL_DB = sqlalchemy.engine.URL.create(
        drivername="mysql",
        username="root",
        password=SQL_DB_PASS,
        host=SQL_DB_URL,
        database="academicAlly",
)

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

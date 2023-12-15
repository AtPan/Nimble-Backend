import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database information
SQL_DB_URL = "mysql-db"
SQL_DB_PASS = "1qaz2wsx!QAZ@WSX"  #Has Original Password

# Creates an sql engine
engine = create_engine(sqlalchemy.engine.URL.create(
        drivername="mysql+pymysql",
        username="root",
        password=SQL_DB_PASS,
        host=SQL_DB_URL,
        port = 3306,
        database="academicAlly",
))
# Creates a sql database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Retreives the database session. If the session is in use, hang until it becomes available.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

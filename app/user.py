from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from db import Base, get_db

router = APIRouter()

#sql tables must be made specifying non-null, autoincrement primary keys

class UserData(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)

class User(BaseModel):
    name: str
    password: str
    email: str
    class Config:
        orm_mode = True

@router.post("/api/users", tags=["users"])
def create_user(user: User, db: Session = Depends(get_db)):
    udata = fetch_user_by_email(db, user.email)
    if udata is not None:
        raise HTTPException(status_code=403, detail="Email in use")
    udata = UserData(name=user.name, password=user.password, email=user.email)
    db.add(udata)
    db.commit()
    db.refresh(udata)
    return {"message": "User created successfully"}

@router.get("/api/users/{user_id}", tags=["users"], response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    udata = fetch_user_by_id(db, user_id)
    if udata is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(name=udata.name, password=udata.password, email=udata.email).dict()

@router.put("/api/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    db.query(UserData).filter(user_id == UserData.id).update(user.dict())
    db.commit()
    return {"message": "Updated user successfully"}

@router.delete("/api/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.query(UserData).filter(user_id == UserData.id).delete()
    db.commit()
    return {"message": "Deleted user successfully"}

def fetch_user_by_id(db: Session, user_id: int):
    return db.query(UserData).filter(UserData.id == user_id).first()

def fetch_user_by_email(db: Session, email: str):
    return db.query(UserData).filter(UserData.email == email).first()

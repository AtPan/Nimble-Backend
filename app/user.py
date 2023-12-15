from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, select, delete, update
from sqlalchemy.orm import Session
from hashing import Hash
from db import Base, get_db
import JWTtoken as token

router = APIRouter()

#sql tables must be made specifying non-null, autoincrement primary keys

# The ORM representation of User. See `project.py` for more details.
class UserData(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)

# The representation of User used in the backend/frontend communications.
class User(BaseModel):
    name: str
    password: str
    email: str
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    email: str
    class Config:
        orm_mode = True

# Creates a user. Data must be sent as form data.
# If the user exists, send a 403.
# Auto creates a token for user authentication for the creation of tasks/projects.
@router.post("/api/users", tags=["users"])
def create_user(user: User, db: Session = Depends(get_db)):
    udata = fetch_user_by_email(db, user.email)
    if udata is not None:
        raise HTTPException(status_code=403, detail="Email in use")
    udata = UserData(name=user.name, password=Hash.bcrypt(user.password), email=user.email)
    db.add(udata)
    db.commit()
    db.refresh(udata)
    return {"message": "User created successfully", "access_token": token.create_access_token(data={"sub": user.email}), "token_type": "bearer"}

# Retreives a user's information by a given id.
# If there is no user of that id, a 404 is returned.
@router.get("/api/users/{user_id}", tags=["users"], response_model=ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    udata = fetch_user_by_id(db, user_id)
    if udata is None:
        raise HTTPException(status_code=404, detail="User not found")
    return udata

# Modifies a user's information by a given id.
# Information must be sent as form data.
@router.put("/api/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    db.execute(update(UserData).where(UserData.id==user_id).values({
        UserData.id: user.name,
        UserData.email: user.email,
        UserData.password: user.password
        }))
    db.commit()
    return {"message": "Updated user successfully"}

# Removes a user by a given id.
@router.delete("/api/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.execute(delete(UserData).where(UserData.id==user_id))
    db.commit()
    return {"message": "Deleted user successfully"}

def fetch_user_by_id(db: Session, user_id: int):
    row = db.execute(select(UserData).filter_by(id=user_id)).first()
    if row != None:
        row = row[0]
    return row

def fetch_user_by_email(db: Session, email: str):
    row = db.execute(select(UserData).filter_by(email=email)).first()
    if row != None:
        row = row[0]
    return row

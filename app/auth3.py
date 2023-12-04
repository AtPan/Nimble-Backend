from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import Base, get_db
from sqlalchemy.orm import Session
from user import UserData, fetch_user_by_email
from hashing import Hash
import token

router = APIRouter(
    tags=['Authentication']
)

class Login(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = fetch_user_by_email(db, login.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify(user.password, login.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")
    
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
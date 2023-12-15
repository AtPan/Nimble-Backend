from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import get_db
from sqlalchemy.orm import Session
from user import fetch_user_by_email
from hashing import Hash
import JWTtoken as token

router = APIRouter(
    tags=['Authentication']
)

# Pydantic model of our Login structure
class Login(BaseModel):
    username: str
    password: str

# POST method for /login endpoint
# Expects username/password fields sent as form data
# Sends a 404 if the given information does not correlate with an existing user
@router.post('/login')
def login(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = fetch_user_by_email(db, login.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify(user.password, login.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")
    
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

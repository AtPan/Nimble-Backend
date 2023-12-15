from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from JWTtoken import verify_token
from user import fetch_user_by_email
from db import get_db
from sqlalchemy.orm import Session

# OAuth2 password bearer authentication scheme.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency function to get the current user based on the provided JWT token.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    # Exception to be raised in case of token or credential validation failure
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify the token and extract payload data.
    tokenData = verify_token(token, credentials_exception)

    # Fetch user from the database based on the email in the token payload.
    user = fetch_user_by_email(db, tokenData.email)

    if user is None:
        print('could not find user')
    return user

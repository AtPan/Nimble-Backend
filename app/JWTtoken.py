from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from pydantic import BaseModel

# Secret key for JWT encoding and decoding. 
SECRET_KEY = "69fe363e3c8ad17d4d8a052a17018c68394a1cba585eea0da6d89e4267b526b7"

# Algorithm used for JWT encoding and decoding.
ALGORITHM = "HS256"

# Expiration time for access tokens in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic Model Token class representing the structure of an access token. 
class Token(BaseModel):
    access_token: str
    token_type: str

# Pydantic Model TokenData class representing the payload data of a decoded JWT token.
class TokenData(BaseModel):
    email: Union[str, None] = None

# Creates access token with provided data.  Using the username, returns a JWT access token.
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verifies the validity of a JWT token and extracts the email address from the payload.
def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except JWTError:
        raise credentials_exception
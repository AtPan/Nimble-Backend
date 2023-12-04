from passlib.context import CryptContext

PWD_CXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return PWD_CXT.hash(password)
    
    def verify(hashed_password, plain_password):
        return PWD_CXT.verify(plain_password, hashed_password)
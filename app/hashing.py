from passlib.context import CryptContext

# Create a CryptContext instance with bcrypt as the hashing scheme
PWD_CXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash class for password hashing and verification using bcrypt.
class Hash():

    # Hashes the input password using bcrypt.
    def bcrypt(password: str):
        return PWD_CXT.hash(password)
    
    # Verifies a plain password against a hashed password using bcrypt.
    def verify(hashed_password, plain_password):
        return PWD_CXT.verify(plain_password, hashed_password)
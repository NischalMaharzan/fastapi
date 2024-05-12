from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(passowrd: str):
    return pwd_context.hash(passowrd)

def verify(plain_password, encrypted_passowrd_from_DB):
    return pwd_context.verify(plain_password, encrypted_passowrd_from_DB)
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import models

def Hash(password:str):
    return pwd_context.hash(password)
     
     
def HashValidate(password,hashed_password):
    return pwd_context.verify(password,hashed_password)
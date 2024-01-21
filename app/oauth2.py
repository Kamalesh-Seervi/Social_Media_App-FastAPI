from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi import status, HTTPException,Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models

oauth2_scheme=OAuth2PasswordBearer('/user')

SECRET_KEY = "ebf160c96dab97c8be046b88f856134b743389ed1dd52afee8629d6005638d49"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# I am doing token validation when the client try to create_post and other imp routes
def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        email:str =payload.get("email_address")
        if id is None:
            raise credential_exception
        token_data=schemas.TokenData(email_address=email)
        
    except JWTError:
        raise credential_exception
    
    return token_data
    
    
# This func is used in the routing fields like /posts and soon on so we can use token validation 
    
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credential_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token=verify_access_token(token,credential_exception)
    user=db.query(models.User).filter(models.User.email==token.email_address).first()
    return user 
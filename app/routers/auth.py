from fastapi import FastAPI , Response, status, HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schemas import UserLogin
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from utils import HashValidate
import oauth2

router=APIRouter(
    tags=["Authentication"]
)


@router.post("/login",status_code=status.HTTP_201_CREATED)
def create_user(user_cred:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    
    user=db.query(models.User).filter(models.User.email==user_cred.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not HashValidate(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    access_token=oauth2.create_access_token(data={"user_id":user.id,"email_address":user.email})
    
    return {"Access_Token":access_token,"Token-Type":"Bearer"}
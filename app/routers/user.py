from typing import Union,List
from fastapi import FastAPI , Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from utils import Hash

router= APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # i am gonna hash password before we send into database
    hashed_password= Hash(user.password)
    user.password=hashed_password
    
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message":"Your account has been Created"}


@router.get("/{id}",response_model=schemas.UserProfileFromServer)
def get_user(id:int,db:Session=Depends(get_db)):
    
    getUser=db.query(models.User).filter(models.User.id==id).first()
    if not getUser :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    
    return getUser


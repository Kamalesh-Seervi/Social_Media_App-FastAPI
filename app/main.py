from typing import Union,List
from fastapi import FastAPI , Response, status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from passlib.context import CryptContext
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from database import engine,get_db
import models
import schemas
import utils


models.base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()

  
while True:
    try:
        conn = psycopg2.connect(host= 'localhost',database='fastapi_DB',user='postgres',password='0000', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connected")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:",error)
        time.sleep(2)

    
@app.get("/")  # path
def read_root():
    return {"message": "hello folks"}

# @app.get("/test")
# def orm_test(db:Session=Depends(get_db)):
#     post=db.query(models.Post).all()
#     return post


@app.get("/posts",response_model=List[schemas.PostFromServer])
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.PostFromServer)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}",response_model=schemas.PostFromServer)
def get_post(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    return post


@app.delete("/posts/{id}")
def del_post(id:int,db:Session=Depends(get_db)):
    delete=db.query(models.Post).filter(models.Post.id==id)

    if delete.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    schemas.PostCreate.delete(synchronize_session=False)
    db.commit()
    return {"Post_Details": delete}


@app.put("/posts/{id}",response_model=schemas.PostFromServer)
def update_post(id:int,Posts:schemas.PostCreate,db:Session=Depends(get_db)):
    update=db.query(models.Post).filter(models.Post.id ==id).first()
    if update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
     # Update individual attributes of the update object
    for key, value in Posts.dict(exclude_unset=True).items():
        setattr(update, key, value)
    db.commit()
    db.refresh(update)
    return update


@app.post("/user",status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # i am gonna hash password before we send into database
    hashed_password= utils.Hash(user.password)
    user.password=hashed_password
    
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"Your account has been Created"}


@app.get("/user/{id}",response_model=schemas.UserProfileFromServer)
def get_user(id:int,db:Session=Depends(get_db)):
    getUser=db.query(models.User).filter(models.User.id==id).first()
    if not getUser :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    return getUser
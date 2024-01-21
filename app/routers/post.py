from typing import Union,List
from fastapi import FastAPI , Response, status, HTTPException,Depends,APIRouter

from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from oauth2 import get_current_user


router= APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",response_model=List[schemas.PostFromServer])
def get_posts(db:Session=Depends(get_db)):
    
    posts=db.query(models.Post).all()
    
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostFromServer)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:str = Depends(get_current_user)):
    
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}",response_model=schemas.PostFromServer)
def get_post(id:int,db:Session=Depends(get_db)):
    
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    
    return post


@router.delete("/{id}")
def del_post(id:int,db:Session=Depends(get_db),current_user:str = Depends(get_current_user)):
    
    delete=db.query(models.Post).filter(models.Post.id==id)

    if delete.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    delete.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.PostFromServer)
def update_post(id:int,Posts:schemas.PostCreate,db:Session=Depends(get_db),current_user:str = Depends(get_current_user)):
    
    update=db.query(models.Post).filter(models.Post.id ==id).first()
    if update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
     # Update individual attributes of the update object
    for key, value in Posts.dict(exclude_unset=True).items():
        setattr(update, key, value)
    db.commit()
    db.refresh(update)
    
    return update
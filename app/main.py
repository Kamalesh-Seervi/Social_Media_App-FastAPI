from typing import Union
from fastapi import FastAPI , Response, status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine,get_db
#import engine from database.py
from . import models
#import models.py


models.base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
  
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

# storing data
# my_posts = [{"title": "title of of post 1", "content": "content of the post", "id": 1}, {
#     "title": "favorite foods", "content": "i like pizza", "id": 2
# }]


@app.get("/")  # path
def read_root():
    return {"message": "hello folks"}

@app.get("ormtest")
def betatest( db: Session = Depends(get_db)):
    return{"Status":"success"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts= cursor.fetchall()
    # print(posts)
    return {"message": posts}

# access based on each property
# fix a datatype so now you get a bug if specified datatype not followed


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def createpost(Post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(Post.title,Post.content,Post.published))
    new_post= cursor.fetchone()
    conn.commit()
    return {"message":new_post}


@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * from posts WHERE id=%s""",(str(id),))
    post=cursor.fetchone()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    return {"Post_Details": post}

@app.delete("/posts/{id}")
def del_post(id:int):
    cursor.execute("""DELETE from posts WHERE id=%s RETURNING *""",(str(id),))
    delete=cursor.fetchone()
    conn.commit()
    if not delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    return {"Post_Details": delete}

@app.put("/posts/{id}")
def update_post(id:int,Post:Post):
    cursor.execute("""UPDATE posts SET title = %s,content=%s,published=%s WHERE id =%s RETURNING *""",(Post.title,Post.content,Post.published,(str(id))))
    update=cursor.fetchone()
    conn.commit()
    if not update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    return {"Post_Details": update}
    



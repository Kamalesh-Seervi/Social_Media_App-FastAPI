from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from database import engine
import models
from routers import post,user,auth

models.base.metadata.create_all(bind=engine)



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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") 
def read_root():
    return {"message": "hello folks"}


from typing import Union
from fastapi import FastAPI , Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

# storing data


my_posts = [{"title": "title of of post 1", "content": "content of the post", "id": 1}, {
    "title": "favorite foods", "content": "i like pizza", "id": 2
}]


@app.get("/")  # path
def read_root():
    return {"message": "hello folks"}


@app.get("/posts")
def read_posts():
    return {"message": my_posts}

# access based on each property
# fix a datatype so now you get a bug if specified datatype not followed


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def createpost(Post: Post):
    post_dict= Post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"message": "data posted"}


@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    if ['id'] >=3:
        response.status_code = 404
    return {"Post_Details": f"Here is post {id}"}


# title str, content str

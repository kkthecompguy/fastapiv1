from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = 0


post_list = [
  {"id": 1, "title": "Title of post one", "content": "Content of post one", "published": True, "rating": 5},
  {"id": 2,"title": "Title of post two", "content": "Content of post two", "published": True, "rating": 6}
]

def find_post(id):
  for p in post_list:
    if p['id'] == id:
      return p

def find_index_post(id):
  for i, p in enumerate(post_list):
    if p['id'] == id:
      return i


@app.get('/')
async def root():
  return {'message': 'welcome to api creation with fastapi'}


@app.get('/posts')
async def get_posts():
  return {'data': post_list}


@app.post('/posts/create', status_code=status.HTTP_201_CREATED)
async def create_post(payload: Post):
  post = payload.dict()
  post['id'] = len(post_list) + 1
  post_list.append(post)
  return {'message': payload}


@app.get('/posts/latest')
async def latest_post():
  post = post_list[len(post_list) -1]
  return {'data': post}
  

@app.get('/posts/detail/{id}')
async def get_post(id: int):
  post = find_post(id)
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
  return {'data': post}


@app.delete('/posts/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
  post_list.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/edit/{id}')
async def update_post(id: int, payload: Post):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
  post_dict = payload.dict()
  post_dict['id'] = id
  post_list[index] = post_dict
  return {'data': post_dict}
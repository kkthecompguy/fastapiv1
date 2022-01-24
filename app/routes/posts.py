from typing import Optional
from fastapi import HTTPException, status, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import schemas, models, oauth2
from app.database import get_db


router = APIRouter(
    prefix="/api/v1/posts",
    tags=['Posts']
)


@router.get('/', response_model=schemas.ListPostResponse)
async def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
  # cursor.execute(""" select * from posts; """)
  # posts = cursor.fetchall()
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

  posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  return {'data': posts}


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
  # cursor.execute(""" insert into posts (title, content, published) values(%s, %s, %s) returning * """, (payload.title, payload.content, payload.published))
  # new_post = cursor.fetchone()
  # conn.commit() 
  new_post = models.Post(owner_id=current_user.id, **payload.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return {'message': 'post created successfully'}


@router.get('/latest', response_model=schemas.PostResponse)
async def latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" select * from posts order by id desc limit 1; """)
  # post = cursor.fetchone()
  # post = db.query(models.Post).order_by(-models.Post.id).first()

  post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(-models.Post.id).first()
  return {'data': post}
  

@router.get('/detail/{id}', response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
  # cursor.execute(""" select * from posts where id = %s """, (str(id),))
  # post = cursor.fetchone()
  # post = db.query(models.Post).filter(models.Post.id == id).first()

  post = db.query(models.Post
  , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

  return {'data': post}


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute("""delete from posts where id = %s returning * """, (str(id),))
  # deleted_post = cursor.fetchone()
  # conn.commit()
  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

  if post.first().owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")  

  post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/edit/{id}', response_model=schemas.PostResponse)
async def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
  # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """, (payload.title, payload.content, payload.published, str(id)))
  # post = cursor.fetchone()
  # conn.commit()
  post = db.query(models.Post).filter(models.Post.id == id)
  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

  if post.first().owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 

  post.update(payload.dict(), synchronize_session=False)
  db.commit()
  return {'data': post.first()}
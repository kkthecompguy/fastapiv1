from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from app import schemas, oauth2, models, database


router = APIRouter(
  prefix="/api/v1/vote",
  tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):

  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")

  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
  found_vote = vote_query.first()
  if vote.direction == 1:
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user has already voted")
    
    new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
    db.add(new_vote)
    db.commit()
    return {"success": True, "code": status.HTTP_201_CREATED, "message": "successfully added vote"} 
  else:
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist or has been deleted")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"success": True, "code": status.HTTP_204_NO_CONTENT, "message": "successfully deleted vote"}



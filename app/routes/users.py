from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app import models
from app import utils
from app.database import get_db

router = APIRouter(
    prefix="/api/v1/users",
    tags=['Users']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.UserCreate, db:Session = Depends(get_db)):
  payload.password = utils.hash(payload.password)
  new_user = models.User(**payload.dict())

  user_exist = db.query(models.User).filter(models.User.email==payload.email).first()
  if user_exist:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with email already exists")
    
  try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'user created successfully'}
  except Exception as e:
    print(e)
    return {'message': "internal server error"}
    


@router.get('/detail/{id}', response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")

  return {'success': True, 'code': status.HTTP_200_OK, 'data': user}  

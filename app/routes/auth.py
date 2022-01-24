from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import oauth2
from app.database import get_db
from app import schemas, models, utils, oauth2

router = APIRouter(
    prefix="/api/v1/auth",
    tags=['Auth']
)


@router.post('/login')
async def login(user_credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    payload = {
        "user_id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }
    access_token = oauth2.create_access_token(data={"user_id": user.id})    

    return {"success": True, "code": status.HTTP_200_OK, "access_token": access_token, "token_type": "bearer", "user": payload}    
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from ..utils import verify, hash
from .. import OAuth2


router = APIRouter(
    prefix="/login"
)

@router.post("/", response_model=schemas.Token)
def userLogin(credential: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with {credential.username} email does not found.")
    if not verify(credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"password, email does not match.")
    # Create JWT Token
    access_token = OAuth2.create_access_token(data = {"user_id": user.user_id})
    return {"access_token" : access_token, "token_type" : "bearer"}


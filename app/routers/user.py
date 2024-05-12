from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from ..utils import verify, hash
from .. import OAuth2


router = APIRouter(
    prefix="/users",
    tags = ["users"]

)


@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    query = db.query(models.User) 
    users = query.all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No any users created found.")

    return users 


@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_users(id: int, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.user_id==id)
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No any found with id = {id}.")

    return user 



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def createUser(User: schemas.GetUser, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == User.email).first()
    
    if query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {User.email} already exists.")

    hashed_password = hash(User.password)
    User.password = hashed_password
    user = models.User(**User.dict())
    db.add(user)
    db.commit()
    db.refresh(user) 
    return user


@router.put("/{id}", response_model=schemas.User)
def update_user(id:int, currentUser:schemas.GetUser, db: Session= Depends(get_db), get_user: int=Depends(OAuth2.get_current_user)):
    query = db.query(models.User).filter(models.User.user_id==id)
    
    db_user = query.first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} id doesnot exists.")
    
    if  get_user.user_id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You doesnot have to change other user account's that has id {id}, where as your account id is {get_user.user_id}")
    
    user_with_same_email = db.query(models.User).filter(models.User.email == currentUser.email).first()
    if user_with_same_email and user_with_same_email.user_id != get_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with same email {user_with_same_email.email} exists, please use different email.")

    hased_password = hash(currentUser.password)

    currentUser = currentUser.dict()
    currentUser["password"] = hased_password
    currentUser['user_id'] = id
    user = models.User(**currentUser)
    db.delete(db_user) 
    db.add(user)
    db.commit()
    return query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id:int, db: Session=Depends(get_db), get_user: int = Depends(OAuth2.get_current_user)):
    post = db.query(models.User).filter(models.User.user_id == id).first()

    if get_user.user_id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with id {get_user.user_id} doesnot have rights to delete other user with id {id}.")


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} id doesnot exists.")
 
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

  
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import OAuth2

router = APIRouter(
    prefix="/votes",
    tags = ["votes"]
)

@router.post("/", response_model=schemas.Vote)
def votes(input: schemas.TakeVote, db: Session=Depends(get_db),get_user: int=Depends(OAuth2.get_current_user)):
    user_id = get_user.user_id
    post_id = input.post_id
    dir = input.dir
    # print(user_id, post_id, dir)

# cheking if the post exist in post table or not?
    post =db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found.")

# checking if post id and user id exists in vote table or not?
    post = db.query(models.Vote).filter(models.Vote.post_id == post_id , models.Vote.user_id == user_id).first()
    if post and dir == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You cannot vote twice.")
    elif post and dir == 0:
        db.delete(post)    
        db.commit()
        return {"data": "Your vote has been removed to the post."}
    elif not post and dir == 1:
        post = models.Vote(post_id = post_id, user_id = user_id)
        db.add(post)
        db.commit()
        return {"data": "Your voted has been added up." }
    elif not post and dir == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You cannot unvote first.")


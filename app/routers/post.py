from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import OAuth2
from sqlalchemy import func
from typing import Optional


router = APIRouter(
    prefix="/posts", 
    tags = ["posts"]
)


@router.get("", response_model= List[schemas.Postwithvote])
# @router.get("")
def get_posts(db: Session = Depends(get_db), get_user: int=Depends(OAuth2.get_current_user), limit: int =10, skip: int = 0, search: Optional[str]= ""):
    # return(all_posts)  

    # cursor.execute("""SELECT * FROM posts""") 
    # posts = cursor.fetchall()  
    # return(posts)
# query paramters .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post, models.Vote).outerjoin(models.Vote).COUNT(models.Vote.user_id).filter(models.Post.id == models.Vote.post_id).Groupby(models.Post.id)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts)
    return posts

@router.get("/myposts", response_model= List[schemas.Postwithvote])
def get_posts(db: Session = Depends(get_db), get_user: int=Depends(OAuth2.get_current_user)): 
    # return(all_posts)  

    # cursor.execute("""SELECT * FROM posts""") 
    # posts = cursor.fetchall() 
    # return(posts)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).filter(models.Post.owner_id == get_user.user_id).group_by(models.Post.id).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == get_user.user_id).all()
    return posts 

@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post) 
def createPost(newPost : schemas.PostCreate, db: Session = Depends(get_db), get_user: int=Depends(OAuth2.get_current_user)):
    # newPost_dict = newPost.dict()
    # all_posts.append(newPost_dict)
    # return {"data": all_posts}

    # cursor.execute(""" INSERT INTO posts (title, author) VALUES (%s, %s) RETURNING * """, (newPost.title, newPost.author))
    # post = cursor.fetchall()
    # conn.commit()
    # print(post)  
    # return(post) 
    # print(user_id)
    user = db.query(models.User).filter(models.User.user_id == get_user.user_id).first()
    # print (get_user.user_id)
    # print(user.email)
    # print(user.password) 
    # print(user)
    post = models.Post(**newPost.dict(),owner_id= get_user.user_id) 
    db.add(post)  
    db.commit() 
    db.refresh(post)
    return post


 
@router.get("/{id}", response_model=schemas.Postwithvote)
def get_post(id: int, db: Session = Depends(get_db),get_user: int=Depends(OAuth2.get_current_user)):
#     post = get_post_by_id(id)  
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} id not found.")
#     return{f"post with id {id}": post} 



    # cursor.execute(""" SELECT * FROM posts WHERE id = (%s)""", (id))
    # post = cursor.fetchone()
    # return(post) 
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).filter(models.Post.id==id).group_by(models.Post.id).first()

    # post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} id doesnot exists.")
    
    if post.Post.owner_id != get_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not the creator of this post with {id} id")
    # print(post.Post.owner_id)
    return post
 
    
# @app.get("/posts/latest")
# If you want the latest one post then this should be above the @app.get("/posts/{id}") as it throws error cause id is expecting int and latest is antoher path paramenet in this api

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session = Depends(get_db), get_user: int=Depends(OAuth2.get_current_user)): 
    # post = get_post_by_id(id)
    # if post in all_posts:
    #     all_posts.remove(post)
    #     return Response(status_code=status.HTTP_204_NO_CONTENT) 
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} id not found so could not delete.")


#     cursor.execute(""" DELETE FROM posts WHERE id = (%s) RETURNING * """,(str(id)))
#     post = cursor.fetchone()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found with id {id}")
#     conn.commit()
#     raise HTTPException(status_code=status.HTTP_200_OK, detail=f"post with {id} id has been deleted succesffuly")
    
# def get_post_by_id(id): 
#     for post in all_posts:
#         if post["id"] == id: 
#             return(post)
#     else:
#         return None


    post = db.query(models.Post).filter(models.Post.id == id).first()
    # if not post:
    # if post is None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.owner_id != get_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not the creator of this post with {id} id")
    
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



    # post_query = db.query(models.Post).filter(models.Post.id == id)
    # if post_query.first() == None:
    #     print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} id doesnot exists..")
    

    # post_query.delete(synchronize_session=False)
    # db.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


 
     
@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Postwithvote) 
def update_post(id: int, newPost : schemas.UpdatePost, db: Session = Depends(get_db), get_user: int=Depends(OAuth2.get_current_user)): 
    # post = get_post_by_id(id)
    # if post != None:
    #     newPost_dict = newPost.dict()
    #     newPost_dict["id"] = id 
    #     all_posts.remove(post)
    #     all_posts.append(newPost_dict)
    #     return{f"Post has been succesffuly replace as a whole new post with all attributes and same id {id}."}
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} id doesnot exists.")


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} id doesnot exists.")

    if post.owner_id != get_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not the creator of this post with {id} id")
    
    post_query.update(newPost.dict(), synchronize_session=False)
    db.commit()

    post = post_query.first() 
    id = post.id

    # //getting postID and using same path operations query of posts//{id}
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).filter(models.Post.id==id).group_by(models.Post.id).first()
    return post
 
    # newPost_dict = newPost.dict()
    # newPost_dict["id"] = str(id)
    # newPost = models.Post(**newPost_dict)
    # db.delete(post)
    # db.commit()
    # db.add(newPost)
    # db.commit()
    # db.refresh(newPost) 
    # return newPost
 
      
from fastapi import FastAPI,status, HTTPException, Response, Depends
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .utils import hash, verify
from . import OAuth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .routers import auth, post, user, vote
from fastapi.middleware.cors import CORSMiddleware



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
 
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# class Post(BaseModel): 
#     title: str
#     author: str 
#     rating: Optional[int]= None 
 
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi2', user='postgres', password='Maharzan@123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB succesfully connected")   
        break
    except Exception as error:
        print("DB Connection failed")    
        print(f"Error was {error}")
        time.sleep(2)

# all_posts = [{"title": "POST1", "author":"Author1", "id": 1},{"title": "POST2", "author":"Author2", "id": 2}]


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
 
@app.get("/")
def root():
    return {"message": "Welcome to fastapi2"} 
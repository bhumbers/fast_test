from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from backend import models, schemas
from backend.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = models.User(username=user.username, email=user.email, hashed_password=user.password) # In real app, hash the password
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, owner_id: int, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == owner_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_post = models.Post(image_url=post.image_url, caption=post.caption, owner_id=owner_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    return db_post

@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, post_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        # Check if post exists
        post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_comment = models.Comment(text=comment.text, post_id=post_id, user_id=user_id)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    return db_comment

@app.get("/posts/{post_id}/comments/", response_model=List[schemas.Comment])
def read_post_comments(post_id: int, limit: int = None, db: Session = Depends(get_db)):
    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    query = db.query(models.Comment).filter(models.Comment.post_id == post_id).order_by(models.Comment.created_at.desc())
    if limit:
        query = query.limit(limit)
    
    comments = query.all()
    return comments

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Instagram Clone!"}

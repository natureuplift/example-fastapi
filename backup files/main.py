from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
# from starlette.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# root path
@app.get("/")
def root():
    return {"message": "Welcome to my API!"}

# # test route for sqlalchemy
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

# Read Posts
# to input argument which gives us access into our DB object to make queries and changes to DB, use -> db: Session = Depends(get_db)
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""") # dire
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # return {"data": posts}
    # FastAPI automatically serialize and convert it into Json
    return posts

# Create Post
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # save it to DB
# instead of adding attributes from model (title=post.title, content=post.content, published=post.published), we can use post.dict for dictionary and unpack dictionary with '**'
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get One Post
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, [str(id)])
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with  id: {id} was not found")
    return post

# Delete Post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [str(id)])
    # deleted_post = cursor.fetchone()
    # conn.commit() # save it to DB
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit() # save it to DB
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()

    return post_query.first()

# post used to test without DB 
# my_posts = [{"title": "title of post 1", "content":"content of post 1", "id":1},{"title": "favorite foods","content":"I like pizza", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# function to post id
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 1000000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}

# @app.get("/posts/{id}")
# def get_post(id: int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with  id: {id} was not found")
#     return {"post_detail": post}

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     #deleting post
#     #find the index in the array that has required ID
#     #my_post.pop(index)
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
#     my_posts.pop(index)
#     # return {'message': 'post was successfuly deleted'}
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     print(post)
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {"data": post_dict}
    
# @app.post("/posts")
# def create_posts(post: Post):
#     print(post)
#     print(post.dict())
#     return {"data": post}

# @app.get("/posts")
# def create_posts():
#     return {"data": "This is our post!"}

# @app.post("/posts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"post": f"title {payload['title']} content: {payload['content']}"}

# @app.post("/posts")
# def create_posts(new_post: Post):
#     print(new_post.published)
#     return {"data": "new post"}
# # we expect: title str, content str (category, Bool published)
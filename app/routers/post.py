from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db, Session
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix = '/posts',
    tags=["Posts"]
)


# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).all()
#     print(posts)
#     return posts


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, 
              search: Optional[str] = ""
              ):
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)\
                .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #print(type(results), "\n", results)

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} was not found" 
        )
    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    print("post query result:", post_query.first())

    return post_query.first()
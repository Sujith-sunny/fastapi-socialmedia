from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import model, schemas, utils
from .import oauth2
from .. database import get_db
from typing import Optional

router = APIRouter()

@router.get("/allposts", response_model=list[schemas.PostResponse])    # This function gets triggered once the API is called from postman, cusor executes the SQL commands and get the DB info, message in return is displayed in the outcome for API
def get_user_data(db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # all_posts = db.query(model.Post).order_by(model.Post.id_number.asc()).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(model.Post, func.count(model.votes.post_id).label("votes")).join(model.votes, model.Post.id_number == model.votes.post_id, isouter=True).group_by(model.Post.id_number).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_user(new_post: schemas.PostBase, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    print(current_user_email.email)
    new_post = model.Post(owner_email=current_user_email.email, **new_post.dict()) #**new_post.dict() converts the dictionary into a keyword argument
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}", response_model=schemas.PostResponse)        #{id} is a path parameter, path parameter comes in as string, we need the int
def get_post(id : int, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):          #id is converted into int to get the right post from the DB
    #print(current_user_email.email)
    # single_post = db.query(model.Post).filter(model.Post.id_number == id).first()
    single_post = db.query(model.Post, func.count(model.votes.post_id).label("votes")).join(model.votes, model.Post.id_number == model.votes.post_id, isouter=True).where(model.Post.id_number == id).group_by(model.Post.id_number).first()
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    return single_post
             

@router.delete("/deleteposts/{id}")
def delete_post(id:int, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    delete_post = db.query(model.Post).filter(model.Post.id_number == id)

    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    
    if delete_post.first().owner_email != current_user_email.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized user to perform this action")
    
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  #For delete operations we wont be sending any message back
    #return {"message" : 'Post deleted successfully'}


#update a post - PUT 
@router.put("/updateposts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.GetPostResponse)
def update_post(id:int, post:schemas.PostBase, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    updated_post = db.query(model.Post).filter(model.Post.id_number == id)
    
    if updated_post.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()


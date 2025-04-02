from .. import model, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from . import oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #print(current_user.email)# this will print the email of the user who is making the request

    #hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = model.users(**user.dict()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#Get All Users
@router.get("/", response_model=list[schemas.GetUserResponse])
def get_user(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    user = db.query(model.users).order_by(model.users.id_number.asc()).all()
    return user


#Get User by ID
@router.get("/{id}", response_model=schemas.GetUserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    user = db.query(model.users).filter(model.users.id_number == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found")
    return user
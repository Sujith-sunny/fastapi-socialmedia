from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. import schemas, database, model
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


"""
    The above functions are used for creating and verifying access tokens in a Python application using
    JWT authentication.
    
    :param data: The `data` parameter in the `create_access_token` function is a dictionary containing
    the data that will be encoded into the access token. This data typically includes information about
    the user or client for whom the token is being generated
    :type data: dict
    :return: The `get_current_user` function is returning the result of calling the `verify_token`
    function with the `token` parameter and `credentials_exception` as arguments.
"""


def create_access_token(data: dict):
    to_encode = data.copy()    #This is a dictionary
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("user_email")
        id: str = payload.get("user_id")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_token(token, credentials_exception)
    user_email = db.query(model.users).filter(model.users.email == token.email).first()

    return user_email
#Every model represents a table in our database. 

from .database import Base_model
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base_model):
    __tablename__ = "socialmediaposts"

    #Creating coloums
    id_number = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("now()"))
    owner_email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)  #This is a foreign key
    #Setting up a relation with the users table
    owner = relationship("users")  #This is a relationship with the User model

class users(Base_model):
    __tablename__ = "users"

    #Creating coloums
    id_number = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("now()"))



class votes(Base_model):
    __tablename__ = "votes"

    #Creating coloums
    post_id = Column(Integer, ForeignKey("socialmediaposts.id_number", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id_number", ondelete="CASCADE"), primary_key=True)
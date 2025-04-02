from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor #Used for SQL statements
from .config import settings


#Connection the DB
SqlAlchemy_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
Sql_Engine = create_engine(SqlAlchemy_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Sql_Engine)   #A session helps us to connect to the DB
Base_model = declarative_base()#Base is the base class for all our models. All the models are based on this.

#Dependency Injection 
def get_db():
    """
    The function `get_db` returns a database session that is closed after its use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Connection to the Database using psycopg2
# The code snippet `connection = psycopg2.connect(user="postgres", password="sunny1306",
# host="localhost", database="fastapi", cursor_factory=RealDictCursor)` is establishing a connection
# to a PostgreSQL database named "fastapi" running on the local host with the usernam & password.
# The `cursor_factory=RealDictCursor` parameter specifies that the cursor should
# return rows as dictionaries rather than lists.

# try:
#     connection = psycopg2.connect(user="postgres", password="sunny1306", host="localhost", database="fastapi", cursor_factory=RealDictCursor)
#     cursor = connection.cursor() #The one that helps for the SQL Statements
#     print('Database connection was successful')
# except Exception as error:
#     print("Connection to database failed")
#     print("Error: ", error)
from passlib.context import CryptContext


# This line creates a password context object using the `CryptContext` class from the `passlib.context` module. This
# password context is used to hash and verify passwords in the application.
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt", deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


def verifying(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password, scheme="bcrypt") 
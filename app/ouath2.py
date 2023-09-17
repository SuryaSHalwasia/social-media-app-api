from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import database, models
from sqlalchemy.orm import Session
from config import settings
#SECRET_KEY (random you put)
#Algorithm HS256
#Expiration time of token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #route for login

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGO
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id:int = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED,
                                          "Could not validate credentials", 
                                          {"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    print(user)
    return user
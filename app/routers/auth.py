from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from schemas import userLogin, Token
import utils
import ouath2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models import User
router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    #username and password fields in dictionary is returned by OAuth2Password
    user = db.query(User).filter(User.email == credentials.username).first()
    
    if(user == None):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "PInvalid credentials")
    
    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid credentials")
    
    #create the token
    access_token = ouath2.create_access_token(data = {"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}






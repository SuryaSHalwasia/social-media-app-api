from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
import models
from database import get_db
from sqlalchemy.orm import Session
from schemas import userCreate, userOut

import utils

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=userOut)
def create_user(user:userCreate, db:Session = Depends(get_db)):

    user.password  = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#get user by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=userOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if(user != None):
        return user
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User with id {} not found".format(id))

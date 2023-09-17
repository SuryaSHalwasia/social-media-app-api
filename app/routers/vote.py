from fastapi import Depends, Response, HTTPException, status, APIRouter
from typing import List, Optional
import models
from database import get_db
from sqlalchemy.orm import Session
from schemas import Vote
import ouath2

router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:Vote, db:Session=Depends(get_db), user:int = Depends(ouath2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if(not post):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post with id {} not found".format(vote.post_id))
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, 
                                      models.Votes.user_id == user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        #create a vote
        if(found_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User {} has already voted".format(user.id))
        new_vote = models.Votes(user_id = user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"Sucessfully added vote"}
    else:
        #delete a vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User {} has not voted".format(user.id))
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Sucessfully removed vote"}


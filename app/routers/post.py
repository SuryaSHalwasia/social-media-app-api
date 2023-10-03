from fastapi import Depends, Response, HTTPException, status, APIRouter
from typing import List, Optional
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import postCreate, Post, postOut
import app.ouath2 as ouath2
from sqlalchemy import func
from pydantic import parse_obj_as

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[postOut])
def get_posts(db: Session = Depends(get_db), limit:int = 10, skip:int = 0,
               search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    votes = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, 
                                       isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
    votes = list(map(lambda x: x._mapping, votes))
    return votes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(new_post : postCreate, db : Session = Depends(get_db), 
                 user: int = Depends(ouath2.get_current_user)):
    
    #new_post = new_post.dict()
    #cur.execute("INSERT INTO posts(title,body,published) VALUES(%s,%s,%s) RETURNING *",
    #           (new_post['title'], new_post['body'], new_post["published"]))
    #post = cur.fetchone()
    #conn.commit()
    post = models.Post(user_id = user.id, **new_post.dict()) 
    db.add(post)

    db.commit()
    db.refresh(post)

    return post

@router.get("/{id}", response_model=postOut)
def get_post(id:int, response:Response, db : Session = Depends(get_db), user: int = Depends(ouath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #cur.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    #post = cur.fetchone()
    votes = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).filter(models.Post.id == id).join(models.Votes, models.Votes.post_id == models.Post.id, 
                                       isouter=True).group_by(models.Post.id).first()

    

    if(votes!=None):
        
        #votes = list(map(lambda x: x._mapping, votes))
        return votes
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post with id {} not found".format(id))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, response:Response, db : Session = Depends(get_db), 
                 user: int = Depends(ouath2.get_current_user)):
    #cur.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    #post = cur.fetchone()
    #conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if(post.first() == None):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            "Post with id {} not found".format(id))
    elif(post.first().user_id != user.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Not authorized to perform requested action")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def update_post(new_post:postCreate, id:int, response:Response, db : Session = Depends(get_db), 
                 user: int = Depends(ouath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    #new_post = new_post.dict()
    #cur.execute("UPDATE posts SET title = %s, body = %s, published = %s WHERE id = %s RETURNING *",
    #            (new_post.title, new_post.body, new_post.published, str(id, )))
    #post = cur.fetchone()
    #conn.commit()
    if(post.first() == None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Post with id {} not found".format(id))
    elif(post.first().user_id != user.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,"Not authorized to perform requested action")
    else:
        post.update({'title':new_post.title, 'body':new_post.body},
                             synchronize_session=False)
        db.commit()
        return post.first()   

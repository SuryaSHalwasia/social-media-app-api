from fastapi import FastAPI
import models
from database import engine
from routers import user, post, auth, vote
from config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#models.Base.metadata.create_all(bind=engine)

@app.get("/") 
def get_user():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
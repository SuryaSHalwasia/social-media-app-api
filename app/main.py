from fastapi import FastAPI
import sys
import os

# Get the parent directory of the current script (tests directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python path
sys.path.append(parent_dir)



from app.database import engine
from app.routers import user, post, auth, vote
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

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
    return {"message": "Hello World!"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from . import routes
from .context import db_engine

app = FastAPI(
    dependencies=[
        Depends(db_engine)
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://story.imaginer.ai",
        "https://dev-story.imaginer.ai",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.root)

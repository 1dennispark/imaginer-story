import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

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

if os.path.exists('./website/build'):
    static_files = StaticFiles(directory="./website/build", html=True)

    @app.get("/character")
    def character():
        return FileResponse("./website/build/index.html")

    @app.get("/synopsis")
    def synopsis():
        return FileResponse("./website/build/index.html")

    app.mount("/", static_files, name="static")

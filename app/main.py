from fastapi import FastAPI
from app.routers import samplepaperAPI

app = FastAPI()


app.include_router(samplepaperAPI.router)

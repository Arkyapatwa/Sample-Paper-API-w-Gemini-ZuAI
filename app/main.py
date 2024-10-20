from fastapi import FastAPI
from app.routers import samplepaperAPI, extractSamplePaperAPI
from app.internal import extractSamplePaper

app = FastAPI()


app.include_router(samplepaperAPI.router)
app.include_router(extractSamplePaperAPI.router)

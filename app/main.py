from fastapi import FastAPI
from app.routers import samplepaperAPI, extractSamplePaperAPI
from redis import Redis
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host="localhost", port=6379)
    yield
    app.state.redis.close()

app = FastAPI(lifespan=lifespan)


app.include_router(samplepaperAPI.router)
app.include_router(extractSamplePaperAPI.router)

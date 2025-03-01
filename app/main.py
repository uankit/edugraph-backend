from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload
from app.routes import graph

origins = [
    "http://localhost:5173",
]

app = FastAPI(
    title="EduGraph API",
    description="API for EduGraph - an intelligent learning platform that extracts and organizes study materials into a knowledge graph.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(graph.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to EduGraph API!"}
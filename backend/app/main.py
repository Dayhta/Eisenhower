"""FastAPI application entrypoint (clean UTF-8, regenerated)."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import tasks, config

# Ensure tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Eisenhower Matrix Todo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api")
app.include_router(config.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Eisenhower Matrix Todo API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

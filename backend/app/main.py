"""FastAPI application entrypoint with MongoDB-only persistence, JWT auth, refresh tokens, and advanced scoring config."""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pymongo.errors import PyMongoError

from .routers import auth, mongo_tasks, config
from .logging_mw import LoggingMiddleware
from .rate_limit import api_limiter
from .admin import ensure_admin_user
from .mongo import get_db

ENV = os.getenv("ENVIRONMENT", "development")
allowed_origins = ["http://localhost:3000"] if ENV == "production" else ["http://localhost:3000", "*"]

app = FastAPI(
    title="Eisenhower Matrix Todo API",
    version="3.0.0",
    description="Mongo-backed Eisenhower matrix with multifactor scoring, JWT auth, refresh tokens, category weighting, runtime config.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def global_rate_limit(request: Request, call_next):
    if request.url.path.startswith("/api/") and not request.url.path.startswith("/api/auth"):
        api_limiter(request)
    return await call_next(request)

app.include_router(auth.router, prefix="/api")
app.include_router(mongo_tasks.router, prefix="/api")
app.include_router(config.router, prefix="/api")

@app.on_event("startup")
async def startup():  # pragma: no cover
    ensure_admin_user()
    try:
        get_db().command("ping")
    except PyMongoError as e:
        raise RuntimeError(f"MongoDB connectivity failed: {e}")

@app.get("/")
def root():
    return {"message": "Eisenhower Matrix Todo API", "version": "3.0.0", "storage": "mongo"}

@app.get("/health")
def health():
    try:
        get_db().command("ping")
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=503, detail="database_unreachable")

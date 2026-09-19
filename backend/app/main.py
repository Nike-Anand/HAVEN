"""HAVEN FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config, db
from .routers import auth, contacts, legal, settings, sos, stegano, sync, therapy


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    title="HAVEN — Women's Safety & Support Platform",
    version="1.0.0",
    description=(
        "AI-powered safety platform: discreet SOS, crisis therapy bot, legal "
        "guidance (Indian women's rights), and emergency contact coordination."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock down to the app's domain in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sos.router)
app.include_router(therapy.router)
app.include_router(contacts.router)
app.include_router(legal.router)
app.include_router(settings.router)
app.include_router(sync.router)
app.include_router(stegano.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "haven", "version": "1.0.0"}


@app.get("/")
def root():
    return {
        "service": "HAVEN API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0",
    }
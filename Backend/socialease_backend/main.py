from fastapi import FastAPI
from database import engine, Base
from routers import settings, progress

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(settings.router, prefix="/api", tags=["Settings"])
app.include_router(progress.router, prefix="/api", tags=["Progress"])

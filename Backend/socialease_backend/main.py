import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from socialease_backend.database import db  # Use absolute import
from socialease_backend.routers import settings, progress, notifications  # Use absolute import

app = FastAPI()

# Include routers
app.include_router(settings.router, prefix="/api", tags=["Settings"])
app.include_router(progress.router, prefix="/api", tags=["Progress"])  # Ensure this is included
app.include_router(notifications.router, prefix="/api", tags=["Notifications"])  # Added notifications router

from fastapi import FastAPI
from app.routes import community, auth
from app.database import create_tables  # Corrected import statement

app = FastAPI(title="Social Ease Community API")

# Create tables on startup
@app.on_event("startup")
def startup():
    create_tables()

# Include routes
app.include_router(auth.router)
app.include_router(community.router)

@app.get("/")
def home():
    return {"message": "Welcome to Social Ease Community Page API"}

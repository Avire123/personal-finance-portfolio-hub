from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.endpoints import router as api_router

# Create DB tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Finance & Investment Portfolio Hub",
    description="Backend API for tracking assets, live market prices, and expense targets.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Personal Finance API is running. Visit /docs for interactive Swagger API documentation."}

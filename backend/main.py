from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config
from routes import environment, submission, config as config_routes, updates, history, debug, models

app = FastAPI(
    title="ML Model Builder Environment",
    description="Backend orchestration service for ML Model Builder",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(environment.router)
app.include_router(submission.router)
app.include_router(config_routes.router)
app.include_router(updates.router)
app.include_router(history.router)
app.include_router(debug.router)
app.include_router(models.router)

@app.get("/health")
async def health_check():
    """Health check endpoint to verify service status"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "config_loaded": config.get().github is not None
    }

@app.on_event("startup")
async def startup_event():
    print("Starting ML Model Builder Backend...")
    if not config.get().github:
        print("WARNING: GitHub configuration not found. Submissions will fail.")
    else:
        print("Configuration loaded successfully.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

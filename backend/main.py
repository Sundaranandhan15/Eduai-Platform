import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth_router, predict, submit, progress, chat

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduAI Backend",
    description="Backend API for EduAI Adaptive Knowledge Tracing & AI Tutoring Platform",
    version="1.0.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router.router)
app.include_router(predict.router)
app.include_router(submit.router)
app.include_router(progress.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to EduAI API!"}

if __name__ == "__main__":
    import uvicorn
    # Use port 8000 (wait, Triton uses 8000 for HTTP. We should use 8080 for backend)
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

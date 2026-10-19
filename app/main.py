import os

from fastapi import FastAPI

app = FastAPI(title="Cloud Build POC")

# dummy
@app.get("/")
def home():
    """Single endpoint used for the Cloud Build demo."""
    return {
        "message": "Hello from Cloud Build POC",
        "version": os.getenv("APP_VERSION", "v1"),
        "build": os.getenv("BUILD_ID", "local"),
    }

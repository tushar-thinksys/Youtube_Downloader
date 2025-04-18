from fastapi import Header, HTTPException, status
import os

API_KEY = os.getenv("API_KEY", "password123")  # fallback if .env not used
API_KEY_NAME = "X-API-Key"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

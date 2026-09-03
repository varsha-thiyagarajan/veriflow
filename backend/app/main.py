from fastapi.middleware.cors import CORSMiddleware

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.verification_pipeline import run_text_verification_pipeline


app = FastAPI(
    title="VeriFlow AI",
    description="AI output verification API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VerificationRequest(BaseModel):
    content: str


@app.get("/health")
def health() -> Dict[str, str]:
    return {
        "status": "ok",
        "service": "veriflow-ai",
    }


@app.post("/api/verify")
def verify(request: VerificationRequest) -> Dict[str, Any]:
    if not request.content.strip():
        raise HTTPException(
            status_code=400,
            detail="Content cannot be empty.",
        )

    try:
        return run_text_verification_pipeline(
            content=request.content,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
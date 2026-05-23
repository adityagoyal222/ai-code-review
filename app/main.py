from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import get_settings
from app.rag.ingest import run_ingest
from app.rag.review import review_code

app = FastAPI(title="AI Code Review Assistant")
settings = get_settings()

app.mount("/static", StaticFiles(directory="app/ui"), name="static")


class ReviewRequest(BaseModel):
    code: str
    language: Optional[str] = None
    file_path: Optional[str] = None


class ReviewResponse(BaseModel):
    review: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse("app/ui/index.html")


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.post("/ingest")
def ingest(reset: bool = False) -> JSONResponse:
    result = run_ingest(settings, reset=reset)
    return JSONResponse(result)


@app.post("/review", response_model=ReviewResponse)
def review(request: ReviewRequest) -> ReviewResponse:
    review_text = review_code(
        settings,
        code=request.code,
        language=request.language,
        file_path=request.file_path,
    )
    return ReviewResponse(review=review_text)

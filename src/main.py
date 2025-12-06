from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.api.v1.routes import router as api_router

app = FastAPI(title="FastAPI Starter")

app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
        }
    )
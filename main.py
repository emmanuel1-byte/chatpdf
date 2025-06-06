from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.chat_pdf_api_service import rag, authentication
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app = FastAPI(
    title="ChatPDF API",
    summary=" A powerful API for uploading PDF documents and interacting with their content through natural language chat. Supports authentication, real-time communication, and multi-user isolation using vector search and LLMs",
    servers=[
        # {"url": "https://api.kennapartners.com", "description": "Production server"},
        {
            "url": "https://chatpdf-9ih9.onrender.com/",
            "description": "Staging server",
        },
        {"url": "http://127.0.0.1:8000", "description": "Local development server"},
    ],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authentication)
app.include_router(rag)


@app.get("/", tags=["Health"])
def health_check():
    return JSONResponse(content={"message": "API is healthy"}, status_code=200)

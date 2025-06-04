from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.chat_pdf_api_service import rag, authentication

app = FastAPI()

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

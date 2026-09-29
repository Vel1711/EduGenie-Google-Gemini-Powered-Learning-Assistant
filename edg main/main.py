from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.modules.qna import router as qna_router
from app.modules.explanation_module import router as explanation_router
from app.modules.quiz_module import router as quiz_router
from app.modules.summary_module import router as summary_router
from app.modules.learning_path import router as learning_router
from config import settings

app = FastAPI(
    title=settings.app_name,
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(qna_router)
app.include_router(explanation_router)
app.include_router(quiz_router)
app.include_router(summary_router)
app.include_router(learning_router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "explanation_provider": settings.explanation_provider,
    }

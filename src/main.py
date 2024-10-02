from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import settings
from src.delivery.api.routes import router as shortener_url

description = """## Fastapi Microservice Clean Architecture"""

app = FastAPI(
    docs_url=settings.swagger_url,
    version="1.1.0",
    title=settings.app_title,
    description=description,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(shortener_url)

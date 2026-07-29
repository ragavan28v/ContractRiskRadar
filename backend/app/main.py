import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, clauses, contracts, dashboard, rewrite
from .core.config import get_settings
from .core.mongo import init_mongo_indexes


settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    await init_mongo_indexes()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(contracts.router, prefix=settings.API_V1_STR)
app.include_router(clauses.router, prefix=settings.API_V1_STR)
app.include_router(rewrite.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)


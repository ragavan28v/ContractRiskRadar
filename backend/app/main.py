import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.db import Base, engine, SessionLocal
from .api import auth, contracts, clauses, rewrite, dashboard
from .services.contracts_service import sync_sql_to_mongo


settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# open CORS during development; should be restricted in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ensure database schema up-to-date for added columns
from sqlalchemy import text
from .core.db import engine

with engine.connect() as conn:
    # sqlite needs manual ALTER TABLE
    if engine.dialect.name == "sqlite":
        cols = [r[1] for r in conn.execute(text("PRAGMA table_info(contracts)"))]
        if "access_password_hash" not in cols:
            conn.execute(text("ALTER TABLE contracts ADD COLUMN access_password_hash VARCHAR"))
    else:
        conn.execute(text("ALTER TABLE IF NOT EXISTS contracts ADD COLUMN access_password_hash VARCHAR"))

# migrate any existing consented contracts into Mongo during startup
@app.on_event("startup")
async def startup_migrations():
    # add column if missing (redundant but safe)
    with engine.connect() as conn:
        if engine.dialect.name == "sqlite":
            cols = [r[1] for r in conn.execute(text("PRAGMA table_info(contracts)"))]
            if "access_password_hash" not in cols:
                conn.execute(text("ALTER TABLE contracts ADD COLUMN access_password_hash VARCHAR"))
        else:
            conn.execute(text("ALTER TABLE IF NOT EXISTS contracts ADD COLUMN access_password_hash VARCHAR"))

    # perform SQL->Mongo sync using regular session
    session = SessionLocal()
    try:
        await sync_sql_to_mongo(session)
    finally:
        session.close()

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(contracts.router, prefix=settings.API_V1_STR)
app.include_router(clauses.router, prefix=settings.API_V1_STR)
app.include_router(rewrite.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


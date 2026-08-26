from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .database import Base, engine, settings
from .routers import auth, users, social, posts, analytics

Base.metadata.create_all(bind=engine)

def lightweight_migrate():
    # Keeps existing development databases usable after upgrading the starter schema.
    with engine.begin() as conn:
        for statement in [
            "ALTER TABLE posts ADD COLUMN IF NOT EXISTS platform VARCHAR(50) DEFAULT 'Instagram'",
            "ALTER TABLE posts ADD COLUMN IF NOT EXISTS published_at TIMESTAMP NULL",
            "ALTER TABLE posts ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE social_accounts ADD COLUMN IF NOT EXISTS connected BOOLEAN DEFAULT TRUE",
        ]:
            try:
                conn.execute(text(statement))
            except Exception:
                pass

try:
    lightweight_migrate()
except Exception:
    pass

app = FastAPI(title="SocialFlow API", version="2.0", description="Production-style social planning and automation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(social.router)
app.include_router(posts.router)
app.include_router(analytics.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "socialflow-api", "version": "2.0"}

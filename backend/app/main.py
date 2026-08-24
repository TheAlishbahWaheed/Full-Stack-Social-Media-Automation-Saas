from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base,engine,settings
from .routers import auth,users,social,posts
Base.metadata.create_all(bind=engine) # learning-friendly; use Alembic later
app=FastAPI(title="SocialFlow API",version="1.0")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.CORS_ORIGINS.split(",")],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth.router);app.include_router(users.router);app.include_router(social.router);app.include_router(posts.router)
@app.get("/health")
def health(): return {"status":"ok"}

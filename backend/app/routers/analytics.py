from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_user
from ..models import Post, SocialAccount, User
from ..schemas import Analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("", response_model=Analytics)
def analytics(u: User = Depends(current_user), db: Session = Depends(get_db)):
    posts = db.query(Post).filter_by(user_id=u.id).all()
    accounts = db.query(SocialAccount).filter_by(user_id=u.id, connected=True).count()
    upcoming = [p for p in posts if p.status == "scheduled" and p.scheduled_at]
    upcoming.sort(key=lambda p: p.scheduled_at)
    return Analytics(
        total_posts=len(posts),
        drafts=sum(p.status == "draft" for p in posts),
        scheduled=sum(p.status == "scheduled" for p in posts),
        published=sum(p.status == "published" for p in posts),
        connected_accounts=accounts,
        upcoming=upcoming[:5],
    )

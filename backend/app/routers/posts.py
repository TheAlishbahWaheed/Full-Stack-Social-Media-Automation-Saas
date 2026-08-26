from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_user
from ..models import Post, User
from ..schemas import PostCreate, PostUpdate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])

def normalize_status(p: Post):
    if p.status == "published":
        return
    p.status = "scheduled" if p.scheduled_at else "draft"

@router.get("", response_model=list[PostOut])
def all_posts(u: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(Post).filter_by(user_id=u.id).order_by(Post.created_at.desc(), Post.id.desc()).all()

@router.post("", response_model=PostOut)
def add(x: PostCreate, u: User = Depends(current_user), db: Session = Depends(get_db)):
    p = Post(**x.model_dump(), user_id=u.id)
    normalize_status(p)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.put("/{id}", response_model=PostOut)
def update(id: int, x: PostUpdate, u: User = Depends(current_user), db: Session = Depends(get_db)):
    p = db.query(Post).filter_by(id=id, user_id=u.id).first()
    if not p: raise HTTPException(404, "Post not found")
    for k, v in x.model_dump(exclude_unset=True).items():
        if k == "status" and v not in {"draft", "scheduled", "published"}:
            raise HTTPException(400, "Invalid status")
        setattr(p, k, v)
    normalize_status(p)
    db.commit(); db.refresh(p)
    return p

@router.post("/{id}/publish", response_model=PostOut)
def publish(id: int, u: User = Depends(current_user), db: Session = Depends(get_db)):
    p = db.query(Post).filter_by(id=id, user_id=u.id).first()
    if not p: raise HTTPException(404, "Post not found")
    p.status = "published"
    p.published_at = datetime.now(timezone.utc).replace(tzinfo=None)
    p.scheduled_at = None
    db.commit(); db.refresh(p)
    return p

@router.post("/{id}/duplicate", response_model=PostOut)
def duplicate(id: int, u: User = Depends(current_user), db: Session = Depends(get_db)):
    p = db.query(Post).filter_by(id=id, user_id=u.id).first()
    if not p: raise HTTPException(404, "Post not found")
    copy = Post(content=p.content, platform=p.platform, status="draft", user_id=u.id)
    db.add(copy); db.commit(); db.refresh(copy)
    return copy

@router.delete("/{id}")
def delete(id: int, u: User = Depends(current_user), db: Session = Depends(get_db)):
    p = db.query(Post).filter_by(id=id, user_id=u.id).first()
    if not p: raise HTTPException(404, "Post not found")
    db.delete(p); db.commit()
    return {"message": "deleted"}

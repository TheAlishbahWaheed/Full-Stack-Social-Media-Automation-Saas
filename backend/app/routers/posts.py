from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_user
from ..models import User,Post
from ..schemas import PostCreate,PostUpdate,PostOut
router=APIRouter(prefix="/posts",tags=["Posts"])
def status(p): p.status="scheduled" if p.scheduled_at else "draft"
@router.get("",response_model=list[PostOut])
def all(u=Depends(current_user),db:Session=Depends(get_db)): return db.query(Post).filter_by(user_id=u.id).order_by(Post.id.desc()).all()
@router.post("",response_model=PostOut)
def add(x:PostCreate,u=Depends(current_user),db:Session=Depends(get_db)):
    p=Post(**x.model_dump(),user_id=u.id);status(p);db.add(p);db.commit();db.refresh(p);return p
@router.put("/{id}",response_model=PostOut)
def update(id:int,x:PostUpdate,u=Depends(current_user),db:Session=Depends(get_db)):
    p=db.query(Post).filter_by(id=id,user_id=u.id).first()
    if not p: raise HTTPException(404,"Post not found")
    for k,v in x.model_dump(exclude_unset=True).items(): setattr(p,k,v)
    status(p);db.commit();db.refresh(p);return p
@router.delete("/{id}")
def delete(id:int,u=Depends(current_user),db:Session=Depends(get_db)):
    p=db.query(Post).filter_by(id=id,user_id=u.id).first()
    if not p: raise HTTPException(404,"Post not found")
    db.delete(p);db.commit();return {"message":"deleted"}

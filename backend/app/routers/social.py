from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_user
from ..models import User,SocialAccount
from ..schemas import SocialCreate,SocialOut
router=APIRouter(prefix="/social-accounts",tags=["Social Accounts"])
@router.get("",response_model=list[SocialOut])
def all(u=Depends(current_user),db:Session=Depends(get_db)): return db.query(SocialAccount).filter_by(user_id=u.id).all()
@router.post("",response_model=SocialOut)
def add(x:SocialCreate,u=Depends(current_user),db:Session=Depends(get_db)):
    a=SocialAccount(**x.model_dump(),user_id=u.id);db.add(a);db.commit();db.refresh(a);return a
@router.delete("/{id}")
def delete(id:int,u=Depends(current_user),db:Session=Depends(get_db)):
    a=db.query(SocialAccount).filter_by(id=id,user_id=u.id).first()
    if not a: raise HTTPException(404,"Social account not found")
    db.delete(a);db.commit();return {"message":"deleted"}

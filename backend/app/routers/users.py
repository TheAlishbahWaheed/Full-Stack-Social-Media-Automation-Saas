from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import current_user
from ..models import User
from ..schemas import UserOut,ProfileUpdate
router=APIRouter(prefix="/users",tags=["Users"])
@router.get("/me",response_model=UserOut)
def me(u:User=Depends(current_user)): return u
@router.put("/me",response_model=UserOut)
def update(x:ProfileUpdate,u:User=Depends(current_user),db:Session=Depends(get_db)):
    u.name=x.name;db.commit();db.refresh(u);return u

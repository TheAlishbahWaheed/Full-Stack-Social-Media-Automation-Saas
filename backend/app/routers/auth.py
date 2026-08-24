from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate,LoginRequest,Token
from ..security import hash_password,verify_password,token
router=APIRouter(prefix="/auth",tags=["Auth"])
@router.post("/register",response_model=Token)
def register(x:UserCreate,db:Session=Depends(get_db)):
    if db.query(User).filter_by(email=x.email).first(): raise HTTPException(400,"Email is already registered")
    u=User(name=x.name,email=x.email,hashed_password=hash_password(x.password));db.add(u);db.commit();db.refresh(u)
    return {"access_token":token(u.id),"user":u}
@router.post("/login",response_model=Token)
def login(x:LoginRequest,db:Session=Depends(get_db)):
    u=db.query(User).filter_by(email=x.email).first()
    if not u or not verify_password(x.password,u.hashed_password): raise HTTPException(401,"Invalid email or password")
    return {"access_token":token(u.id),"user":u}

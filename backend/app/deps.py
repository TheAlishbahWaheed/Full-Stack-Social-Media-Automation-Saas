from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .security import user_id
bearer=HTTPBearer()
def current_user(c=Depends(bearer),db:Session=Depends(get_db)):
    try: uid=user_id(c.credentials)
    except (JWTError,ValueError,KeyError): raise HTTPException(401,"Invalid or expired token")
    u=db.get(User,uid)
    if not u: raise HTTPException(401,"User not found")
    return u

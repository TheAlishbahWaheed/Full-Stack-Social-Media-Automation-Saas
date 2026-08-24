from datetime import datetime,timedelta,timezone
from jose import jwt
from passlib.context import CryptContext
from .database import settings
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def token(uid): return jwt.encode({"sub":str(uid),"exp":datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)},settings.SECRET_KEY,algorithm="HS256")
def user_id(t): return int(jwt.decode(t,settings.SECRET_KEY,algorithms=["HS256"])["sub"])

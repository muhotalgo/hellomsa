from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.models.user as sqlm
import api.schema.user as pym
from api import auth
from api.database import get_db

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/users", response_model=list[pym.User])
async def list_products(db: Session = Depends(get_db)):
    users = db.query(sqlm.User).all()
    return [pym.User.from_orm(p) for p in users]


@router.post("/users", response_model=pym.User)
async def create_user(user: pym.UserCreate, db: Session = Depends(get_db)):
    return auth.register(db, user)


@router.post("/login", response_model=pym.Token)
async def login_user(user: pym.UserLogin, db: Session = Depends(get_db)):
    token = auth.authenticate(db, user)

    if not token:
        raise HTTPException(status_code=401,
                            detail='로그인 실패!! - 아이디나 비밀번호가 틀려요!')

    return token
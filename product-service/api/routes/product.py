from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.models.product as sqlm
import api.schema.product as pym
from api.database import get_db

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/products", response_model=list[pym.Product])
async def list_products(db: Session = Depends(get_db)):
    products = db.query(sqlm.Product).all()
    return [pym.Product.from_orm(p) for p in products]


@router.post("/products", response_model=pym.Product)
async def create_products(product: pym.ProductCreate, db: Session = Depends(get_db)):
    product = sqlm.Product(**product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return pym.Product.from_orm(product)
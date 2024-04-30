from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    class Config:
        from_attributes=True


class Product(ProductBase):
    pno: int

    class Config:
        from_attributes=True

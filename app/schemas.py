from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id : int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name : str
    description : str
    price : float
    stock : int 

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id : int

    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    quantity : int
    product_id : int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id : int
    user_id : int

    class Config:
        orm_mode = True
    
class PurchaseBase(BaseModel):
    total_price : float

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id : int
    user_id : int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str
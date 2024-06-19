from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, autoincrement= True)
    username = Column(String, unique= True, index= True)
    hashed_password = Column(String)

    cart_items = relationship("CartItem", back_populates="onwer")
    purchases = relationship("Purchase", back_populates="buyer")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String, unique= True, index= True)
    description = Column(String, index= True)
    price = Column(Integer)
    stock = Column(Integer)

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key= True, autoincrement= True)
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))


    onwer = relationship("User", back_populates="cart_items")
    product = relationship("Product")
    
class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key= True, autoincrement= True)
    total_price = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    product_id = Column(Integer, ForeignKey("products.id"))

    buyer = relationship("User", back_populates="purchases")
    product = relationship("Product")
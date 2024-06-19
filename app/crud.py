from sqlalchemy.orm import Session
import models
import schemas
import depends

def get_user_by_username(db: Session, username : str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = depends.get_password_hash(user.password)
    db_user = models.User(username = user.username, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_product(db: Session, product_id = int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session):
    return db.query(models.Product).all()

def create_products(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_cart_items(db: Session, user_id : int):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).first()

def add_item_to_cart(db: Session, cart_item : schemas.CartItemCreate, user_id : int = models.User.id):
    db_cart_item = models.CartItem(**cart_item.dict(), user_id = user_id)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def create_purchase(db: Session, purchase: schemas.PurchaseCreate, user_id = int):
    db_purchase = models.Purchase(**purchase.dict(), user_id = user_id)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm  
from sqlalchemy.orm import Session
import crud
import schemas
import depends
import database

database.Base.metadata.create_all(bind = database.engine)

app = FastAPI()

@app.get("/user", response_model=list[schemas.User], tags=["USER"])
def get_user(username: str,db: Session = Depends(depends.get_db)):
    try:
        user = crud.get_user_by_username(db,username)
        if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not able to find the user"
                )
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )

#login endpoint
@app.post("/token", response_model=schemas.Token, tags=["USER"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(depends.get_db)):
    try:
        user = depends.authenticate_user(db, form_data.username, form_data.password)
        if not user :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Bad request"
            )
        access_token = depends.create_access_token(data={"sub": user.username})
        return {"access_token" : access_token, "token_type" : "bearer"}
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )

#creating a user
@app.post("/users", response_model=schemas.User,  tags=["USER"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(depends.get_db)):
    try:
        db_user = crud.get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "user already registered"
            )
        return crud.create_user(db=db, user= user)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already registered"
        )


#read the products
@app.get("/products", response_model=list[schemas.Product], tags= ["PRODUCT"])
async def read_products(db: Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    try:
        product = crud.get_products(db)
        return product
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )

#creating the new products
@app.post("/products", response_model=schemas.Product, tags= ["PRODUCT"])
def create_products(product : schemas.ProductCreate, db : Session = Depends(depends.get_db), current_user: schemas.User =Depends(depends.get_current_user)):
    try:
        return crud.create_products(db=db, product=product)
    except:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Product not created"
        )

#read the cartitems
@app.get("/carts", response_model= list[schemas.CartItem], tags= ["CART"])
def read_cart(user_id:int ,db: Session = Depends(depends.get_db), current_user: schemas.User = Depends(depends.get_current_user)):
    try:
        return crud.get_cart_items(db, user_id=user_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cart items found"
        )

#add the items to cart
@app.post("/cart", response_model=schemas.CartItem, tags= ["CART"])
def add_item_to_cart(cart_item : schemas.CartItemCreate, db : Session = Depends(depends.get_db), current_user : schemas.User = Depends(depends.get_current_user)):
   try:
        return crud.add_item_to_cart(db= db, cart_item=cart_item, user_id=current_user.id)
   except:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Item not added to cart"
       )

#creating a purchase
@app.post("/purchase", response_model=schemas.Purchase, tags= ["PURCHASE"])
async def create_purchase(purchase : schemas.PurchaseCreate, db : Session = Depends(depends.get_db), current_user: schemas.User = Depends(depends.get_current_user)):
    try:
        return crud.create_purchase(db=db, purchase=purchase, user_id=current_user.id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Purchase not created"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port= 5000)
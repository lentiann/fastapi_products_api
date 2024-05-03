from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

import app.routers.products_router as products_router

import app.repositories.users as users_repository
import app.schemas.schemas as schemas
import app.utils.auth_jwt as authentication

from app.utils.database import SessionLocal


from app.utils.exceptions import ProductNotFound

app = FastAPI()
app.include_router(products_router.router)


@app.exception_handler(ProductNotFound)
async def product_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db = SessionLocal()
    user.password = authentication.get_password_hash(user.password)
    return users_repository.create_user(db, user)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authentication.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/items/")
def read_own_items(user: schemas.User = Depends(authentication.get_current_active_user)):
    return {"username": user.username, "email": user.email}

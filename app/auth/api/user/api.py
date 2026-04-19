"""Api for user."""
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.schemas.user import UserLogin, UserRegister
from app.auth.schemas.tokens import TokenPair
from app.auth.domain.Auth import AuthService

app = APIRouter(prefix='/user')

@app.post('/login', response_model=TokenPair)
async def login_user(user_data: UserLogin):
    try:
        tokens = await AuthService.login(user_data)
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e

@app.post('/register', response_model=TokenPair)
async def register_user(user_data: UserRegister):
    try:
        tokens = await AuthService.register(user_data)
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

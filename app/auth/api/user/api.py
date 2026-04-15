"""Api for user."""
from fastapi import APIRouter, Depends
from app.auth.database import get_db
from sqlalchemy.orm import Session
from models import user

app = APIRouter(prefix='user')

@app.post('/login', response_model=user.UserLogin)
async def login_user():
    pass


@app.post('/register', response_model=user.UserRegister)
async def register_user(session: Session = Depends(get_db)):
    s
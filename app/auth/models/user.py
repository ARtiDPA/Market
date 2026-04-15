"""Models for api on user."""

from pydantic import BaseModel

class UserRegister(BaseModel):
    """User register data.

    Args:
        BaseModel (class): base model
    """
    login: str
    password: str
    name: str
    last_name: str


class UserLogin(BaseModel):
    """User login data.

    Args:
        BaseModel (_type_): _description_
    """
    login: str
    password: str

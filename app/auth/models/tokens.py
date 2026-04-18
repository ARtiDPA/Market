from pydantic import BaseModel



class TokenPair(BaseModel):
    """tokens

    Args:
        BaseModel (class): _description_
    """
    access_token: str
    refresh_token: str

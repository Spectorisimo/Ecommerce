from enum import Enum

from pydantic import BaseModel


class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'


class TokenPayload(BaseModel):
    sub: str
    exp: int
    token_type: TokenType
    jti: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

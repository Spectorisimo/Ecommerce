from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'


@dataclass
class Token:
    subject_id: str
    token_type: TokenType
    jti: str
    expires_at: datetime


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str

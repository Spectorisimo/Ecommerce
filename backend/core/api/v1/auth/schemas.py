from pydantic import BaseModel

from core.apps.users.entities.tokens import TokenPair as TokensEntity


class CredentialSchema(BaseModel):
    email: str
    password: str


class TokenOutSchema(BaseModel):
    access_token: str
    refresh_token: str

    @staticmethod
    def from_entity(entity: TokensEntity) -> 'TokenOutSchema':
        return TokenOutSchema(**entity.dict())

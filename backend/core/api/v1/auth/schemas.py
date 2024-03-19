from pydantic import BaseModel

from core.apps.users.entities.tokens import TokenPair


class CredentialSchema(BaseModel):
    email: str
    password: str


class TokenOutSchema(BaseModel):
    access_token: str
    refresh_token: str

    @classmethod
    def from_entity(cls, token_pair: TokenPair) -> 'TokenOutSchema':
        return cls(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )

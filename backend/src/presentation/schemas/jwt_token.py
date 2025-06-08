from pydantic import BaseModel


class Token(BaseModel):
    token: str


class JWTToken(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenResponse(Token):
    ...

class AccessTokenReponse(Token):
    ...
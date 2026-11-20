from pydantic import BaseModel, Field, SecretStr, field_validator


class AuthCredentials(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: SecretStr = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class RegisterRequest(AuthCredentials):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)

class LoginRequest(AuthCredentials):
    pass


class RefreshRequest(BaseModel):
    refresh_token: SecretStr


class AuthUser(BaseModel):
    id: str
    email: str | None
    first_name: str | None = None
    last_name: str | None = None


class AuthSession(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RegisterResponse(BaseModel):
    user: AuthUser
    session: AuthSession | None
    message: str


class LoginResponse(AuthSession):
    user: AuthUser


class MessageResponse(BaseModel):
    message: str

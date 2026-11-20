from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from supabase_auth.errors import AuthApiError
from supabase_auth.types import Session, User

from app.core.auth import get_current_user
from app.core.database import get_auth_client
from app.schemas.auth import (
    AuthSession,
    AuthUser,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _auth_user(user: User) -> AuthUser:
    metadata = user.user_metadata or {}
    return AuthUser(
        id=user.id,
        email=user.email,
        first_name=metadata.get("first_name"),
        last_name=metadata.get("last_name"),
    )


def _provider_error(
    error: AuthApiError,
    *,
    invalid_status: int,
    invalid_message: str,
) -> HTTPException:
    if error.status == 429:
        return HTTPException(status_code=429, detail="Too many authentication requests.")
    if error.status >= 500:
        return HTTPException(
            status_code=502,
            detail="Authentication provider request failed.",
        )
    return HTTPException(status_code=invalid_status, detail=invalid_message)


def _auth_session(session: Session) -> AuthSession:
    return AuthSession(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        token_type=session.token_type,
        expires_in=session.expires_in,
    )


@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(
    request: RegisterRequest,
    client: Client = Depends(get_auth_client),
) -> RegisterResponse:
    user_metadata = {
        key: value
        for key, value in {
            "first_name": request.first_name,
            "last_name": request.last_name,
        }.items()
        if value is not None
    }
    credentials: dict[str, object] = {
        "email": request.email,
        "password": request.password.get_secret_value(),
    }
    if user_metadata:
        credentials["options"] = {"data": user_metadata}

    try:
        response = client.auth.sign_up(credentials)
    except AuthApiError as exc:
        raise _provider_error(
            exc,
            invalid_status=400,
            invalid_message="Unable to register with the provided credentials.",
        ) from exc

    if response.user is None:
        raise HTTPException(status_code=502, detail="Authentication provider returned no user.")

    session = _auth_session(response.session) if response.session is not None else None
    message = (
        "Account created. You can now sign in."
        if session is not None
        else "Account created. Check your email to confirm your account."
    )
    return RegisterResponse(user=_auth_user(response.user), session=session, message=message)


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    client: Client = Depends(get_auth_client),
) -> LoginResponse:
    try:
        response = client.auth.sign_in_with_password(
            {
                "email": request.email,
                "password": request.password.get_secret_value(),
            }
        )
    except AuthApiError as exc:
        raise _provider_error(
            exc,
            invalid_status=401,
            invalid_message="Invalid email or password.",
        ) from exc

    if response.user is None or response.session is None:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return LoginResponse(
        **_auth_session(response.session).model_dump(),
        user=_auth_user(response.user),
    )


@router.post("/refresh", response_model=LoginResponse)
def refresh(
    request: RefreshRequest,
    client: Client = Depends(get_auth_client),
) -> LoginResponse:
    try:
        response = client.auth.refresh_session(request.refresh_token.get_secret_value())
    except AuthApiError as exc:
        raise _provider_error(
            exc,
            invalid_status=401,
            invalid_message="Invalid or expired refresh token.",
        ) from exc

    if response.user is None or response.session is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")

    return LoginResponse(
        **_auth_session(response.session).model_dump(),
        user=_auth_user(response.user),
    )


@router.post("/logout", response_model=MessageResponse)
def logout(
    request: RefreshRequest,
    client: Client = Depends(get_auth_client),
) -> MessageResponse:
    try:
        response = client.auth.refresh_session(request.refresh_token.get_secret_value())
        if response.session is None:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")
        client.auth.sign_out({"scope": "local"})
    except AuthApiError as exc:
        raise _provider_error(
            exc,
            invalid_status=401,
            invalid_message="Invalid or expired refresh token.",
        ) from exc

    return MessageResponse(message="Signed out successfully.")


@router.get("/me", response_model=AuthUser)
def get_me(user: User = Depends(get_current_user)) -> AuthUser:
    return _auth_user(user)

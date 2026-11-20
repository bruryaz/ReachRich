from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client
from supabase_auth.errors import AuthApiError
from supabase_auth.types import User

from app.core.database import get_auth_client

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    client: Client = Depends(get_auth_client),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        response = client.auth.get_user(credentials.credentials)
    except AuthApiError as exc:
        if exc.status == 429:
            raise HTTPException(status_code=429, detail="Too many authentication requests.") from exc
        if exc.status >= 500:
            raise HTTPException(
                status_code=502,
                detail="Authentication provider request failed.",
            ) from exc
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if response is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response.user

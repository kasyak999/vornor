from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.crud.user import ALGORITHM
from http import HTTPStatus

security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """Получение текущего пользователя по токену."""
    try:
        payload = jwt.decode(
            token.credentials, settings.secret, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Недействительный токен") from exc

from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.config import get_settings
from backend.app.database import get_db
from backend.app.models.entities import AdminUser
from backend.app.schemas.contracts import LoginRequestDTO, TokenResponseDTO
from backend.app.services.auth_service import (
    create_access_token,
    get_current_admin,
    verify_password,
)

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["Admin Concierge Authentication"])


@router.post("/login", response_model=TokenResponseDTO, summary="Admin Login & Bearer Token Generation")
async def login(payload: LoginRequestDTO, db: AsyncSession = Depends(get_db)):
    """Authenticates admin staff and issues signed JWT bearer token."""
    res = await db.execute(select(AdminUser).where(AdminUser.email == payload.username))
    user = res.scalars().first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email address or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin user account has been disabled."
        )

    # Record login timestamp
    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    token = create_access_token(
        data={"sub": user.email, "role": user.role, "name": user.full_name}
    )

    return TokenResponseDTO(
        access_token=token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        user_email=user.email,
        full_name=user.full_name,
        role=user.role
    )


@router.get("/me", summary="Get Authenticated Admin Profile")
async def get_me(current_admin: AdminUser = Depends(get_current_admin)):
    """Returns profile information for the actively authenticated staff member."""
    return {
        "id": current_admin.id,
        "email": current_admin.email,
        "full_name": current_admin.full_name,
        "role": current_admin.role,
        "is_active": current_admin.is_active,
        "last_login": current_admin.last_login
    }

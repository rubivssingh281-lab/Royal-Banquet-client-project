from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.schemas.contracts import AvailabilityCheckResponseDTO
from backend.app.services.availability_service import AvailabilityService

router = APIRouter(prefix="/availability", tags=["Date & Capacity Availability"])


@router.get(
    "/check",
    response_model=AvailabilityCheckResponseDTO,
    summary="Check Date Availability & Ballroom Recommendation"
)
async def check_availability(
    date: str = Query(..., description="Target celebration date in YYYY-MM-DD format"),
    guests: str = Query("medium", description="Guest count tier (e.g. intimate, medium, grand)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Evaluates date availability against existing reservations and recommends
    the optimal ballroom layout for the specified guest count.
    """
    return await AvailabilityService.check_availability(db, date=date, guest_count=guests)


@router.get(
    "/calendar",
    response_model=List[Dict[str, Any]],
    summary="Get Monthly Reservation Availability Calendar"
)
async def get_monthly_calendar(
    month: str = Query(..., description="Target month in YYYY-MM format (e.g. 2026-12)"),
    db: AsyncSession = Depends(get_db)
):
    """Returns booked dates and slots across all ballrooms for a given calendar month."""
    return await AvailabilityService.get_month_calendar(db, year_month=month)

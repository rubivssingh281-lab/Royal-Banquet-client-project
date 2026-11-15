from __future__ import annotations

from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.models.entities import AdminUser
from backend.app.schemas.contracts import (
    InquiryCreateDTO,
    InquiryResponseDTO,
    InquiryUpdateStatusDTO,
    ProblemDetail,
)
from backend.app.services.auth_service import get_current_admin
from backend.app.services.inquiry_service import InquiryService

router = APIRouter(prefix="/inquiries", tags=["Inquiries & Consultation Requests"])


@router.post(
    "",
    response_model=InquiryResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ProblemDetail}},
    summary="Submit a Family Reservation Inquiry & Tour Request"
)
async def create_inquiry(
    payload: InquiryCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    """
    Submits a reservation consultation request from the public website form.
    Automatically assigns recommended ballroom based on guest count tier.
    """
    try:
        inquiry = await InquiryService.create_inquiry(db, payload)
        return inquiry
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process inquiry: {str(e)}"
        )


@router.get(
    "",
    response_model=List[InquiryResponseDTO],
    summary="List Inquiries (Admin Concierge Only)"
)
async def list_inquiries(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by pending|contacted|confirmed|cancelled"),
    search: Optional[str] = Query(None, description="Search by name, phone, or email"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Returns paginated inquiries. Requires valid admin bearer token."""
    return await InquiryService.list_inquiries(
        db, status=status_filter, search=search, limit=limit, offset=offset
    )


@router.get(
    "/stats",
    response_model=Dict[str, int],
    summary="Get Inquiry Pipeline Metrics (Admin Concierge Only)"
)
async def get_inquiry_stats(
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Returns real-time pipeline counts for pending, contacted, and confirmed leads."""
    return await InquiryService.get_stats(db)


@router.patch(
    "/{inquiry_id}/status",
    response_model=InquiryResponseDTO,
    summary="Update Inquiry Status & Concierge Notes"
)
async def update_inquiry_status(
    inquiry_id: int,
    payload: InquiryUpdateStatusDTO,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Updates an inquiry's status and records follow-up notes."""
    updated = await InquiryService.update_status(db, inquiry_id, payload)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inquiry with ID {inquiry_id} not found."
        )
    return updated

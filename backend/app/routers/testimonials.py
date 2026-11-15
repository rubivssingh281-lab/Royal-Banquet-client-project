from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.models.entities import Testimonial
from backend.app.schemas.contracts import (
    TestimonialCreateDTO,
    TestimonialResponseDTO,
)

router = APIRouter(prefix="/testimonials", tags=["Family Love Letters & Testimonials"])


@router.get("", response_model=List[TestimonialResponseDTO], summary="List Approved Love Letters")
async def get_testimonials(db: AsyncSession = Depends(get_db)):
    """Returns curated 5-star testimonials from celebrating families."""
    res = await db.execute(
        select(Testimonial).where(Testimonial.is_approved == True).order_by(desc(Testimonial.created_at))
    )
    return list(res.scalars().all())


@router.post("", response_model=TestimonialResponseDTO, status_code=status.HTTP_201_CREATED, summary="Submit Family Review")
async def submit_testimonial(payload: TestimonialCreateDTO, db: AsyncSession = Depends(get_db)):
    """Allows celebration guests to submit feedback and love letters."""
    testimonial = Testimonial(
        author_names=payload.author_names,
        event_type=payload.event_type,
        rating=payload.rating,
        review_text=payload.review_text,
        is_approved=True  # Auto-approved or set to False for moderation
    )
    db.add(testimonial)
    await db.commit()
    await db.refresh(testimonial)
    return testimonial

from __future__ import annotations

from typing import Dict, List, Optional
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.entities import Inquiry, Venue
from backend.app.schemas.contracts import InquiryCreateDTO, InquiryUpdateStatusDTO


class InquiryService:
    """Business service orchestrating consultation inquiries and lead pipeline."""

    @staticmethod
    async def create_inquiry(db: AsyncSession, payload: InquiryCreateDTO) -> Inquiry:
        """Persists a new celebration inquiry."""
        # Auto-resolve venue if not provided based on guest tier
        venue_id = payload.venue_id
        if not venue_id:
            guest_str = payload.estimated_guests.lower()
            if "grand" in guest_str or "1,200" in guest_str or "600" in guest_str:
                palace = await db.execute(select(Venue).where(Venue.slug == "the-royal-palace"))
                palace_v = palace.scalars().first()
                if palace_v:
                    venue_id = palace_v.id
            else:
                banquet = await db.execute(select(Venue).where(Venue.slug == "the-royal-banquet"))
                banquet_v = banquet.scalars().first()
                if banquet_v:
                    venue_id = banquet_v.id

        inquiry = Inquiry(
            full_name=payload.full_name,
            phone=payload.phone,
            email=payload.email,
            celebration_type=payload.celebration_type,
            estimated_guests=payload.estimated_guests,
            preferred_date=payload.preferred_date,
            venue_id=venue_id,
            message=payload.message,
            status="pending"
        )
        db.add(inquiry)
        await db.commit()
        await db.refresh(inquiry)
        return inquiry

    @staticmethod
    async def list_inquiries(
        db: AsyncSession,
        status: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Inquiry]:
        """Lists inquiries with optional filtering."""
        query = select(Inquiry).order_by(desc(Inquiry.created_at))
        if status:
            query = query.where(Inquiry.status == status)
        if search:
            query = query.where(
                (Inquiry.full_name.ilike(f"%{search}%")) |
                (Inquiry.phone.ilike(f"%{search}%")) |
                (Inquiry.email.ilike(f"%{search}%"))
            )
        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_status(
        db: AsyncSession,
        inquiry_id: int,
        payload: InquiryUpdateStatusDTO
    ) -> Optional[Inquiry]:
        """Updates status and concierge notes for an inquiry."""
        result = await db.execute(select(Inquiry).where(Inquiry.id == inquiry_id))
        inquiry = result.scalars().first()
        if not inquiry:
            return None

        inquiry.status = payload.status
        if payload.admin_notes is not None:
            inquiry.admin_notes = payload.admin_notes

        await db.commit()
        await db.refresh(inquiry)
        return inquiry

    @staticmethod
    async def get_stats(db: AsyncSession) -> Dict[str, int]:
        """Calculates breakdown of inquiries for administrative dashboard."""
        query = select(Inquiry.status, func.count(Inquiry.id)).group_by(Inquiry.status)
        result = await db.execute(query)
        stats = {"pending": 0, "contacted": 0, "confirmed": 0, "cancelled": 0, "total": 0}
        total = 0
        for status_val, count_val in result.all():
            stats[status_val] = count_val
            total += count_val
        stats["total"] = total
        return stats

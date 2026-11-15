from __future__ import annotations

from typing import Any, Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.entities import BookingAvailability, Venue
from backend.app.schemas.contracts import AvailabilityCheckResponseDTO


class AvailabilityService:
    """Service evaluating event dates and palatial venue capacities."""

    @staticmethod
    async def check_availability(
        db: AsyncSession,
        date: str,
        guest_count: str
    ) -> AvailabilityCheckResponseDTO:
        """
        Evaluates venue capacity and availability for a requested date and guest tier.
        """
        # Fetch venues
        res_venues = await db.execute(select(Venue).where(Venue.is_active == True))
        venues = list(res_venues.scalars().all())

        # Check existing bookings for the specified date
        res_bookings = await db.execute(
            select(BookingAvailability).where(BookingAvailability.booked_date == date)
        )
        bookings = list(res_bookings.scalars().all())
        conflicting_count = len(bookings)

        lower_tier = guest_count.lower()
        if "grand" in lower_tier or "1200" in lower_tier or "600" in lower_tier:
            target_slug = "the-royal-palace"
            tier_label = "Grand Gala (600 – 1,200+ Guests)"
            rec_notes = (
                "The Royal Palace Grand Ballroom is recommended for 600 to 1,200+ guests. "
                "Features soaring ceilings, crystal chandeliers, expansive dining halls, and full valet parking."
            )
        elif "intimate" in lower_tier or "300" in lower_tier:
            target_slug = "the-royal-banquet"
            tier_label = "Intimate Gathering (100 – 300 Guests)"
            rec_notes = (
                "The Royal Banquet Ballroom is tailor-made for intimate gatherings (100–300 guests). "
                "Provides acoustic staging, private family lounges, and an intimate royal ambiance."
            )
        else:
            target_slug = "the-royal-banquet"
            tier_label = "Medium Celebration (300 – 600 Guests)"
            rec_notes = (
                "The Royal Banquet (Main Ballroom) accommodates 300 to 600 guests comfortably, "
                "with step-free transitions and seamless mandap-to-dining flow."
            )

        rec_venue = next((v for v in venues if v.slug == target_slug), None)
        rec_venue_name = rec_venue.name if rec_venue else "The Royal Banquet Palace"
        rec_venue_id = rec_venue.id if rec_venue else None

        # Check if the specific recommended venue is locked on this date
        venue_booked = any(b.venue_id == rec_venue_id and b.is_locked for b in bookings) if rec_venue_id else False

        is_available = not venue_booked

        if venue_booked:
            rec_notes += " Note: The preferred evening slot has a pending reservation; our concierge can offer the morning/afternoon slot or an adjacent weekend date."

        return AvailabilityCheckResponseDTO(
            date=date,
            is_available=is_available,
            recommended_venue=rec_venue_name,
            recommended_venue_id=rec_venue_id,
            guest_tier=tier_label,
            recommendation_notes=rec_notes,
            conflicting_bookings_count=conflicting_count
        )

    @staticmethod
    async def get_month_calendar(
        db: AsyncSession,
        year_month: str
    ) -> List[Dict[str, Any]]:
        """
        Returns list of reserved dates within a YYYY-MM prefix.
        """
        query = select(BookingAvailability).where(
            BookingAvailability.booked_date.like(f"{year_month}%")
        )
        res = await db.execute(query)
        bookings = res.scalars().all()

        return [
            {
                "date": b.booked_date,
                "venue_id": b.venue_id,
                "slot": b.slot,
                "celebration_type": b.celebration_type,
                "is_locked": b.is_locked
            }
            for b in bookings
        ]

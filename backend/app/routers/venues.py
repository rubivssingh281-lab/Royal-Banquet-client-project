from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.models.entities import Venue
from backend.app.schemas.contracts import VenueResponseDTO

router = APIRouter(prefix="/venues", tags=["Palatial Venues & Ballrooms"])


def serialize_venue(v: Venue) -> VenueResponseDTO:
    """Helper formatting comma-separated features into clean string array."""
    feature_list = [f.strip() for f in v.features.split(",") if f.strip()] if v.features else []
    return VenueResponseDTO(
        id=v.id,
        slug=v.slug,
        name=v.name,
        tagline=v.tagline,
        address=v.address,
        locality=v.locality,
        min_capacity=v.min_capacity,
        max_capacity=v.max_capacity,
        description=v.description,
        features=feature_list,
        image_url=v.image_url,
        is_active=v.is_active
    )


@router.get("", response_model=List[VenueResponseDTO], summary="List All Grand Venues")
async def get_venues(db: AsyncSession = Depends(get_db)):
    """Returns list of active ballrooms and palatial venues."""
    res = await db.execute(select(Venue).where(Venue.is_active == True))
    venues = res.scalars().all()
    return [serialize_venue(v) for v in venues]


@router.get("/{slug}", response_model=VenueResponseDTO, summary="Get Venue Details by Slug")
async def get_venue_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Retrieves full specification for a specific venue by slug."""
    res = await db.execute(select(Venue).where(Venue.slug == slug, Venue.is_active == True))
    venue = res.scalars().first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venue '{slug}' was not found."
        )
    return serialize_venue(venue)

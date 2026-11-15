from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base


def utc_now() -> datetime:
    """Returns current UTC timestamp with timezone information."""
    return datetime.now(timezone.utc)


class Venue(Base):
    """
    Physical Palatial Venues managed by The Royal Banquet Palace.
    """
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    tagline: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    locality: Mapped[str] = mapped_column(String(100), default="Dwarka, New Delhi")
    min_capacity: Mapped[int] = mapped_column(Integer, default=100)
    max_capacity: Mapped[int] = mapped_column(Integer, default=1200)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    features: Mapped[str] = mapped_column(Text, default="")  # Comma-separated or JSON list
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Relationships
    inquiries: Mapped[List["Inquiry"]] = relationship("Inquiry", back_populates="venue")
    bookings: Mapped[List["BookingAvailability"]] = relationship("BookingAvailability", back_populates="venue")


class Inquiry(Base):
    """
    Family Reservation & Tour Consultation Inquiries.
    Captures high-value wedding and celebration leads.
    """
    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    celebration_type: Mapped[str] = mapped_column(String(100), nullable=False)
    estimated_guests: Mapped[str] = mapped_column(String(50), nullable=False)
    preferred_date: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    
    venue_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("venues.id"), nullable=True)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Workflow Status: pending | contacted | confirmed | cancelled
    status: Mapped[str] = mapped_column(String(50), default="pending", index=True)
    admin_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    venue: Mapped[Optional["Venue"]] = relationship("Venue", back_populates="inquiries")


class BookingAvailability(Base):
    """
    Tracks locked and reserved event dates/slots for real-time calendar availability.
    """
    __tablename__ = "booking_availability"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venue_id: Mapped[int] = mapped_column(Integer, ForeignKey("venues.id"), nullable=False, index=True)
    booked_date: Mapped[str] = mapped_column(String(30), nullable=False, index=True)  # YYYY-MM-DD
    slot: Mapped[str] = mapped_column(String(30), default="evening")  # morning | evening | full_day
    celebration_type: Mapped[str] = mapped_column(String(100), default="Wedding Reception")
    is_locked: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Relationships
    venue: Mapped["Venue"] = relationship("Venue", back_populates="bookings")


class Testimonial(Base):
    """
    Family and Couple Testimonials & Love Letters.
    """
    __tablename__ = "testimonials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_names: Mapped[str] = mapped_column(String(200), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), default="Wedding Celebration")
    rating: Mapped[int] = mapped_column(Integer, default=5)
    review_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class BlogPost(Base):
    """
    Wedding planning guides and articles migrated from original WordPress publication.
    """
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    published_date: Mapped[str] = mapped_column(String(50), nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    cover_image: Mapped[str] = mapped_column(String(500), nullable=False)
    read_time: Mapped[str] = mapped_column(String(50), default="5 min read")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AdminUser(Base):
    """
    Administrative and concierge management users.
    """
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="concierge_admin")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

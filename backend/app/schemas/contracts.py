from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ─── COMMON & RFC 9457 SCHEMAS ──────────────────────────────────────────────

class ProblemDetail(BaseModel):
    """RFC 9457 standardized problem response."""
    model_config = ConfigDict(extra="forbid")

    type: str = Field(default="about:blank", description="URI reference identifying problem type")
    title: str = Field(..., description="Short human-readable summary of problem")
    status: int = Field(..., description="HTTP status code")
    detail: str = Field(..., description="Human-readable explanation specific to this occurrence")
    instance: Optional[str] = Field(default=None, description="URI reference identifying specific occurrence")


# ─── INQUIRY CONTRACTS ──────────────────────────────────────────────────────

class InquiryCreateDTO(BaseModel):
    """Payload received from the frontend reservation & consultation form."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    full_name: str = Field(..., min_length=2, max_length=200, description="Full name of contact person")
    phone: str = Field(..., min_length=7, max_length=25, description="Mobile / WhatsApp number")
    email: EmailStr = Field(..., description="Valid contact email address")
    celebration_type: str = Field(..., min_length=2, max_length=100, description="Type of event/celebration")
    estimated_guests: str = Field(..., min_length=2, max_length=50, description="Guest tier (e.g. 100-300, 300-600, 600-1200+)")
    preferred_date: str = Field(..., min_length=6, max_length=30, description="Preferred event date (YYYY-MM-DD or descriptive)")
    venue_id: Optional[int] = Field(default=None, description="Preferred venue ID if pre-selected")
    message: Optional[str] = Field(default=None, max_length=3000, description="Special vision, traditions, or dietary requests")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Strip common formatting characters
        cleaned = re.sub(r"[\s\-\(\)\.]", "", v)
        if not re.match(r"^\+?[0-9]{7,15}$", cleaned):
            raise ValueError("Phone number must contain between 7 and 15 digits, optionally prefixed with '+'")
        return v


class InquiryUpdateStatusDTO(BaseModel):
    """Concierge update payload for managing inquiry status."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    status: str = Field(..., pattern="^(pending|contacted|confirmed|cancelled)$")
    admin_notes: Optional[str] = Field(default=None, max_length=2000)


class InquiryResponseDTO(BaseModel):
    """Output DTO for family inquiry."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str
    email: str
    celebration_type: str
    estimated_guests: str
    preferred_date: str
    venue_id: Optional[int] = None
    message: Optional[str] = None
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ─── VENUE CONTRACTS ────────────────────────────────────────────────────────

class VenueResponseDTO(BaseModel):
    """Output DTO for banquet venue."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    tagline: str
    address: str
    locality: str
    min_capacity: int
    max_capacity: int
    description: str
    features: List[str]
    image_url: str
    is_active: bool


# ─── AVAILABILITY CONTRACTS ─────────────────────────────────────────────────

class AvailabilityCheckResponseDTO(BaseModel):
    """Result of calendar and date capacity inquiry."""
    date: str
    is_available: bool
    recommended_venue: str
    recommended_venue_id: Optional[int] = None
    guest_tier: str
    recommendation_notes: str
    conflicting_bookings_count: int


# ─── TESTIMONIAL CONTRACTS ──────────────────────────────────────────────────

class TestimonialCreateDTO(BaseModel):
    """Public customer review submission."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    author_names: str = Field(..., min_length=2, max_length=200)
    event_type: str = Field(default="Family Celebration", max_length=100)
    rating: int = Field(default=5, ge=1, le=5)
    review_text: str = Field(..., min_length=10, max_length=2000)


class TestimonialResponseDTO(BaseModel):
    """Output DTO for approved testimonials."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_names: str
    event_type: str
    rating: int
    review_text: str
    created_at: datetime


# ─── BLOG CONTRACTS ─────────────────────────────────────────────────────────

class BlogPostResponseDTO(BaseModel):
    """Output DTO for wedding insights & blog articles."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    category: str
    published_date: str
    excerpt: str
    content: str
    cover_image: str
    read_time: str


# ─── AUTH CONTRACTS ─────────────────────────────────────────────────────────

class LoginRequestDTO(BaseModel):
    """Admin login credentials."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    username: EmailStr = Field(..., description="Admin email address")
    password: str = Field(..., min_length=6, description="Admin password")


class TokenResponseDTO(BaseModel):
    """JWT bearer token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    user_email: str
    full_name: str
    role: str

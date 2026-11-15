from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.models.entities import BlogPost
from backend.app.schemas.contracts import BlogPostResponseDTO

router = APIRouter(prefix="/blog", tags=["Wedding Insights & Guides"])


@router.get("", response_model=List[BlogPostResponseDTO], summary="List Wedding & Celebration Guides")
async def get_blog_posts(db: AsyncSession = Depends(get_db)):
    """Returns curated articles originally published on The Royal Banquet Palace portal."""
    res = await db.execute(select(BlogPost).order_by(desc(BlogPost.created_at)))
    return list(res.scalars().all())


@router.get("/{slug}", response_model=BlogPostResponseDTO, summary="Get Article by Slug")
async def get_blog_post_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Retrieves full article content and metadata."""
    res = await db.execute(select(BlogPost).where(BlogPost.slug == slug))
    post = res.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article '{slug}' was not found."
        )
    return post

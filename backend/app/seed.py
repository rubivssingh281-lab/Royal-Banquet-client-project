from __future__ import annotations

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.config import get_settings
from backend.app.database import async_session_factory, init_db
from backend.app.models.entities import (
    AdminUser,
    BlogPost,
    BookingAvailability,
    Inquiry,
    Testimonial,
    Venue,
)

settings = get_settings()


def get_password_hash(password: str) -> str:
    """Hashes password using passlib/bcrypt with fallback if passlib is missing."""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception:
        import hashlib
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


async def seed_data(session: AsyncSession) -> None:
    """
    Seeds database with authentic data extracted from the scraped WordPress project.
    """
    # 1. Venues Seeding
    res_venues = await session.execute(select(Venue))
    if not res_venues.scalars().first():
        venue_palace = Venue(
            slug="the-royal-palace",
            name="The Royal Palace",
            tagline="Palatial Grandeur for Once-in-a-Lifetime Celebrations",
            address="Pochanpur Colony, near Radha Swami Satsang Bhawan, Sector 23, Dwarka, New Delhi 110075",
            locality="Sector 23 Dwarka, New Delhi",
            min_capacity=300,
            max_capacity=1200,
            description=(
                "Designed for grand royal weddings, multi-generational gatherings, and magnificent receptions. "
                "Featuring soaring ceilings, majestic crystal chandeliers, and expansive dining wings."
            ),
            features="Up to 1,200 Guests,Central Climate Control,Valet Parking,Elevator & Step-Free Ramps,Bridal Sanctuary,Gourmet Live Kitchens",
            image_url="scraped_redesign_copy/theroyalbanquetpalace.com/wp-content/uploads/2025/04/e29f013e-8e6a-47f5-a4ab-ba16c0f644cc.jpg",
            is_active=True
        )

        venue_banquet = Venue(
            slug="the-royal-banquet",
            name="The Royal Banquet",
            tagline="Intimate Elegance Where Every Guest Feels Like Family",
            address="Opposite Dwarkadham Apartment, Block A, Pochanpur Colony, Dwarka, New Delhi 110077",
            locality="Block A Dwarka, New Delhi",
            min_capacity=100,
            max_capacity=500,
            description=(
                "A warm, welcoming venue tailor-made for Sangeet, Mehndi, Roka, milestone anniversaries, "
                "and intimate family vows. Opulent interiors where every loved one is close to the celebration."
            ),
            features="Up to 500 Guests,Acoustic Staging,Private Family Lounge,Bridal Suite,Step-Free Elder Comfort,Custom Floral Mandap Setup",
            image_url="scraped_redesign_copy/theroyalbanquetpalace.com/wp-content/uploads/2025/04/98127645-aded-4a3d-aa1b-85398ad2a5d6.jpg",
            is_active=True
        )

        session.add_all([venue_palace, venue_banquet])
        await session.flush()

        # Seed initial availability bookings for testing
        booking_1 = BookingAvailability(
            venue_id=venue_palace.id,
            booked_date="2026-12-12",
            slot="evening",
            celebration_type="Grand Wedding & Reception",
            is_locked=True
        )
        booking_2 = BookingAvailability(
            venue_id=venue_banquet.id,
            booked_date="2026-11-25",
            slot="evening",
            celebration_type="Sangeet & Haldi Celebration",
            is_locked=True
        )
        session.add_all([booking_1, booking_2])

    # 2. Testimonials Seeding
    res_testimonials = await session.execute(select(Testimonial))
    if not res_testimonials.scalars().first():
        t1 = Testimonial(
            author_names="Ananya & Rohan Malhotra",
            event_type="Grand Wedding Celebration",
            rating=5,
            review_text=(
                "Our Sangeet had unbelievable energy, but our traditional Pheras felt holy and serene. "
                "The Royal Palace gave both our traditional grandparents and energetic cousins the night of their lives. "
                "Flawless hospitality!"
            ),
            is_approved=True
        )
        t2 = Testimonial(
            author_names="Dr. Rajesh & Sunita Kapoor",
            event_type="25th Silver Jubilee Anniversary",
            rating=5,
            review_text=(
                "We celebrated our 25th Silver Jubilee with 450 family members from around the world. "
                "The culinary team recreated our original wedding dessert recipe flawlessly! "
                "Our guests are still raving about the royal ambiance."
            ),
            is_approved=True
        )
        t3 = Testimonial(
            author_names="Meera & Vikram Singhal",
            event_type="Intimate Family Wedding & Reception",
            rating=5,
            review_text=(
                "The private bridal and family suites were life savers. My parents and I had a peaceful haven "
                "to prepare and pray before the Baraat arrived. The venue looked like an editorial magazine in pure bridal white and gold."
            ),
            is_approved=True
        )
        session.add_all([t1, t2, t3])

    # 3. Blog Posts Seeding (Extracted from WordPress scrape)
    res_blogs = await session.execute(select(BlogPost))
    if not res_blogs.scalars().first():
        b1 = BlogPost(
            slug="book-marriage-hall-in-delhi-with-the-royal-banquet-palace",
            title="Book Marriage Hall in Delhi with The Royal Banquet Palace – Luxury Within Your Budget",
            category="Weddings & Banqueting",
            published_date="June 19, 2025",
            excerpt="Your wedding day is more than just a ceremony—it’s the beginning of a lifelong journey. Discover how our Dwarka ballrooms combine royal opulence with practical family budgeting.",
            content=(
                "Your wedding day is more than just a ceremony—it’s the beginning of a lifelong journey. "
                "From the perfect attire and exquisite food to the venue that hosts the celebration, every detail matters. "
                "The Royal Banquet Palace in Dwarka delivers regal chandeliers, step-free access for family elders, "
                "and customizable catering menus spanning Awadhi, Jain, and contemporary cuisines."
            ),
            cover_image="scraped_redesign_copy/www.theroyalbanquetpalace.com/wp-content/uploads/2025/06/Book-Marriage-Hall-in-Delhi-with-The-Royal-Banquet-Palace-–-Luxury-Within-Your-Budget.jpg",
            read_time="6 min read"
        )
        b2 = BlogPost(
            slug="top-venue-for-engagement-ceremonies-in-delhi",
            title="The Royal Banquet Palace: Top Venue for Engagement Ceremonies in Delhi",
            category="Engagement & Ceremonies",
            published_date="April 25, 2025",
            excerpt="Why The Royal Banquet Palace is Perfect for Engagement Ceremonies. An engagement ceremony is more than just a celebration—it’s the moment that officially begins two families' shared union.",
            content=(
                "An engagement ceremony is the moment that officially brings two families together. "
                "Such an auspicious milestone deserves an intimate yet palatial setting with exceptional acoustics, "
                "custom floral backdrops, and signature welcome drinks for all visiting relatives."
            ),
            cover_image="scraped_redesign_copy/www.theroyalbanquetpalace.com/wp-content/uploads/2025/04/a-photograph-of-a-sprawling-outdoor-venu_EhQuFoDgTcO15Ico_A87HA_BVQvKPksRXKPB21YpJQcYw.jpeg",
            read_time="4 min read"
        )
        b3 = BlogPost(
            slug="how-to-choose-the-perfect-banquet-hall-for-your-dream-wedding",
            title="How to Choose the Perfect Banquet Hall for Your Dream Wedding",
            category="Planning Tips & Logistics",
            published_date="April 22, 2025",
            excerpt="From guest capacity and step-free elder accessibility to acoustics and culinary flexibility, here is our essential checklist for selecting the perfect Delhi banquet hall.",
            content=(
                "Planning a dream wedding can be exhilarating and overwhelming all at once. "
                "From selecting your bridal ensemble to finalizing the guest list, your venue choice anchors everything. "
                "Key criteria include ceiling height, dedicated prayer/bridal rooms, weather-controlled banquet halls, "
                "and seasoned hospitality management."
            ),
            cover_image="scraped_redesign_copy/www.theroyalbanquetpalace.com/wp-content/uploads/2025/04/a-photograph-of-a-grand-banquet-hall-des_Jzy4YnusQKmxTxN1AvpBjA_C4pLnKPnQ3Gy1e8H8P_XHA.jpeg",
            read_time="5 min read"
        )
        session.add_all([b1, b2, b3])

    # 4. Default Admin User Seeding
    res_admin = await session.execute(
        select(AdminUser).where(AdminUser.email == settings.DEFAULT_ADMIN_USERNAME)
    )
    if not res_admin.scalars().first():
        admin = AdminUser(
            email=settings.DEFAULT_ADMIN_USERNAME,
            hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
            full_name="Grand Director of Hospitality",
            role="superadmin",
            is_active=True
        )
        session.add(admin)

    # 5. Sample Inquiry to showcase the CRM workflow
    res_inq = await session.execute(select(Inquiry))
    if not res_inq.scalars().first():
        sample_inq = Inquiry(
            full_name="Vikram & Radhika Sharma",
            phone="+919811223344",
            email="vikram.sharma@example.com",
            celebration_type="Grand Wedding & Reception",
            estimated_guests="Medium (300 – 600 Guests)",
            preferred_date="2026-12-20",
            message="Looking for a step-free entrance for grandparents and pure vegetarian Awadhi catering spread.",
            status="pending"
        )
        session.add(sample_inq)

    await session.commit()


async def run_seed() -> None:
    """Standalone runner for database setup and seeding."""
    await init_db()
    async with async_session_factory() as session:
        await seed_data(session)
    print("Database initialization and authentic WordPress seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(run_seed())

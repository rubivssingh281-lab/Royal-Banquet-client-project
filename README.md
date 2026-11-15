# The Royal Banquet Palace

A luxury editorial web application and high-performance backend for **The Royal Banquet Palace & Grand Ballrooms** in Dwarka, Delhi. Redesigned with a **Wedding Dress White** aesthetic, multi-generational family hospitality, and a robust asynchronous REST API backed by SQLAlchemy and SQLite/PostgreSQL.

---

## 🕊️ Design Philosophy & Features

### 1. Wedding Dress White & Editorial Palette
- **Layered Bridal Neutrals**: Pure Silk White (`#ffffff`), Lustrous Pearl White (`#fcfbf9`), Alabaster Cream (`#f8f6f0`), and Chantilly Lace borders.
- **Accents**: Muted Royal Champagne Gold (`#c5a059`), Soft Golden Shimmer (`#e5d2ac`), and Antique Brass (`#997836`).
- **High-Contrast Editorial Typography**: Obsidian/Calligraphy Charcoal (`#1a1816`) paired with elegant serif headings (*Cormorant Garamond* & *Cinzel*) and clean sans-serif body text (*Montserrat* & *Raleway*).

### 2. Multi-Generational Family Hospitality
- **Elder-Friendly Comfort**: 100% step-free transitions, elevator access, cushioned seating, and calm conversation lounges for beloved grandparents.
- **Honoring Sacred Customs**: Dedicated spaces and logistics for Baraat processions, ceremonial Mandaps, Sangeet performances, and Haldi rituals.
- **Heirloom Banqueting**: Pure vegetarian, Jain, Awadhi, and multi-cuisine spreads honoring regional recipes.
- **Private Family & Bridal Suites**: Opulent, climate-controlled sanctuaries for pre-wedding prayers, blessings, and preparation.

### 3. Backend & Database Capabilities
- **FastAPI Core & Clean Architecture**: Fully asynchronous REST endpoints with Pydantic v2 schemas and RFC 9457 Problem Details.
- **Dual Database Compatibility**: Zero-configuration asynchronous SQLite (`royal_banquet.db`) out-of-the-box, easily switched to PostgreSQL via `DATABASE_URL`.
- **Authentic Scraped WordPress Seeding**: Automatic database population with authentic venues, WordPress articles, testimonials, and booking slots from `scraped_redesign_copy`.
- **CRM Consultation Pipeline**: End-to-end inquiry capture, status management (`pending`, `contacted`, `confirmed`, `cancelled`), and admin analytics.
- **Calendar & Capacity Engine**: Dynamic venue capacity matching and conflict checking for dates and guest tiers.
- **Security & RBAC**: Password hashing (Argon2id/Bcrypt), JWT bearer tokens, and route authorization.

---

## 📁 Project Structure

```text
/
├── index.html                  # Single-page application entry point
├── README.md                   # Full system documentation
├── package.json                # Project dependencies
├── assets/                     
│   ├── js/                     
│   │   └── main.js             # Core interactive logic, API integration & animations
│   └── css/                    # Modularized CSS styles
│       ├── base.css            # Wedding Dress White palette & CSS tokens
│       ├── navigation.css      # Editorial navbar with champagne CTA
│       ├── hero-section.css    # Bridal white hero with trust badges
│       ├── sections-general.css# Section headers, family grid & capacity tool
│       ├── ventures-section.css# High-end venue cards & floor plan inquiries
│       ├── about-section.css   # Heritage storytelling & stats
│       ├── services-section.css# Family celebration services & experiences
│       ├── portfolio-gallery.css # Curated moments gallery & category tabs
│       ├── testimonials.css    # Family testimonials & love letters
│       ├── cta-section.css     # White silk & champagne tour invitation
│       ├── contact-section.css # Private family consultation form
│       └── footer.css          # Editorial grounding footer
├── backend/
│   ├── requirements.txt        # Python backend dependencies
│   ├── run.py                  # Standalone API runner
│   ├── app/
│   │   ├── config.py           # Pydantic settings & environment configuration
│   │   ├── database.py         # SQLAlchemy async engine & session factory
│   │   ├── main.py             # FastAPI app lifespan, CORS, and error handlers
│   │   ├── seed.py             # Automatic database initialization & seed runner
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── entities.py     # Venue, Inquiry, Booking, Testimonial, BlogPost, AdminUser
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── contracts.py    # Pydantic v2 DTOs & RFC 9457 problem models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py # JWT issuance, validation & password hashing
│   │   │   ├── availability_service.py # Capacity recommender & calendar
│   │   │   └── inquiry_service.py # Lead workflow, filtering & stats
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py         # POST /api/v1/auth/login, GET /api/v1/auth/me
│   │       ├── availability.py # GET /api/v1/availability/check, GET /calendar
│   │       ├── blog.py         # GET /api/v1/blog, GET /api/v1/blog/{slug}
│   │       ├── inquiries.py    # POST /api/v1/inquiries, GET /inquiries, PATCH /{id}/status
│   │       ├── testimonials.py # GET /api/v1/testimonials, POST /testimonials
│   │       └── venues.py       # GET /api/v1/venues, GET /venues/{slug}
│   └── tests/
│       ├── __init__.py
│       └── test_api.py         # Pytest asynchronous integration suite
└── scraped_redesign_copy/      # Original scraped WordPress source materials & media
```

---

## 🚀 Running The Application

### Option A: Complete Full-Stack Run (Frontend + Backend + Database)

1. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Start the FastAPI server (automatically initializes and seeds `royal_banquet.db`):
   ```bash
   python backend/run.py
   ```

3. Open in your browser:
   - **Frontend Application**: `http://localhost:8000`
   - **Interactive OpenAPI Docs**: `http://localhost:8000/docs`
   - **Alternative ReDoc**: `http://localhost:8000/redoc`

Default Concierge Admin Credentials:
- **Username**: `admin@theroyalbanquetpalace.com`
- **Password**: `RoyalDwarka2026!`

---

### Option B: Running Tests

Execute the automated test suite with pytest:
```bash
pytest backend/tests/test_api.py -v
```

---

### Option C: Static-Only Preview

If you only want to preview the static client:
```bash
python -m http.server 8000
```

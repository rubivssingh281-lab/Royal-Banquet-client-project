# The Royal Banquet Palace

A luxury editorial web application for **The Royal Banquet Palace & Grand Ballrooms** in Dwarka, Delhi. Redesigned with a **Wedding Dress White** aesthetic and an emphasis on **multi-generational family celebrations**, honoring sacred traditions, and world-class hospitality.

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

### 3. Interactive UI Components
- **Banquet Capacity & Date Recommender**: Interactive guest count filter recommending optimal ballrooms (*The Royal Palace* up to 1,200 guests or *The Royal Banquet* up to 500 guests).
- **Curated Moments Gallery**: Filterable photo gallery (*All*, *Grand Weddings*, *Sangeet & Haldi*, *Banqueting & Feasts*, *White & Gold Decor*).
- **3D Testimonial Perspective Carousel**: Emotional love letters written by couples and parents.
- **Bridal Jasmine Petals & Golden Stardust**: Subtle falling jasmine petals and interactive stardust cursor trails on desktop.
- **Family Consultation Concierge**: Direct reservation inquiry form with celebratory golden burst feedback.

---

## 📁 Project Structure

```text
/
├── index.html                  # Single-page application entry point
├── README.md                   # Documentation
└── assets/                     
    ├── js/                     
    │   └── main.js             # Core interactive logic, filtering & animations
    └── css/                    # Modularized CSS styles
        ├── base.css            # Wedding Dress White palette & CSS tokens
        ├── navigation.css      # Editorial navbar with champagne CTA
        ├── hero-section.css    # Bridal white hero with trust badges
        ├── sections-general.css# Section headers, family grid & capacity tool
        ├── ventures-section.css# High-end venue cards & floor plan inquiries
        ├── about-section.css   # Heritage storytelling & stats
        ├── services-section.css# Family celebration services & experiences
        ├── portfolio-gallery.css # Curated moments gallery & category tabs
        ├── testimonials.css    # Family testimonials & love letters
        ├── cta-section.css     # White silk & champagne tour invitation
        ├── contact-section.css # Private family consultation form
        └── footer.css          # Editorial grounding footer
```

---

## 🚀 Previewing Locally

Run a local development server using Python:

```bash
cd ~/Royal-Banquet-client-project
python -m http.server 8000
```

Then visit:
```
http://localhost:8000
```

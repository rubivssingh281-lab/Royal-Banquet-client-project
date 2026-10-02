# The Royal Banquet Palace

A luxurious, beautifully designed frontend web application for **The Royal Banquet Palace** — an elegant wedding and event venue. This project showcases a premium, highly interactive user interface built with vanilla web technologies, emphasizing smooth micro-animations, a romantic color palette, and high performance.

##  Features

- **Dynamic Hero Section**: Engaging entrance with a slow background pulse and elegant floating heart animations.
- **Micro-Animations & Effects**: 
  - Mouse-following sparkle trails (desktop).
  - Floating rose petals falling gently across the screen.
  - Number counters that animate dynamically upon scrolling into view.
- **Modern & Responsive Layout**: Fully responsive design with a mobile-friendly slide-out hamburger menu.
- **Modular Architecture**: Clean, componentized CSS logic distributing styles across 22 specific files for excellent maintainability.
- **Smooth Navigation**: Sticky, glassmorphic navigation bar that changes transparency on scroll, paired with smooth anchor scrolling for all page sections.
- **Interactive UI Components**: Beautifully styled venture cards, service icons with hover effects, an automatic testimonial carousel, and an elegant contact form.

##  Folder Structure

The project is structured professionally for easy maintenance and scaling without the overhead of heavy JavaScript frameworks:

```text
/
├── index.html                  # Main single-page application entry point
├── README.md                   # Project documentation
└── assets/                     
    ├── js/                     
    │   └── main.js             # Core interactive logic and animations
    ├── css/                    # Modularized CSS styles
    │   ├── base.css            # Base resets and typography
    │   ├── navigation.css      # Navbar and mobile menu styles
    │   ├── hero-section.css    # Hero banner styling
    │   ├── rose-petal-fall.css # Petal animation logic
    │   ├── responsive.css      # Media queries and mobile styling
    │   └── ... (17 more specialized modules)
    └── images/                 # Local image directory
```

##  Getting Started

Since the project uses vanilla HTML, CSS, and JavaScript, no complicated build tools or Node.js dependencies are required. 

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Any lightweight local HTTP server to preview the site properly (prevents browser CORS blocks on local files).

### Installation & Execution

1. Clone or download the repository to your local machine.
2. Navigate to the project root directory:
   ```bash
   cd RoyalBanquet
   ```
3. Run a local development server. If you have Python installed, you can simply run:
   ```bash
   python -m http.server 8000
   ```
   *(Alternatively, use VS Code's "Live Server" extension or `npx serve`)*
4. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

##  Built With

- **HTML5**: Semantic and accessible markup.
- **CSS3**: Advanced CSS properties including variables, flexbox, CSS Grid, animations, and gradients.
- **Vanilla JavaScript**: Lightweight ES6+ implementation for logic, event listeners, and DOM manipulation (Zero dependencies).
- **FontAwesome**: Vector icons for UI elements and social links.
- **Google Fonts**: Premium typography using *Cormorant Garamond*, *Montserrat*, *Great Vibes*, and *Raleway*.

##  Design System

- **Primary Colors**: Gold (`#c9a96e`), Rose Gold (`#c8a882`), Deep Rose (`#b76e6e`).
- **Typography**: A mix of serif (for elegance and headings) and clean sans-serif (for readability and body text).
- **Aesthetics**: Glassmorphism, soft glowing shadows, CSS gradients, and seamless hover transitions. 

##  License

&copy; 2026 The Royal Banquet Palace. All rights reserved. 
Crafted with ♥ for special moments.

/**
 * The Royal Banquet Palace - Main Interactions & Animations
 * 
 * Features:
 * - Rich Cursor Trail
 * - Scroll-triggered Parallax
 * - IntersectionObserver reveals (Candles, Headings, Unfolding Cards)
 * - 3D Testimonial Carousel
 * - SVG Signature Draw
 * - Form Submission Confetti
 */

(function () {
    // ─── ACCESSIBILITY CHECK ───────────────
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ─── UTILITIES ───────────────
    function getOffsetTop(element) {
        let offsetTop = 0;
        while(element) {
            offsetTop += element.offsetTop;
            element = element.offsetParent;
        }
        return offsetTop;
    }

    // ─── LENIS SMOOTH SCROLL ───────────────
    let lenis;
    if (typeof Lenis !== 'undefined' && !prefersReducedMotion) {
        lenis = new Lenis({
            duration: 1.5,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            smoothWheel: true
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
    }

    // ─── NAVBAR & SCROLL TO TOP ───────────────
    const navbar = document.getElementById('navbar');
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    
    function handleScrollBasic() {
        const scrolled = window.scrollY > 60;
        if(navbar) navbar.classList.toggle('scrolled', scrolled);
        if(scrollTopBtn) scrollTopBtn.classList.toggle('visible', window.scrollY > 500);
    }
    window.addEventListener('scroll', handleScrollBasic, { passive: true });

    // ─── MOBILE MENU ───────────────
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileOverlay = document.getElementById('mobileOverlay');
    
    function toggleMenu() {
        if(!mobileMenu || !mobileOverlay) return;
        mobileMenu.classList.toggle('active');
        mobileOverlay.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }
    
    if(hamburger) hamburger.addEventListener('click', toggleMenu);
    if(mobileOverlay) mobileOverlay.addEventListener('click', toggleMenu);
    document.querySelectorAll('.mobile-menu a').forEach(link => {
        link.addEventListener('click', toggleMenu);
    });

    // ─── SMOOTH SCROLL ───────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === '') return;
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offset = 70;
                if (lenis) {
                    lenis.scrollTo(target, { offset: -offset });
                } else {
                    const top = target.getBoundingClientRect().top + window.scrollY - offset;
                    window.scrollTo({ top, behavior: 'smooth' });
                }
            }
        });
    });

    if(scrollTopBtn) {
        scrollTopBtn.addEventListener('click', () => {
            if (lenis) {
                lenis.scrollTo(0);
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }

    // ─── RICH CURSOR GLOW TRAIL ───────────────
    if (!prefersReducedMotion && window.matchMedia("(pointer: fine)").matches) {
        const cursorContainer = document.createElement('div');
        cursorContainer.id = 'cursorGlowContainer';
        cursorContainer.style.position = 'fixed';
        cursorContainer.style.top = '0';
        cursorContainer.style.left = '0';
        cursorContainer.style.width = '100vw';
        cursorContainer.style.height = '100vh';
        cursorContainer.style.pointerEvents = 'none';
        cursorContainer.style.zIndex = '9998';
        cursorContainer.style.overflow = 'hidden';
        document.body.appendChild(cursorContainer);

        const particles = [];
        const maxParticles = 40;
        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;

        window.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        }, { passive: true });

        function createCursorParticle() {
            if (particles.length > maxParticles) return;
            
            const p = document.createElement('div');
            const size = Math.random() * 15 + 5;
            p.style.position = 'absolute';
            p.style.width = `${size}px`;
            p.style.height = `${size}px`;
            p.style.background = `radial-gradient(circle, rgba(201,169,110,0.8) 0%, rgba(201,169,110,0) 70%)`;
            p.style.borderRadius = '50%';
            p.style.left = `${mouseX - size/2}px`;
            p.style.top = `${mouseY - size/2}px`;
            p.style.opacity = '1';
            p.style.transform = 'scale(1)';
            p.style.willChange = 'transform, opacity';
            
            cursorContainer.appendChild(p);

            particles.push({
                element: p,
                life: 1,
                dx: (Math.random() - 0.5) * 2,
                dy: (Math.random() - 0.5) * 2 + 1, // slight downward drift
                size: size
            });
        }

        function updateCursorParticles() {
            createCursorParticle();
            
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.life -= 0.03;
                
                if (p.life <= 0) {
                    p.element.remove();
                    particles.splice(i, 1);
                } else {
                    const currentLeft = parseFloat(p.element.style.left);
                    const currentTop = parseFloat(p.element.style.top);
                    p.element.style.left = `${currentLeft + p.dx}px`;
                    p.element.style.top = `${currentTop + p.dy}px`;
                    p.element.style.opacity = p.life;
                    p.element.style.transform = `scale(${p.life * 1.5})`;
                }
            }
            requestAnimationFrame(updateCursorParticles);
        }
        updateCursorParticles();
    }

    // ─── PARALLAX HERO EFFECT ───────────────
    if (!prefersReducedMotion) {
        const heroSection = document.getElementById('home');
        const heroBg = document.querySelector('.hero-bg-img');
        
        if (heroSection && heroBg) {
            // Generate some particle layers in JS to keep HTML clean
            for(let i=0; i<15; i++) {
                const layer = document.createElement('div');
                layer.className = 'parallax-particle';
                const size = Math.random() * 80 + 20;
                layer.style.width = `${size}px`;
                layer.style.height = `${size}px`;
                layer.style.left = `${Math.random() * 100}%`;
                layer.style.setProperty('--duration', `${Math.random() * 20 + 10}s`);
                layer.style.setProperty('--delay', `-${Math.random() * 20}s`);
                layer.style.setProperty('--max-opacity', (Math.random() * 0.4 + 0.1).toString());
                heroSection.appendChild(layer);
            }

            window.addEventListener('scroll', () => {
                const scrollY = window.scrollY;
                if (scrollY < window.innerHeight) {
                    heroBg.style.transform = `translateY(${scrollY * 0.4}px) scale(${1 + scrollY * 0.0005})`;
                }
            }, { passive: true });
        }
    }

    // ─── INTERSECTION OBSERVER FOR ALL REVEALS ───────────────
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -10% 0px',
        threshold: 0.1
    };

    const mainObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                
                if (el.classList.contains('reveal-heading')) {
                    el.classList.add('is-revealed');
                } else if (el.classList.contains('invite-wrapper')) {
                    el.classList.add('unfolded');
                } else if (el.classList.contains('candle-accent')) {
                    el.classList.add('lit');
                } else if (el.classList.contains('signature-container')) {
                    el.classList.add('visible', 'drawn');
                } else {
                    // Generic fade in for cards
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }
                observer.unobserve(el);
            }
        });
    }, observerOptions);

    // 1. Text Reveals
    document.querySelectorAll('h1, h2, h3').forEach(heading => {
        if(heading.closest('.footer-col') || heading.closest('.invite-content-card')) return; // Skip minor headers
        
        heading.classList.add('reveal-heading');
        const text = heading.textContent;
        heading.innerHTML = '';
        
        // Wrap words and chars
        const words = text.split(' ');
        words.forEach((word, wordIndex) => {
            const wordSpan = document.createElement('span');
            wordSpan.className = 'reveal-word';
            
            const chars = word.split('');
            chars.forEach((char, charIndex) => {
                const charSpan = document.createElement('span');
                charSpan.className = 'reveal-char';
                charSpan.textContent = char;
                // Stagger delay based on word and character position
                const delay = (wordIndex * 0.1) + (charIndex * 0.03);
                charSpan.style.transitionDelay = `${delay}s`;
                wordSpan.appendChild(charSpan);
            });
            
            heading.appendChild(wordSpan);
            if(wordIndex < words.length - 1) {
                heading.appendChild(document.createTextNode(' '));
            }
        });
        
        mainObserver.observe(heading);
    });

    // 2. Generic Cards & Elements
    document.querySelectorAll('.service-card, .team-card, .blog-card, .gallery-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(40px)';
        el.style.transition = 'opacity 0.8s ease, transform 0.8s cubic-bezier(0.25, 1, 0.5, 1)';
        mainObserver.observe(el);
    });

    // 3. Candles & Signatures & Invites
    document.querySelectorAll('.candle-accent, .signature-container, .invite-wrapper').forEach(el => {
        mainObserver.observe(el);
    });


    // ─── COUNTERS ───────────────
    let countersAnimated = false;
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !countersAnimated) {
                countersAnimated = true;
                document.querySelectorAll('.stat-number[data-count]').forEach(el => {
                    const target = parseInt(el.getAttribute('data-count'));
                    const duration = 2500;
                    const startTime = performance.now();
                    
                    function update(ts) {
                        const elapsed = ts - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const eased = 1 - Math.pow(1 - progress, 4); // easeOutQuart
                        el.textContent = Math.floor(eased * target);
                        
                        if (progress < 1) requestAnimationFrame(update);
                        else el.textContent = target;
                    }
                    requestAnimationFrame(update);
                });
                statsObserver.disconnect();
            }
        });
    });
    const statsRow = document.querySelector('.stats-row');
    if (statsRow) statsObserver.observe(statsRow);


    // ─── 3D TESTIMONIAL CAROUSEL ───────────────
    const carouselContainer = document.querySelector('.carousel-3d-container');
    if (carouselContainer) {
        // Find existing cards and rebuild them into a 3D track
        const oldCarousel = document.getElementById('testimonialCarousel');
        const cardsData = Array.from(oldCarousel.querySelectorAll('.testimonial-card')).map(card => {
            return {
                stars: card.querySelector('.testimonial-stars').innerHTML,
                text: card.querySelector('.testimonial-text').innerHTML,
                author: card.querySelector('.testimonial-author').innerHTML
            };
        });

        // Replace old structure
        const track = document.createElement('div');
        track.className = 'carousel-3d-track';
        carouselContainer.innerHTML = '';
        carouselContainer.appendChild(track);

        const totalCards = cardsData.length;
        const angleIncrement = 360 / totalCards;
        const radius = 350; // Distance from center

        cardsData.forEach((data, index) => {
            const cardEl = document.createElement('div');
            cardEl.className = 'carousel-3d-card';
            cardEl.innerHTML = `
                <div class="testimonial-stars">${data.stars}</div>
                <p>${data.text}</p>
                <span class="testimonial-author">${data.author}</span>
            `;
            
            // Position radially
            const angle = index * angleIncrement;
            cardEl.style.transform = `rotateY(${angle}deg) translateZ(${radius}px)`;
            track.appendChild(cardEl);
        });

        let currentAngle = 0;
        let carouselInterval;

        function rotateCarousel() {
            currentAngle -= angleIncrement;
            track.style.transform = `rotateY(${currentAngle}deg)`;
        }

        function startCarousel() {
            carouselInterval = setInterval(rotateCarousel, 4000);
        }

        startCarousel();

        carouselContainer.addEventListener('mouseenter', () => clearInterval(carouselInterval));
        carouselContainer.addEventListener('mouseleave', startCarousel);
    }


    // ─── FORM SUBMIT CONFETTI BURST ───────────────
    window.handleSubmit = function (e) {
        e.preventDefault();
        const btn = e.target.querySelector('button[type="submit"]');
        const originalText = btn.textContent;
        
        btn.textContent = 'Sending... 💫';
        btn.disabled = true;
        btn.style.opacity = '0.8';
        
        setTimeout(() => {
            btn.textContent = '✓ Received with Love!';
            btn.style.background = 'var(--gold)';
            btn.style.color = '#fff';
            
            if (!prefersReducedMotion) triggerConfettiBurst(btn);
            
            e.target.reset();
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
                btn.style.color = '';
                btn.disabled = false;
            }, 4000);
        }, 1500);
    };

    function triggerConfettiBurst(element) {
        const rect = element.getBoundingClientRect();
        const startX = rect.left + rect.width / 2;
        const startY = rect.top + rect.height / 2;
        
        const container = document.createElement('div');
        container.className = 'confetti-container';
        document.body.appendChild(container);

        const colors = ['#c9a96e', '#d4a5a5', '#b76e6e', '#ffffff'];
        const shapes = ['burst', 'petal'];
        const petals = ['🌹', '🌸', '✨', '💖'];

        for (let i = 0; i < 50; i++) {
            const piece = document.createElement('div');
            const isPetal = Math.random() > 0.7;
            
            piece.className = `confetti-piece burst ${isPetal ? 'petal' : ''}`;
            
            if (isPetal) {
                piece.textContent = petals[Math.floor(Math.random() * petals.length)];
            } else {
                piece.style.background = colors[Math.floor(Math.random() * colors.length)];
            }

            piece.style.setProperty('--start-x', `${startX}px`);
            piece.style.setProperty('--start-y', `${startY}px`);
            piece.style.setProperty('--end-x', `${startX + (Math.random() - 0.5) * 800}px`);
            piece.style.setProperty('--end-y', `${startY - (Math.random() * 500 + 200)}px`);
            piece.style.setProperty('--rot', `${Math.random() * 720 - 360}deg`);
            
            piece.style.animationDelay = `${Math.random() * 0.2}s`;
            
            container.appendChild(piece);
        }

        setTimeout(() => container.remove(), 4000);
    }

    console.log('💖 The Royal Banquet Palace — Interactive modules loaded successfully! ✨🌹');
})();

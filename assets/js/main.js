(function () {
            // ─── NAVBAR SCROLL EFFECT ───────────────
            const navbar = document.getElementById('navbar');
            const scrollTopBtn = document.getElementById('scrollTopBtn');
            window.addEventListener('scroll', () => {
                const scrolled = window.scrollY > 60;
                navbar.classList.toggle('scrolled', scrolled);
                scrollTopBtn.classList.toggle('visible', window.scrollY > 500);
            });

            // ─── MOBILE MENU ───────────────
            const hamburger = document.getElementById('hamburger');
            const mobileMenu = document.getElementById('mobileMenu');
            const mobileOverlay = document.getElementById('mobileOverlay');
            function toggleMenu() {
                mobileMenu.classList.toggle('active');
                mobileOverlay.classList.toggle('active');
                document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
            }
            hamburger.addEventListener('click', toggleMenu);
            mobileOverlay.addEventListener('click', toggleMenu);
            document.querySelectorAll('.mobile-menu a').forEach(link => {
                link.addEventListener('click', toggleMenu);
            });

            // ─── SCROLL TO TOP ───────────────
            scrollTopBtn.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });

            // ─── FLOATING HEARTS ───────────────
            const heartsContainer = document.getElementById('heartsContainer');
            const heartEmojis = ['♥', '💕', '💖', '✨', '💫', '🌸', '🕊️', '💝', '💗', '🪷', '💞', '💘', '🦢', '🌷', '💐',
                '🕯️', '💓', '🫧'
            ];
            function createHeart() {
                const heart = document.createElement('span');
                heart.className = 'floating-heart';
                heart.textContent = heartEmojis[Math.floor(Math.random() * heartEmojis.length)];
                heart.style.left = Math.random() * 90 + '%';
                heart.style.fontSize = (Math.random() * 1.8 + 0.5) + 'rem';
                heart.style.animationDuration = (Math.random() * 10 + 6) + 's';
                heart.style.animationDelay = Math.random() * 3 + 's';
                heart.style.opacity = (Math.random() * 0.4 + 0.25);
                heartsContainer.appendChild(heart);
                setTimeout(() => heart.remove(), 15000);
            }
            for (let i = 0; i < 22; i++) {
                setTimeout(createHeart, i * 350);
            }
            setInterval(createHeart, 1800);

            // ─── ROSE PETAL FALL ───────────────
            const petalContainer = document.getElementById('petalContainer');
            const petalEmojis = ['🌸', '🌷', '💮', '🪷', '🌺', '🏵️', '💐', '✿', '❀', '🌹'];
            function createPetal() {
                const petal = document.createElement('span');
                petal.className = 'petal';
                petal.textContent = petalEmojis[Math.floor(Math.random() * petalEmojis.length)];
                petal.style.left = Math.random() * 95 + '%';
                petal.style.fontSize = (Math.random() * 1.6 + 0.7) + 'rem';
                petal.style.animationDuration = (Math.random() * 14 + 10) + 's';
                petal.style.animationDelay = Math.random() * 8 + 's';
                petal.style.setProperty('--drift', (Math.random() * 120 - 60) + 'px');
                petal.style.setProperty('--spin', (Math.random() * 360) + 'deg');
                petal.style.opacity = (Math.random() * 0.5 + 0.2);
                petalContainer.appendChild(petal);
                setTimeout(() => petal.remove(), 25000);
            }
            for (let i = 0; i < 12; i++) {
                setTimeout(createPetal, i * 700);
            }
            setInterval(createPetal, 2500);

            // ─── ROMANTIC SPARKLE TRAIL ───────────────
            const sparkleContainer = document.getElementById('sparkleTrailContainer');
            const sparkleEmojis = ['✨', '💫', '⭐', '✧', '⋆', '˚', '✶', '·', '₊', '⊹', '♡', '❋'];
            let sparkleTimeout;
            document.addEventListener('mousemove', function (e) {
                if (window.innerWidth < 768) return;
                if (sparkleTimeout) return;
                sparkleTimeout = setTimeout(() => {
                    sparkleTimeout = null;
                    const sparkle = document.createElement('span');
                    sparkle.className = 'sparkle-trail';
                    sparkle.textContent = sparkleEmojis[Math.floor(Math.random() * sparkleEmojis.length)];
                    sparkle.style.left = e.clientX + 'px';
                    sparkle.style.top = e.clientY + 'px';
                    sparkle.style.fontSize = (Math.random() * 0.9 + 0.5) + 'rem';
                    sparkle.style.setProperty('--dx', (Math.random() * 50 - 25) + 'px');
                    sparkle.style.setProperty('--dy', (Math.random() * -40 - 10) + 'px');
                    sparkleContainer.appendChild(sparkle);
                    setTimeout(() => sparkle.remove(), 1300);
                }, 60);
            });

            // ─── COUNTER ANIMATION ───────────────
            let countersAnimated = false;
            function animateCounters() {
                if (countersAnimated) return;
                const statSection = document.querySelector('.stats-row');
                if (!statSection) return;
                const rect = statSection.getBoundingClientRect();
                if (rect.top < window.innerHeight - 100) {
                    countersAnimated = true;
                    document.querySelectorAll('.stat-number[data-count]').forEach(el => {
                        const target = parseInt(el.getAttribute('data-count'));
                        const duration = 2000;
                        const startTime = performance.now();
                        function update(ts) {
                            const elapsed = ts - startTime;
                            const progress = Math.min(elapsed / duration, 1);
                            const eased = 1 - Math.pow(1 - progress, 3);
                            el.textContent = Math.floor(eased * target);
                            if (progress < 1) requestAnimationFrame(update);
                            else el.textContent = target;
                        }
                        requestAnimationFrame(update);
                    });
                }
            }
            window.addEventListener('scroll', animateCounters);
            animateCounters();

            // ─── GALLERY GENERATION ───────────────
            const galleryGrid = document.getElementById('galleryGrid');
            const galleryColors = [
                '#d4a5a5', '#c8a882', '#b76e6e', '#c9a96e', '#a08060',
                '#d9b8b8', '#c49a6c', '#b08585', '#d1b894', '#c09090',
                '#e0c0a0', '#cc9999', '#bfa080', '#d5aaaa', '#c8a070',
                '#e8d0c0', '#b89090', '#d0b090', '#c88080', '#dac0a0'
            ];
            for (let i = 0; i < 15; i++) {
                const item = document.createElement('div');
                item.className = 'gallery-item';
                const color = galleryColors[i];
                item.innerHTML = `
                    <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'><rect fill='${color}' width='300' height='300'/><circle cx='150' cy='130' r='60' fill='white' opacity='0.25'/><text x='150' y='145' text-anchor='middle' fill='white' font-size='40' font-family='serif'>✦</text><text x='150' y='240' text-anchor='middle' fill='white' font-size='14' font-family='sans-serif'>Royal Moment ${i + 1}</text></svg>"
                    alt="Gallery image ${i + 1}">
                    <div class="gallery-zoom"><i class="fas fa-search-plus"></i></div>
                `;
                item.addEventListener('click', () => {
                    alert('✨ Gallery image ' + (i + 1) +
                        ' — Visit our venue to see the full portfolio in person!');
                });
                galleryGrid.appendChild(item);
            }

            // ─── SMOOTH SCROLL FOR ALL ANCHOR LINKS ───────────────
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    const href = this.getAttribute('href');
                    if (href === '#') return;
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        const offset = 70;
                        const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                        window.scrollTo({ top, behavior: 'smooth' });
                    }
                });
            });

            // ─── CONTACT FORM SUBMISSION ───────────────
            window.handleSubmit = function (e) {
                e.preventDefault();
                const btn = e.target.querySelector('button[type="submit"]');
                const originalText = btn.textContent;
                btn.textContent = 'Sending... 💫';
                btn.disabled = true;
                btn.style.opacity = '0.7';
                setTimeout(() => {
                    btn.textContent = '✓ Message Sent!';
                    btn.style.background = '#4a9e4a';
                    btn.style.borderColor = '#4a9e4a';
                    btn.style.opacity = '1';
                    e.target.reset();
                    setTimeout(() => {
                        btn.textContent = originalText;
                        btn.style.background = '';
                        btn.style.borderColor = '';
                        btn.disabled = false;
                    }, 2500);
                }, 1200);
            };

            // ─── INTERSECTION OBSERVER FOR FADE-IN ───────────────
            const observerOptions = { threshold: 0.12, rootMargin: '0px 0px -30px 0px' };
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            document.querySelectorAll(
                '.service-card, .venture-card, .team-card, .blog-card, .testimonial-card, .gallery-item'
            ).forEach(el => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(30px)';
                el.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
                observer.observe(el);
            });

            // ─── TESTIMONIAL AUTO-SCROLL ───────────────
            const carousel = document.getElementById('testimonialCarousel');
            let scrollInterval;
            function startAutoScroll() {
                scrollInterval = setInterval(() => {
                    if (carousel) {
                        const cardWidth = carousel.querySelector('.testimonial-card')?.offsetWidth || 340;
                        carousel.scrollBy({ left: cardWidth + 32, behavior: 'smooth' });
                        if (carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - 20) {
                            setTimeout(() => carousel.scrollTo({ left: 0, behavior: 'smooth' }), 600);
                        }
                    }
                }, 3500);
            }
            startAutoScroll();
            if (carousel) {
                carousel.addEventListener('mouseenter', () => clearInterval(scrollInterval));
                carousel.addEventListener('mouseleave', startAutoScroll);
                carousel.addEventListener('touchstart', () => clearInterval(scrollInterval), { passive: true });
                carousel.addEventListener('touchend', () => setTimeout(startAutoScroll, 2000));
            }

            console.log('💖 The Royal Banquet Palace — Ready to make your celebration magical! ✨🌹');
        })();

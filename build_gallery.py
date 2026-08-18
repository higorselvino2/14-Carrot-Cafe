import os
import urllib.parse

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Everything before <main>
before_main = html.split('<main>')[0]

# Inject masonry CSS
masonry_css = """
        /* Masonry specific styles */
        .page-header {
            padding: 12rem 5% 5rem;
            text-align: center;
            background-color: var(--color-light);
        }
        .page-header h1 {
            font-size: clamp(3rem, 5vw, 4.5rem);
            color: var(--color-dark);
            margin-bottom: 1rem;
            font-family: var(--font-display);
        }
        .masonry-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 5% 8rem;
        }
        .masonry {
            column-count: 4;
            column-gap: 1.5rem;
        }
        @media (max-width: 1024px) { .masonry { column-count: 3; } }
        @media (max-width: 768px) { .masonry { column-count: 2; } }
        @media (max-width: 480px) { .masonry { column-count: 1; } }
        
        .masonry-item {
            break-inside: avoid;
            margin-bottom: 1.5rem;
            position: relative;
            cursor: pointer;
            border-radius: 4px;
            overflow: hidden;
            background-color: #eee;
            display: inline-block;
            width: 100%;
        }
        .masonry-item img {
            width: 100%;
            height: auto;
            display: block;
            transition: transform 0.5s ease;
        }
        .masonry-item:hover img {
            transform: scale(1.03);
            filter: brightness(0.9);
        }
"""
before_main = before_main.replace('</style>', masonry_css + '\n    </style>')
before_main = before_main.replace('<title>14 Carrot Cafe | Preview Mockup</title>', '<title>Gallery | 14 Carrot Cafe</title>')
before_main = before_main.replace('href="#', 'href="index.html#')

# Extract footer
footer_part = html.split('<footer>')[1].split('</footer>')[0]
footer = f'<footer>{footer_part}</footer>'
footer = footer.replace('href="#', 'href="index.html#')

# Ensure we have the lightbox HTML
lightbox = """
    <!-- Lightbox -->
    <div class="lightbox" id="lightbox" aria-hidden="true" role="dialog">
        <div class="lightbox-img-wrapper">
            <span class="lightbox-close" id="lightbox-close" aria-label="Close lightbox">&times;</span>
            <div class="lightbox-nav lightbox-prev" id="lightbox-prev" aria-label="Previous image">&#10094;</div>
            <img src="" alt="Enlarged gallery view" id="lightbox-img">
            <div class="lightbox-nav lightbox-next" id="lightbox-next" aria-label="Next image">&#10095;</div>
        </div>
    </div>
"""

# Build images
images_dir = 'images'
exclude = ['logo.png', 'logo-branco.png', 'favicon.png', '258824536_10159874792210903_1196380951854388237_n.png']
images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png')) and f not in exclude]
images.sort()

masonry_html = '<div class="masonry">\n'
for i, img in enumerate(images):
    img_url = 'images/' + urllib.parse.quote(img)
    masonry_html += f'                    <div class="masonry-item" data-index="{i}"><img src="{img_url}" loading="lazy" alt="Gallery image {i+1}"></div>\n'
masonry_html += '                </div>'

gallery_main = f"""
    <main>
        <section class="page-header">
            <span class="eyebrow" style="color:var(--color-primary);">Full Collection</span>
            <h1>Gallery</h1>
            <p style="color: #666; max-width: 600px; margin: 0 auto; font-size: 1.1rem;">A visual taste of our neighborhood tradition. Explore our space, our community, and our favorite dishes.</p>
            <a href="index.html" class="btn btn-outline-dark" style="margin-top: 2.5rem;">Back to Home</a>
        </section>

        <section class="masonry-container">
            {masonry_html}
        </section>
    </main>
"""

scripts = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            /* --- HEADER & SCROLL --- */
            const header = document.getElementById('main-header');
            const progressBar = document.getElementById('scroll-progress');
            
            if (header) {
                header.classList.add('scrolled');
                header.style.backgroundColor = 'var(--color-light)';
            }
            
            window.addEventListener('scroll', () => {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                if (progressBar) progressBar.style.width = (winScroll / height) * 100 + "%";
            });

            /* --- MOBILE MENU --- */
            const hamburger = document.getElementById('hamburger');
            const mobileMenu = document.getElementById('mobile-menu');
            const mobLinks = document.querySelectorAll('.mob-link');

            function toggleMenu() {
                if (!mobileMenu) return;
                const isActive = mobileMenu.classList.contains('active');
                mobileMenu.classList.toggle('active');
                if (hamburger) {
                    hamburger.classList.toggle('active');
                    hamburger.setAttribute('aria-expanded', !isActive);
                }
                document.body.style.overflow = isActive ? 'auto' : 'hidden';
            }

            if (hamburger) hamburger.addEventListener('click', toggleMenu);
            if (mobLinks) mobLinks.forEach(link => link.addEventListener('click', toggleMenu));

            /* --- LIGHTBOX W/ NAVIGATION --- */
            const lightbox = document.getElementById('lightbox');
            const lbImg = document.getElementById('lightbox-img');
            const galleryItems = document.querySelectorAll('.masonry-item');
            let currentImgIndex = 0;
            const imagesSrc = Array.from(galleryItems).map(item => item.querySelector('img').src);

            function openLightbox(index) {
                currentImgIndex = index;
                if (lbImg) lbImg.src = imagesSrc[currentImgIndex];
                if (lightbox) {
                    lightbox.classList.add('active');
                    lightbox.setAttribute('aria-hidden', 'false');
                }
                document.body.style.overflow = 'hidden';
            }

            function closeLightbox() {
                if (lightbox) {
                    lightbox.classList.remove('active');
                    lightbox.setAttribute('aria-hidden', 'true');
                }
                document.body.style.overflow = 'auto';
            }

            function navLightbox(direction) {
                currentImgIndex = (currentImgIndex + direction + imagesSrc.length) % imagesSrc.length;
                if (lbImg) lbImg.src = imagesSrc[currentImgIndex];
            }

            galleryItems.forEach((item, index) => {
                item.addEventListener('click', () => openLightbox(index));
            });

            if(document.getElementById('lightbox-close')) document.getElementById('lightbox-close').addEventListener('click', closeLightbox);
            if(document.getElementById('lightbox-prev')) document.getElementById('lightbox-prev').addEventListener('click', (e) => { e.stopPropagation(); navLightbox(-1); });
            if(document.getElementById('lightbox-next')) document.getElementById('lightbox-next').addEventListener('click', (e) => { e.stopPropagation(); navLightbox(1); });
            
            if(lightbox) lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) closeLightbox();
            });

            document.addEventListener('keydown', (e) => {
                if (!lightbox || !lightbox.classList.contains('active')) return;
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowLeft') navLightbox(-1);
                if (e.key === 'ArrowRight') navLightbox(1);
            });
        });
    </script>
</body>
</html>
"""

final_html = before_main + gallery_main + footer + lightbox + scripts

with open('gallery.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove CSS
html = re.sub(r'\s*/\*\s*---\s*INTRO ANIMATION\s*---\s*\*/.*?/\*\s*---\s*HERO SECTION\s*---\s*\*/', r'\n\n        /* --- HERO SECTION --- */', html, flags=re.DOTALL)

# Remove HTML
html = re.sub(r'\s*<!-- Intro Animation -->.*?</div>\s*(?=<!-- Header -->)', r'\n\n    ', html, flags=re.DOTALL)

# Remove JS
# In the JS, the intro block is:
# /* --- INTRO & PERFORMANCE --- */
# ... code ...
# /* --- HEADER & SCROLL --- */
html = re.sub(r'\s*/\*\s*---\s*INTRO & PERFORMANCE\s*---\s*\*/.*?/\*\s*---\s*HEADER', r'\n            /* --- HEADER', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import re
html = open('index.html', encoding='utf-8').read()
m1 = re.search(r'<header id="main-header">.*?</header>', html, re.DOTALL)
print("header:", len(m1.group(0)) if m1 else 'none')

m2 = re.search(r'<div class="mobile-menu.*?</div>\n', html, re.DOTALL)
print("mobile_menu:", len(m2.group(0)) if m2 else 'none')

m3 = re.search(r'<footer>.*?</footer>', html, re.DOTALL)
print("footer:", len(m3.group(0)) if m3 else 'none')

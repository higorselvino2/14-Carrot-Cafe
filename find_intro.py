import re
html = open('index.html', encoding='utf-8').read()

idx = html.find('id="intro-overlay"')
if idx != -1:
    print(html[max(0, idx-100):idx+500])
else:
    print("intro-overlay HTML not found")

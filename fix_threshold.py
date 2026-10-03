with open('js/main.js', encoding='utf-8') as f:
    js = f.read()

js = js.replace('threshold: 0.12', 'threshold: 0.04')

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('threshold fixed:', 'threshold: 0.04' in js)

import re

with open('index.html', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the entire portrait-upload-overlay div block
content = re.sub(
    r'\s*<div class="portrait-upload-overlay">.*?</div>\s*(?=</div>\s*</div>)',
    '',
    content,
    flags=re.DOTALL
)

# 2. Replace old portrait wrapper with new premium frame structure
old_wrap_start = '            <div class="portrait-card-wrap">'
old_wrap_end   = '          </div>\n        </div>\n\n      </div>\n    </div>\n  </section>'

# Find and replace the portrait section
# Replace editorial-frame-container with portrait-premium-frame
content = content.replace(
    '          <div class="editorial-frame-container">\n            <div class="portrait-card-wrap">',
    '          <div class="portrait-premium-frame">'
)

# Fix old floating-badge-top class
content = content.replace(
    '<div class="floating-badge floating-badge-top">',
    '<div class="floating-badge">'
)

# Close new structure - find old closing divs pattern
# Old: portrait-card > portrait-image-wrapper > img (now no overlay) ...closed by portrait-card-wrap, editorial-frame
old_close = '              </div>\n\n            </div>\n          </div>\n        </div>\n\n      </div>'
new_close = '''              </div>
            <!-- Gold corner brackets -->
            <span class="corner tl"></span>
            <span class="corner tr"></span>
            <span class="corner bl"></span>
            <span class="corner br"></span>
          </div>
        </div>

      </div>'''

content = content.replace(old_close, new_close, 1)

# 3. Remove scroll-to-top button
content = re.sub(
    r'\n\n  <!-- =+\s*Scroll To Top\s*=+ -->\s*<button class="scroll-top-btn"[^>]*>.*?</button>',
    '',
    content,
    flags=re.DOTALL
)

# 4. Fix toast message text
content = content.replace(
    '>Done!</span>',
    '></span>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched OK')
print('premium-frame present:', 'portrait-premium-frame' in content)
print('upload-overlay present:', 'portrait-upload-overlay' in content)
print('scroll-top present:', 'scroll-top-btn' in content)

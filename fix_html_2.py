import re
with open('index.html', encoding='utf-8') as f:
    html = f.read()

CONTACT_HEADLINE = """      <!-- Oversized editorial contact headline -->
      <h2 class="contact-headline reveal">
        Let's <em>Build</em><br>Something.
      </h2>\n\n"""

if 'contact-headline' not in html:
    html = html.replace('<div class="contact-separated-layout">', CONTACT_HEADLINE + '      <div class="contact-separated-layout">')

def restructure_card(m):
    card = m.group(0)
    if 'proj-content' in card: return card
    preview_match = re.search(r'(<a class="student-project-preview".*?</a>)', card, re.DOTALL)
    if not preview_match: return card
    preview_end_idx = preview_match.end()
    
    preview_html = card[:preview_end_idx]
    rest = card[preview_end_idx:-12]
    
    rest = rest.replace('<p>', '<p class="proj-description">')
    
    return preview_html + '\n      <div class="proj-content">' + rest + '\n      </div>\n    ' + card[-12:]

html = re.sub(r'<article class="student-project-card".*?</article>', restructure_card, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML patched successfully")

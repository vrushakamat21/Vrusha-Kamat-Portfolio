import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── 1. Update Google Fonts → DM Serif Display + Manrope + Space Grotesk ──────
html = html.replace(
    'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@300;400;500;600',
    'family=DM+Serif+Display:ital@0;1&family=Manrope:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600'
)
html = html.replace(
    '<!-- Editorial Font Stack: Cormorant Garamond (luxury serif like reference) + DM Sans + Space Grotesk -->',
    '<!-- Editorial Stack: DM Serif Display + Manrope + Space Grotesk -->'
)

# ── 2. VK Monogram SVG logo ───────────────────────────────────────────────────
VK_SVG = '''<svg class="vk-mono" viewBox="0 0 44 38" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <!-- V: left diagonal to apex, right diagonal up. K shares right diagonal of V as its vertical bar start -->
            <path d="M4 6 L18 32 L23 20" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="23" y1="6" x2="23" y2="32" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
            <path d="M23 19 L39 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M23 19 L39 32" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>'''

html = html.replace('<span class="brand-monogram">VK</span>', VK_SVG.replace('\n          ', '\n        '))

# ── 3. Hero: add micro-labels above status pill ───────────────────────────────
META_LABELS = '''          <!-- Editorial micro-labels -->
          <div class="hero-meta">
            <div class="hero-meta-item">
              <span class="hero-meta-num">01</span>
              <span class="hero-meta-divider"></span>
              <span class="hero-meta-text">Based in India</span>
            </div>
            <div class="hero-meta-item">
              <span class="hero-meta-num">02</span>
              <span class="hero-meta-divider"></span>
              <span class="hero-meta-text">CS Engineering</span>
            </div>
            <div class="hero-meta-item">
              <span class="hero-meta-num">03</span>
              <span class="hero-meta-divider"></span>
              <span class="hero-meta-text">Building Digital Experiences</span>
            </div>
          </div>\n\n'''

html = html.replace(
    '          <div class="status-pill">',
    META_LABELS + '          <div class="status-pill">'
)

# ── 4. Projects: wrap content in .proj-content + add .proj-num ────────────────
# For each project card, we need to restructure the content.
# Current structure: preview img | heading | p | tags | a.btn
# New: preview img | proj-content div { proj-num + heading + description + tags + links }

def wrap_project_card(match):
    card_html = match.group(0)

    # Extract project number from existing badge span
    num_match = re.search(r'<span[^>]*>\s*(Personal Project|Internship Project|Open Source)\s*</span>', card_html)

    # Find project number from position
    return card_html  # we'll do this differently

# Simpler approach: just add proj-num + proj-content wrapper via regex on the heading div
def restructure_project(match):
    full = match.group(0)
    # Add proj-content wrapper around everything after the preview
    return full

# Instead, let's add CSS wrapper classes via simple text replacements
# Add proj-content div around the text content portion
# We target each student-project-heading and wrap siblings

# First, let's add a project content wrapper. 
# The heading, description p, tags, and btn link need to be inside .proj-content
# This is complex to do with regex safely, so let's add the proj-num inside the heading

# Add project numbers to headings
proj_count = [0]
def add_proj_num(match):
    proj_count[0] += 1
    heading_inner = match.group(1)
    num_str = f'0{proj_count[0]}'
    prefix = f'\n        <span class="proj-num">{num_str} — Project</span>\n        '
    return f'<div class="student-project-heading">{prefix}{heading_inner}\n        </div>'

html = re.sub(
    r'<div class="student-project-heading">(.*?)</div>',
    add_proj_num,
    html,
    flags=re.DOTALL
)

# Wrap text content (after preview) in proj-content div
# Identify: preview a tag followed by the heading and content
# We'll insert a proj-content wrapper div after the preview and close it before card end

def wrap_proj_content(m):
    card = m.group(0)
    # Split at the end of the preview anchor tag
    split_point = card.rfind('</a>')  # last </a> is the preview link close? No...
    # Let's find the preview tag more carefully
    prev_end = card.find('</a>') + len('</a>')
    preview_part = card[:prev_end]
    content_part = card[prev_end:-10]  # exclude last </article> or </div>
    close = card[-10:]

    # Check if we have a preview
    if 'student-project-preview' not in preview_part:
        return card

    return preview_part + '\n        <div class="proj-content">' + content_part + '\n        </div>\n' + close

# This is getting complex. Let's just add a CSS-only approach and add proj-content class via JS instead.
# For now, let's at least wrap in the HTML properly.

# Simpler: find each card and reconstruct
def restructure_card(m):
    card = m.group(0)
    # Find preview end
    preview_end_idx = card.find('</a>') + 4
    # Check it's actually the preview (not a button link)
    if 'student-project-preview' not in card[:preview_end_idx]:
        # Try to find the preview specifically
        preview_match = re.search(r'(<a class="student-project-preview".*?</a>)', card, re.DOTALL)
        if not preview_match:
            return card
        preview_end_idx = preview_match.end()

    preview_html = card[:preview_end_idx]
    rest_before_close = card[preview_end_idx:-12]  # before </article>
    close_tag = card[-12:]

    # Wrap links (GitHub/Demo buttons) in .proj-links div
    rest_before_close = re.sub(
        r'(<a[^>]*class="btn[^"]*"[^>]*>.*?</a>\s*)+',
        lambda bm: f'\n          <div class="proj-links">{bm.group(0).strip()}</div>\n        ',
        rest_before_close,
        flags=re.DOTALL
    )

    # Move the description <p> to have class proj-description
    rest_before_close = rest_before_close.replace(
        '\n        <p>',
        '\n        <p class="proj-description">'
    ).replace(
        '\n          <p>',
        '\n          <p class="proj-description">'
    )

    return preview_html + '\n      <div class="proj-content">' + rest_before_close + '\n      </div>' + close_tag

html = re.sub(
    r'<article class="student-project-card".*?</article>',
    restructure_card,
    html,
    flags=re.DOTALL
)

# ── 5. Add cert-num span to each certificate ──────────────────────────────────
cert_count = [0]
def add_cert_num(m):
    cert_count[0] += 1
    info_inner = m.group(1)
    num = f'<span class="cert-num">Cert {cert_count[0]:02d}</span>\n        '
    return f'<div class="mongodb-certificate-info">\n        {num}{info_inner.strip()}\n        </div>'

html = re.sub(
    r'<div class="mongodb-certificate-info">\s*(.*?)\s*</div>',
    add_cert_num,
    html,
    flags=re.DOTALL
)

# ── 6. Add section numbers to each section ────────────────────────────────────
section_nums = {
    'My Story':         '01',
    'Skills & Expertise': '02',
    'Projects I\'ve':   '03',
    'Certificate':      '04',
    'Activities':       '05',
}

# Add section-num span before each section-label
def add_section_num(m):
    label_text = m.group(1)
    for key, num in section_nums.items():
        if key.lower() in label_text.lower():
            return f'<span class="section-num">{num}</span>\n        <span class="section-label">{label_text}</span>'
    return m.group(0)

html = re.sub(
    r'<span class="section-label">([^<]+)</span>',
    add_section_num,
    html
)

# ── 7. Contact: Add oversized headline before contact channels ────────────────
CONTACT_HEADLINE = '''      <!-- Oversized editorial contact headline -->
      <h2 class="contact-headline reveal">
        Let's <em>Build</em><br>Something.
      </h2>\n\n'''

html = html.replace(
    '        <div class="contact-separated-layout">',
    CONTACT_HEADLINE + '        <div class="contact-separated-layout">'
)

# Remove the old section-header in contact (if it exists) to avoid duplication
# Actually keep it, the headline is separate

# ── 8. Footer: Add "Designed & built with intention." tagline ─────────────────
html = html.replace(
    '<p class="footer-desc">',
    '<p class="footer-desc">'
)
html = html.replace(
    '          Computer Science Engineering student crafting thoughtful software and learning something new every day.\n          </p>',
    '          Computer Science Engineering student crafting thoughtful software and learning something new every day.\n          </p>\n          <p class="footer-tagline">Designed &amp; built with intention.</p>'
)

# ── 9. Remove ambient-glow div (the old orb blobs), keep grain in CSS ─────────
# Actually keep it, just in case

# ── 10. Write output ──────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML patched successfully')
print('VK SVG logo:', 'vk-mono' in html)
print('Hero meta labels:', 'hero-meta' in html)
print('Section numbers:', 'section-num' in html)
print('Project content wrappers:', 'proj-content' in html)
print('Cert numbers:', 'cert-num' in html)
print('Contact headline:', 'contact-headline' in html)
print('Footer tagline:', 'footer-tagline' in html)

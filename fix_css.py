import re
with open('css/style.css', encoding='utf-8') as f:
    css = f.read()

# 1. Update text gradients for premium feel (Champagne/Gold to Rose)
gradient_css = """
.name-first {
  display: block; 
  background: linear-gradient(135deg, var(--t0) 0%, var(--a) 60%, var(--t0) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-size: 200% auto;
  animation: shineText 6s linear infinite;
}
.name-last {
  display: block; font-style: italic; font-size: .78em;
  background: linear-gradient(135deg, var(--t1) 0%, var(--a) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.section-title em, .contact-headline em {
  font-style: italic; 
  background: linear-gradient(135deg, var(--a) 0%, var(--t0) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
@keyframes shineText { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
"""

css = css.replace('.name-first { display: block; color: var(--t0); }', gradient_css)
css = css.replace('.name-last { display: block; font-style: italic; color: var(--t1); font-size: .78em; }', '')
css = css.replace('.section-title em { font-style: italic; color: var(--t1); }', '')
css = css.replace('.contact-headline em { font-style: italic; color: var(--t1); }', '')


# 2. Add Floating and Glow Animation to the portrait
portrait_css = """
.hero-portrait-showcase { 
  flex-shrink: 0; 
  animation: fadeIn 1s var(--ease) .5s both, floatImage 6s ease-in-out infinite .5s; 
}
@keyframes floatImage { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }

.portrait-premium-frame { 
  position: relative; display: inline-block; 
}
.portrait-premium-frame::before {
  content: ''; position: absolute; inset: -10px;
  background: radial-gradient(circle, var(--a-mid) 0%, transparent 70%);
  filter: blur(20px); z-index: -1;
  animation: pulseGlow 4s ease-in-out infinite alternate;
}
@keyframes pulseGlow { 0% { opacity: 0.5; transform: scale(0.9); } 100% { opacity: 1; transform: scale(1.1); } }
"""

css = css.replace(
    '.hero-portrait-showcase { flex-shrink: 0; animation: fadeIn 1s var(--ease) .5s both; }',
    portrait_css
).replace('.portrait-premium-frame { position: relative; display: inline-block; }', '')

# 3. Add Premium Hover Shimmer to ALL cards (About, Skills, Projects, Certs)
shimmer_css = """
.about-card::after, .skill-category-card::after, .timeline-card::after, .mongodb-certificate-card::after, .contact-item::after {
  content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
  background: linear-gradient(to right, transparent, rgba(255,255,255,0.03), transparent);
  transform: skewX(-20deg); transition: left 0.7s var(--ease); pointer-events: none;
}
[data-theme="light"] .about-card::after, [data-theme="light"] .skill-category-card::after, [data-theme="light"] .timeline-card::after, [data-theme="light"] .mongodb-certificate-card::after, [data-theme="light"] .contact-item::after {
  background: linear-gradient(to right, transparent, rgba(0,0,0,0.03), transparent);
}
.about-card:hover::after, .skill-category-card:hover::after, .timeline-card:hover::after, .mongodb-certificate-card:hover::after, .contact-item:hover::after {
  left: 200%;
}
"""

css += shimmer_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("CSS patched for premium animations and typography")

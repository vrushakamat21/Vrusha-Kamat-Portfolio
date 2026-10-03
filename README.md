# Vrusha Kamat — Premium Developer Portfolio

A highly customized, premium editorial-style personal portfolio website built from scratch. Designed to showcase projects, skills, and academic achievements with a modern, cinematic aesthetic.

![Portfolio Preview](./assets/profile.jpg) 

## ✨ Features

- **Editorial Aesthetic:** Custom geometric Arch layouts, thin metallic wireframes, and asymmetric grid structures.
- **Cinematic Dark/Light Mode:** Seamless theme switching with state saved in `localStorage`. Defaults to a deep graphite and champagne gold palette.
- **Micro-Interactions & Animations:** 
  - Floating image effects with pulsing aura glows.
  - Glassmorphism shimmer sweeps on card hovers.
  - Dynamic button press (`:active`) states and gradient typography.
- **Zero-Dependency Architecture:** Built entirely without external heavy frameworks (No React, No npm, No Tailwind).
- **Responsive Design:** Fluidly adapts from large desktop layouts to clean, single-column mobile views.
- **Custom UI Components:** Includes a built-in Modal system, Toast notification system, and ScrollSpy navigation.

## 🛠️ Tech Stack

**Frontend:**
- Semantic **HTML5**
- Modern **CSS3** (CSS Variables, Grid, Flexbox, Keyframe Animations)
- **Vanilla JavaScript** (Intersection Observers, DOM Manipulation)

**Backend / Local Server:**
- **Java 25** (Custom lightweight multi-threaded HTTP Server for local hosting)

FOLDER STRUCTURE:
├── assets/             # Images, icons, and PDF resume
├── css/
│   └── style.css       # Core styling, responsive design, animations
├── js/
│   └── main.js         # Theme toggling, observers, modals, toasts
├── index.html          # Main portfolio layout and content
└── PortfolioServer.java# Custom local Java HTTP server

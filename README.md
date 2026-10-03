# Vrusha Kamat — Personal Portfolio Website
*Modern, Editorial, Premium Web Portfolio for Computer Science Engineering*

---

## ✨ Features & Highlights

- **Editorial Aesthetic:** Designed with refined typography (`Cormorant Garamond` serif + `Plus Jakarta Sans` + `Space Grotesk` monospace), spacious whitespace, subtle hairline borders, and ambient background glow.
- **🌓 Dual Theme (Light & Dark):**
  - **Light Theme:** Warm ivory/alabaster background, dark charcoal text, muted burgundy/rose accents (`#9E475A`), soft shadows.
  - **Dark Theme:** Deep obsidian background (`#0D0B0C`), luminous text, glowing rose accents (`#D98295`), and backdrop blurs.
  - Theme choice automatically persists in `localStorage` and respects system preferences.
- **🖼️ Interactive Photo Uploader & Editorial Frame:**
  - Includes a stylish editorial portrait frame with monogram initials and floating degree badges.
  - In-browser "Upload Photo" button previews your photo instantly and persists in local storage.
  - **Permanent image replacement:** Simply save your portrait as `assets/profile.jpg`!
- **📄 Resume Integration:**
  - "Download Resume" downloads `assets/resume.pdf` directly.
  - "View Resume" opens an interactive, printable modal formatted with your academic and engineering details.
- **💻 Interactive Projects Section:**
  - Category filters: **All**, **Full Stack**, **Web Apps**, **Algorithms & AI**, **Systems**.
  - 6 realistic engineering projects with architecture breakdowns, tech pills, GitHub buttons, and live sandbox preview modals.
- **📜 Certificates Gallery:**
  - Five MongoDB learning certificates, a Buildathon certificate, and an ElectroHack participation certificate.
  - Click any certificate image to open the full-size file.
- **⏳ Vertical Experience Timeline:**
  - Glowing timeline nodes, organization cards, impact metrics, and technology badges.
- **✉️ Interactive Contact Section:**
  - Direct contact cards (Email, LinkedIn, GitHub, Location).
  - Working validated contact form with real-time feedback, loading states, and celebratory confirmation toast notifications.
- **📱 Fully Responsive & Accessible:**
  - Fluid layouts for Mobile, Tablet, Laptop, and 4K Displays.
  - Smooth mobile slide-out drawer menu.

- **☕ Java Backend Integration (HTML + CSS + Java):**
  - Includes a zero-dependency **Java HTTP Web Server and REST API** (`PortfolioServer.java`) written in standard Java.
  - Serves static HTML/CSS/assets and provides live endpoints:
    - `GET  /api/health` — Reports server health, Java runtime version, and uptime.
    - `GET  /api/stats` — Reports portfolio metrics and received message counts.
    - `POST /api/contact` — Validates and logs messages to persistent `messages.json`.
    - `GET  /api/messages` — Retrieves stored messages.
  - Features smart port detection (tries `8080`, `8000`, `8081` automatically).
  - Can be started with a single command: `java PortfolioServer` or double-clicking `run.bat`!

---

## 📁 File Structure

```
├── index.html                   # Master semantic HTML structure
├── css/
│   └── style.css                # CSS design system, themes, and responsive rules
├── js/
│   └── main.js                  # Frontend controller & Java API integration
├── PortfolioServer.java         # Native Java HTTP Server & REST API backend
├── run.bat                      # One-click Windows runner script
├── run.sh                       # One-click macOS / Linux runner script
├── messages.json                # Persistent JSON storage for contact inquiries
├── assets/
│   ├── profile-placeholder.svg  # Default editorial portrait SVG
│   ├── profile.jpg              # Portfolio portrait
│   ├── mongodb c1.jpeg          # MongoDB Basics for Students certificate
│   ├── mongodb c2.jpeg          # AI Data Strategy with MongoDB certificate
│   ├── mongodb c3.jpeg          # RAG with MongoDB certificate
│   ├── mongodb c4.jpeg          # Vector Search Fundamentals certificate
│   ├── mongodb c5.jpeg          # AI Agents with MongoDB certificate
│   ├── buildathon-certificate.pdf
│   ├── buildathon-certificate-preview.png
│   ├── Hackathon certificate.jpeg
│   ├── project-apiverse.png     # APIverse project preview
│   ├── project-taskflow.png     # TaskFlow project preview
│   ├── project-velora.png       # Velora project preview
│   └── resume.pdf               # Downloadable PDF resume
└── README.md                    # Documentation & customization guide
```

---

## 🚀 How to Run (HTML, CSS & Java)

### Option 1: Running with the Java Backend (Recommended)
1. **Windows (One-Click):**
   - Double-click [`run.bat`](file:///d:/Vrusha%20Kamat%20Portfolio/run.bat).
2. **Terminal / Command Prompt:**
   ```bash
   javac PortfolioServer.java
   java PortfolioServer
   ```
   Or directly with Java 11+:
   ```bash
   java PortfolioServer.java
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:8000/
   ```
   *(or `http://localhost:8080/` if port 8080 is available)*.

### Option 2: Running Directly as Static Web Files
- You can also double-click [`index.html`](file:///d:/Vrusha%20Kamat%20Portfolio/index.html) to open it directly in Chrome, Edge, Safari, or Firefox without any server. The frontend gracefully handles all features even when offline.

---

## 🛠️ How to Customize Your Portfolio

### 1. Change Your Personal Photo
- **Quick In-Browser:** Click the "Upload Photo" button on the portrait in the hero section to immediately preview any photo from your computer.
- **Permanent:** Save your picture as `assets/profile.jpg` and update line 186 in `index.html`:
  ```html
  <img src="assets/profile.jpg" alt="Vrusha Kamat Portrait" class="portrait-img" id="main-portrait-img" />
  ```

### 2. Replace the Resume PDF
- Replace `assets/resume.pdf` with your actual PDF resume (keeping the same filename `assets/resume.pdf`), or change the `href` in `index.html` to point to your new filename.

### 3. Add or Edit Projects
Each project in `index.html` is wrapped in an `<article class="project-card">` with simple `data-*` attributes for easy customization:
```html
<article class="project-card"
  data-category="fullstack webapp"
  data-title="Your Project Name"
  data-category-label="Full-Stack Web App"
  data-full-desc="A detailed description of your project."
  data-tech="React, Node.js, PostgreSQL"
  data-highlights="Reduced latency by 35% through custom caching."
  data-github="https://github.com/yourusername/project"
  data-live="https://yourdemo.com">
```

### 4. Update Contact Links
In `index.html` under the `#contact` section, update your email, LinkedIn URL, and GitHub handle.

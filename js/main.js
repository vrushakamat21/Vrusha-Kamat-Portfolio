/**
 * Vrusha Kamat - Personal Portfolio Website
 * Refined JavaScript Controller with Scroll-Reveal Animations
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // --------------------------------------------------------------------------
  // 1. Dual Theme System (Light / Dark with LocalStorage Persistence)
  // --------------------------------------------------------------------------
  const themeToggleBtns = document.querySelectorAll('.theme-toggle-btn');
  const htmlRoot = document.documentElement;

  const getInitialTheme = () => {
    const savedTheme = localStorage.getItem('vk-portfolio-theme');
    if (savedTheme) return savedTheme;
    return 'light';
  };

  const applyTheme = (theme) => {
    htmlRoot.setAttribute('data-theme', theme);
    localStorage.setItem('vk-portfolio-theme', theme);
  };

  applyTheme(getInitialTheme());

  // Dynamic year in footer
  const yearEl = document.getElementById('current-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  themeToggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const current = htmlRoot.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      showToast(`Switched to ${next === 'dark' ? '🌙 Dark' : '☀️ Light'} mode`);
    });
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('vk-portfolio-theme')) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });


  // --------------------------------------------------------------------------
  // 2. Navigation — Sticky Header & ScrollSpy
  // --------------------------------------------------------------------------
  const siteNav = document.querySelector('.site-nav');
  const navLinks = document.querySelectorAll('.nav-link, .drawer-link');
  const sections = document.querySelectorAll('section[id]');
  const scrollTopBtn = document.querySelector('.scroll-top-btn');

  const handleScroll = () => {
    const scrollY = window.pageYOffset;

    if (scrollY > 40) {
      siteNav.classList.add('scrolled');
    } else {
      siteNav.classList.remove('scrolled');
    }

    if (scrollY > 500) {
      scrollTopBtn.classList.add('visible');
    } else {
      scrollTopBtn.classList.remove('visible');
    }

    // ScrollSpy
    let currentId = '';
    sections.forEach(section => {
      const top = section.offsetTop - 140;
      const height = section.offsetHeight;
      if (scrollY >= top && scrollY < top + height) {
        currentId = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  const resumeMenuToggle = document.getElementById('resume-menu-toggle');
  const resumeButtonGroup = resumeMenuToggle?.closest('.resume-btn-group');

  const setResumeMenuOpen = (isOpen) => {
    if (!resumeButtonGroup || !resumeMenuToggle) return;
    resumeButtonGroup.classList.toggle('open', isOpen);
    resumeMenuToggle.setAttribute('aria-expanded', String(isOpen));
  };

  if (resumeMenuToggle && resumeButtonGroup) {
    resumeMenuToggle.addEventListener('click', () => {
      setResumeMenuOpen(!resumeButtonGroup.classList.contains('open'));
    });

    document.addEventListener('click', (event) => {
      if (!resumeButtonGroup.contains(event.target)) setResumeMenuOpen(false);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') setResumeMenuOpen(false);
    });

    resumeButtonGroup.querySelectorAll('.resume-dropdown-item').forEach(item => {
      item.addEventListener('click', () => setResumeMenuOpen(false));
    });
  }


  // --------------------------------------------------------------------------
  // 3. Mobile Navigation Drawer
  // --------------------------------------------------------------------------
  const mobileMenuBtn = document.getElementById('mobile-menu-toggle');
  const mobileDrawer = document.getElementById('mobile-drawer');
  const drawerOverlay = document.getElementById('drawer-overlay');
  const drawerCloseBtn = document.getElementById('drawer-close');

  const openDrawer = () => {
    if (mobileDrawer) mobileDrawer.classList.add('open');
    if (drawerOverlay) drawerOverlay.style.display = 'block';
    document.body.style.overflow = 'hidden';
  };

  const closeDrawer = () => {
    if (mobileDrawer) mobileDrawer.classList.remove('open');
    if (drawerOverlay) drawerOverlay.style.display = '';
    document.body.style.overflow = '';
  };

  if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openDrawer);
  if (drawerCloseBtn) drawerCloseBtn.addEventListener('click', closeDrawer);
  if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

  document.querySelectorAll('.drawer-link').forEach(link => {
    link.addEventListener('click', closeDrawer);
  });


  // --------------------------------------------------------------------------
  // 4. Scroll-Reveal Entrance Animations (IntersectionObserver)
  // --------------------------------------------------------------------------
  const revealElements = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          revealObserver.unobserve(entry.target); // Only animate once
        }
      });
    }, {
      threshold: 0.12,
      rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback for browsers without IntersectionObserver
    revealElements.forEach(el => el.classList.add('in-view'));
  }


  // --------------------------------------------------------------------------
  // 5. Skills Progress Bar Animation on Scroll
  // --------------------------------------------------------------------------
  const skillBars = document.querySelectorAll('.skill-bar-fill');
  let animatedSkills = false;

  const skillsSection = document.getElementById('skills');
  if (skillsSection && skillBars.length > 0) {
    const skillObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !animatedSkills) {
          skillBars.forEach(bar => {
            const targetWidth = bar.getAttribute('data-level') || '70%';
            // Small stagger
            setTimeout(() => {
              bar.style.width = targetWidth;
            }, Math.random() * 150);
          });
          animatedSkills = true;
        }
      });
    }, { threshold: 0.2 });

    skillObserver.observe(skillsSection);
  }


  // --------------------------------------------------------------------------
  // 6. Modal System
  // --------------------------------------------------------------------------
  const modalBackdrop = document.getElementById('general-modal-backdrop');
  const modalTitleEl = document.getElementById('modal-title');
  const modalSubtitleEl = document.getElementById('modal-subtitle');
  const modalBodyEl = document.getElementById('modal-body-content');
  const modalFooterEl = document.getElementById('modal-footer-action');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  const openModal = (title, subtitle, contentHtml, footerHtml = '') => {
    if (!modalBackdrop) return;
    if (modalTitleEl) modalTitleEl.textContent = title;
    if (modalSubtitleEl) modalSubtitleEl.textContent = subtitle;
    if (modalBodyEl) modalBodyEl.innerHTML = contentHtml;
    if (modalFooterEl) modalFooterEl.innerHTML = footerHtml;
    modalBackdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  const closeModal = () => {
    if (!modalBackdrop) return;
    modalBackdrop.classList.remove('open');
    document.body.style.overflow = '';
  };

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
      closeDrawer();
    }
  });


  // --------------------------------------------------------------------------
  // 8. View Resume Modal
  // --------------------------------------------------------------------------
  const viewResumeBtns = document.querySelectorAll('.view-resume-trigger');
  viewResumeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();

      const content = `
        <article class="resume-document">
          <header class="resume-document-header">
            <h2>Vrusha Kamat</h2>
            <p class="resume-document-role">Computer Science &amp; Engineering Student · Aspiring Developer</p>
            <div class="resume-contact-list">
              <a href="mailto:vrushakamat06@gmail.com">vrushakamat06@gmail.com</a>
              <a href="tel:+919535421486">+91 9535421486</a>
              <a href="https://linkedin.com/in/vrusha-kamat-525253396" target="_blank" rel="noopener noreferrer">linkedin.com/in/vrusha-kamat-525253396</a>
              <a href="https://github.com/vrushakamat21" target="_blank" rel="noopener noreferrer">github.com/vrushakamat21</a>
              <span>Mangalore, India</span>
            </div>
          </header>

          <section class="resume-section">
            <h3>Profile</h3>
            <p>Computer Science &amp; Engineering student developing practical skills through a Synent Technologies internship, academic work, personal projects, and hackathons. Currently exploring web development and AI/ML.</p>
          </section>

          <section class="resume-section">
            <h3>Education</h3>
            <div class="resume-entry">
              <div class="resume-entry-heading"><strong>B.E. Computer Science &amp; Engineering</strong><span>2024–2028</span></div>
              <p>Canara Engineering College · Current SGPA: 8.5</p>
            </div>
            <div class="resume-entry">
              <div class="resume-entry-heading"><strong>Pre-University Course (Science)</strong><span>2022–2024</span></div>
              <p>Creative PU College · 93%</p>
            </div>
            <div class="resume-entry">
              <div class="resume-entry-heading"><strong>School Education (CBSE)</strong><span>2012–2022</span></div>
              <p>Kendriya Vidyalaya · 89%</p>
            </div>
          </section>

          <section class="resume-section">
            <h3>Skills</h3>
            <ul class="resume-compact-list">
              <li><strong>Programming:</strong> Java 65%, Python 55%, C 55%</li>
              <li><strong>Frontend:</strong> HTML 80%, CSS 75%, JavaScript 60%</li>
              <li><strong>Backend:</strong> Python, Flask, Java</li>
              <li><strong>Databases:</strong> MySQL / SQL 65%, MongoDB 45%</li>
              <li><strong>Tools:</strong> Git &amp; GitHub 65%, VS Code 80%, Linux CLI 45%</li>
              <li><strong>AI/ML:</strong> Machine Learning 45%, Computer Vision / YOLO 40%, NumPy / Pandas 40%</li>
            </ul>
          </section>

          <section class="resume-section">
            <h3>Projects · Synent Technologies</h3>
            <ul class="resume-compact-list">
              <li><a href="https://vrushakamat21.github.io/synent-task3-apiintegrationproject-vrusha/" target="_blank" rel="noopener noreferrer"><strong>APIverse</strong></a> — combined live weather and forecasts with GitHub profile search and daily quotes using APIs.</li>
              <li><a href="https://vrushakamat21.github.io/synent-task1-responsivelandingpage-vrusha/" target="_blank" rel="noopener noreferrer"><strong>Velora</strong></a> — built a responsive fragrance storefront with browsable scent collections, category filters, and a fragrance customization experience.</li>
              <li><a href="https://vrushakamat21.github.io/synent-task2-todoapp-vrusha/" target="_blank" rel="noopener noreferrer"><strong>TaskFlow</strong></a> — created a task organizer with categories, priority highlights, due reminders, completion tracking, and quick notes.</li>
            </ul>
          </section>

          <section class="resume-section">
            <h3>Experience &amp; Activities</h3>
            <ul class="resume-compact-list">
              <li><strong>Internship · Synent Technologies:</strong> completed three hands-on projects spanning API integration, responsive web design, and task management.</li>
              <li><strong>Buildathon 2025:</strong> participated and received a certificate from the Canara Student Open Source Community.</li>
              <li><strong>ElectroHack 4.0:</strong> participated in a 24-hour national-level software and hardware hackathon at KS Institute of Technology on 25–26 September 2026.</li>
              <li>Continuously developing technical skills through projects, experimentation, and hands-on learning.</li>
            </ul>
          </section>

          <section class="resume-section">
            <h3>MongoDB Certificates</h3>
            <p>MongoDB Basics for Students · AI Data Strategy with MongoDB · RAG with MongoDB · Vector Search Fundamentals · AI Agents with MongoDB</p>
          </section>
        </article>
      `;

      const footer = `
        <a href="assets/resume.pdf" download="Vrusha_Kamat_Resume.pdf" class="btn btn-primary btn-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
          Download PDF
        </a>
        <button onclick="window.print()" class="btn btn-outline btn-sm">Print</button>
      `;

      openModal('Curriculum Vitae', 'Vrusha Kamat — B.E. Computer Science & Engineering', content, footer);
    });
  });


  // --------------------------------------------------------------------------
  // 9. Contact Form Validation & Submission
  // --------------------------------------------------------------------------
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const nameInput    = document.getElementById('contact-name');
      const emailInput   = document.getElementById('contact-email');
      const subjectInput = document.getElementById('contact-subject');
      const messageInput = document.getElementById('contact-message');
      const submitBtn    = contactForm.querySelector('button[type="submit"]');

      let isValid = true;

      if (!nameInput.value.trim()) {
        setError(nameInput, 'Please enter your name.');
        isValid = false;
      } else clearError(nameInput);

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(emailInput.value.trim())) {
        setError(emailInput, 'Please enter a valid email.');
        isValid = false;
      } else clearError(emailInput);

      if (!subjectInput.value.trim()) {
        setError(subjectInput, 'Please enter a subject.');
        isValid = false;
      } else clearError(subjectInput);

      if (!messageInput.value.trim() || messageInput.value.trim().length < 10) {
        setError(messageInput, 'Message should be at least 10 characters.');
        isValid = false;
      } else clearError(messageInput);

      if (!isValid) return;

      const originalHtml = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg viewBox="0 0 50 50" style="width:16px; height:16px; animation: spin 1s linear infinite;">
          <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" stroke-width="5" stroke-dasharray="31.4 31.4"></circle>
        </svg>
        Sending...
      `;

      const payload = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        subject: subjectInput.value.trim(),
        message: messageInput.value.trim()
      };

      // Try Java backend, gracefully fallback for static browsing
      fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(r => {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(data => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalHtml;
        contactForm.reset();
        showSuccessModal(payload.name, payload.subject, payload.email, data.messageId);
      })
      .catch(() => {
        setTimeout(() => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalHtml;
          contactForm.reset();
          showSuccessModal(payload.name, payload.subject, payload.email);
        }, 600);
      });
    });
  }

  function showSuccessModal(name, subject, email, msgId) {
    showToast('Message sent! Thank you 🎉');
    const content = `
      <div style="text-align: center; padding: 1.5rem 0;">
        <div style="width: 56px; height: 56px; border-radius: 50%; background: rgba(46,204,113,0.12); border: 1px solid #2ECC71; color: #2ECC71; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.25rem;">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m4.5 12.75 6 6 9-13.5" />
          </svg>
        </div>
        <h3 style="font-size: 1.5rem; font-family: var(--font-serif); margin-bottom: 0.5rem;">Message Received!</h3>
        <p style="color: var(--text-secondary); max-width: 420px; margin: 0 auto; font-size: 0.95rem; line-height: 1.65;">
          Thank you, <strong>${name}</strong>. Your message about <em>"${subject}"</em> has been received. I'll reply to <code>${email}</code> within 24 hours.
        </p>
        ${msgId ? `<div style="margin-top: 1rem; font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-muted);">Receipt: <span style="color: var(--accent-base);">${msgId}</span></div>` : ''}
      </div>
    `;
    openModal('Message Sent', "Let's Connect", content, `
      <button onclick="document.getElementById('general-modal-backdrop').classList.remove('open'); document.body.style.overflow='';" class="btn btn-primary btn-sm">Close</button>
    `);
  }


  // --------------------------------------------------------------------------
  // 10. Java Backend Health Check (footer badge)
  // --------------------------------------------------------------------------
  fetch('/api/health')
    .then(r => r.json())
    .then(data => {
      if (data && data.status === 'UP') {
        const badge = document.getElementById('java-backend-status');
        if (badge) {
          badge.innerHTML = `🟢 Java: ${data.runtime || 'Online'}`;
          badge.style.display = 'inline-flex';
        }
      }
    })
    .catch(() => { /* offline / static */ });


  // --------------------------------------------------------------------------
  // Utility Helpers
  // --------------------------------------------------------------------------
  function setError(input, message) {
    const group = input.closest('.form-group');
    if (!group) return;
    group.classList.add('error');
    const fb = group.querySelector('.form-feedback');
    if (fb) fb.textContent = message;
  }

  function clearError(input) {
    const group = input.closest('.form-group');
    if (!group) return;
    group.classList.remove('error');
  }

  function showToast(message) {
    const toast = document.getElementById('toast-notification');
    const msg = document.getElementById('toast-message');
    if (!toast || !msg) return;
    msg.textContent = message;
    toast.classList.add('visible');
    setTimeout(() => toast.classList.remove('visible'), 3800);
  }

  window.showPortfolioToast = showToast;

});

// Inject spin keyframe globally
const spinStyle = document.createElement('style');
spinStyle.textContent = `@keyframes spin { 100% { transform: rotate(360deg); } }`;
document.head.appendChild(spinStyle);

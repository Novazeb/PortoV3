<div align="center">

# 🌟 Nova Portfolio V3

**Modern, Minimalist, and High-Performance Portfolio for Nova (Nova Berkat Syukur Zebua)**  
*Full-Stack Developer & Software Engineer*

[![Live Demo](https://img.shields.io/badge/Demo-Live_Preview-black?style=for-the-badge&logo=vercel)](https://novazeb.github.io/PortoV3/)
[![Stack](https://img.shields.io/badge/Stack-React%20%7C%20Next.js%20%7C%20TailwindCSS-blue?style=for-the-badge)](https://github.com/Novazeb)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Overview

**PortoV3** is an interactive, dark-mode portfolio showcasing engineering projects, technical stack expertise, architecture manifesto, and timeline roadmap. Built on top of pre-rendered React & Next.js architectures with clean utility styling powered by Tailwind CSS.

### ✨ Key Features
- ⚡ **Zero-Dependency Local Server:** Runs natively with Python stdlib (`server.py`), no heavy `node_modules` required for static runtime.
- 🌐 **Dual-Language Support:** Instant switching between **English** (`/` or `/en`) and **Bahasa Indonesia** (`/id`).
- 🎨 **Modern Visual Aesthetics:** Infinite hero slider with authentic WebP portraits, smooth particle background canvas, and responsive hover cards.
- 📱 **Mobile & Desktop Optimized:** Ultra-responsive layout across all viewport breakpoints.
- 🚀 **Vercel & Static Host Ready:** Includes optimized `vercel.json` routing rules for 1-click cloud deployment.

---

## 🛠️ Tech Stack

### Frontend
- **React 19 & Next.js App Router** — Interactive components, state management & client hydration.
- **Tailwind CSS** — Modern typography, responsive utility grid, and dark theme design.
- **TypeScript & JavaScript (ES6+)** — Robust type-safe client-side logic.

### Backend & Databases
- **PHP & Laravel** — Robust backend architectures and RESTful APIs.
- **Node.js & Python** — Microservices, CLI utilities, and runtime scripting.
- **PostgreSQL & MySQL** — Relational database integrity and query optimization.

### Tools & Infrastructure
- **Git & GitHub** — Version control and collaborative workflows.
- **Vercel & Netlify** — Continuous deployment and edge hosting.
- **VS Code & Figma** — Interface design and engineering workflow.

---

## 📂 Project Structure

```text
PortoV3/
├── _next/                # Compiled JavaScript, CSS, and font bundles
│   └── static/
│       ├── chunks/       # Component bundles & Tailwind stylesheet
│       └── media/        # Web fonts (.woff2)
├── cdn-cgi/              # Cloudflare email protection scripts
├── hero-slider/          # Hero section WebP portrait assets (nova1 - nova7)
├── projects/             # Featured showcase thumbnails & project assets
├── stack/                # Tech stack SVG & brand icons
├── index.html            # Main English landing page
├── id.html               # Bahasa Indonesia landing page
├── portfolio.config.json # Centralized content configuration (Easy to edit!)
├── sync.py               # Auto-sync tool for portfolio.config.json
├── package.json          # Node scripts configuration
├── server.py             # Zero-dependency Python HTTP server
├── vercel.json           # Vercel deployment routing configuration
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation
```

---

## ✏️ How to Edit / Customize Content

You don't need to manually edit minified HTML files! All content is neatly organized in **`portfolio.config.json`**:

1. Open **`portfolio.config.json`** in VS Code.
2. Edit anything you want:
   - **Profile & Social Links** (`profile`)
   - **About Bio** in English & Indonesian (`about`)
   - **Tech Stack & Icons** (`stack`)
   - **Projects, Demo URLs & Descriptions** (`projects`)
   - **Career Roadmap Timeline** (`roadmap`)
3. Run the sync command:
   ```bash
   python sync.py
   # or with npm:
   npm run sync
   ```
4. Refresh your browser to see your changes applied instantly to both English and Indonesian versions!

---

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.8+ (No external pip libraries needed!)

### 1. Clone the repository
```bash
git clone https://github.com/Novazeb/PortoV3.git
cd PortoV3
```

### 2. Run the Local Server
```bash
python server.py
# or if using npm:
npm start
```

### 3. Open in Browser
Visit **`http://localhost:3000`** (English) or **`http://localhost:3000/id`** (Indonesian).

---

## ☁️ Deployment (Vercel)

This project is pre-configured with `vercel.json` for zero-configuration static deployment:

1. Push your changes to GitHub.
2. Go to [Vercel Dashboard](https://vercel.com/dashboard).
3. Click **Add New Project** and select `PortoV3`.
4. Deploy! Vercel will automatically route `/id` and `/en` cleanly.

---

## 📬 Connect with Me

- **Website:** [Nova Portfolio](https://github.com/Novazeb)
- **GitHub:** [@Novazeb](https://github.com/Novazeb)
- **LinkedIn:** [Nova Berkat Syukur Zebua](https://linkedin.com/in/novazebua)
- **Instagram:** [@zebua_1011](https://instagram.com/zebua_1011)
- **Email:** [novaberkatsyukurzebua@gmail.com](mailto:novaberkatsyukurzebua@gmail.com)

---

<div align="center">
  <sub>Built with ❤️ by <b>Nova Berkat Syukur Zebua</b>. All rights reserved.</sub>
</div>

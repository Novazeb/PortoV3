# Nova Portfolio (Version 3)

Technical portfolio and personal web application for Nova Berkat Syukur Zebua, Full-Stack Developer and Software Engineer.

## Overview

PortoV3 is a performance-oriented, bilingual web portfolio engineered with static site architecture. It showcases production software projects, core technical competencies, engineering philosophy, and career trajectory. The application is pre-rendered with Next.js and styled using Tailwind CSS, supporting dark theme interfaces, client-side motion choreography, and sub-second load times.

## Architecture and Specifications

| Attribute | Specification |
| :--- | :--- |
| **Frontend Framework** | React 19 / Next.js (Static Export) |
| **Styling** | Tailwind CSS, Custom Utility Layers |
| **Typography** | Syne, Inter (Self-hosted WebP/WOFF2) |
| **Internationalization** | Dual-language routing (English `/`, Indonesian `/id`) |
| **State & Configuration** | Centralized JSON schema (`portfolio.config.json`) |
| **Local Runtime** | Python 3 Standard Library HTTP Server (`server.py`) |
| **Deployment Target** | Static Hosting (Vercel, GitHub Pages, Netlify) |

## Core Technical Features

- **Decoupled Configuration Pipeline:** Content, metadata, project listings, and roadmap milestones are defined within `portfolio.config.json`. The synchronization compiler (`sync.py`) propagates state updates across static HTML templates and embedded React Flight payloads.
- **Zero-Dependency Runtime:** The local development server operates entirely on the Python Standard Library without requiring runtime package managers or local node dependency trees.
- **Static Pre-rendering & Performance:** Pre-compiled static HTML paired with modern WebP asset compression ensures minimal initial payload sizes and rapid First Contentful Paint (FCP).
- **Interactive Motion Systems:** Smooth scrolling powered by Lenis, particle field simulations, and physics-driven UI components implemented with Framer Motion.

## Technical Stack

### Frontend Engineering
- **Languages:** TypeScript, JavaScript (ECMAScript 2022+)
- **Frameworks & Libraries:** React 19, Next.js (App Router), Lucide React
- **CSS Architecture:** Tailwind CSS, PostCSS

### Backend & Databases
- **Runtime & Frameworks:** PHP 8+, Laravel, Node.js, Python 3
- **Data Persistence:** PostgreSQL, MySQL
- **APIs & Protocols:** RESTful APIs, JSON Schema

### DevOps & Infrastructure
- **Version Control:** Git, GitHub
- **Hosting & Edge Delivery:** Vercel, Netlify, Cloudflare
- **Tooling:** Visual Studio Code, Figma

## Repository Structure

```text
PortoV3/
├── _next/                # Pre-compiled client scripts, styles, and font assets
├── hero-slider/          # Compressed portrait assets (WebP format)
├── projects/             # High-resolution project showcase mockups
├── stack/                # Vector technology badges and brand icons
├── index.html            # English entry point (Primary)
├── id.html               # Indonesian entry point (Alternative)
├── portfolio.config.json # Master content configuration file
├── sync.py               # Automated JSON-to-HTML synchronization pipeline
├── push.bat              # Modular Git commit and push automation
├── server.py             # Lightweight local HTTP preview server
├── vercel.json           # Cloud deployment routing configuration
├── .gitignore            # Git exclusion rules
└── README.md             # Technical documentation
```

## Configuration and Content Management

All application content is maintained centrally within `portfolio.config.json`. Direct modification of compiled HTML or JavaScript bundles is not required.

### Content Modification Procedure:
1. Edit the relevant records in `portfolio.config.json`:
   - `profile`: Personal identity, contact endpoints, and social links.
   - `about`: Biographical statements in both languages.
   - `stack`: Technology categorizations and associated SVG identifiers.
   - `projects`: Showcase catalog including descriptions, tech tags, and repository links.
   - `roadmap`: Chronological milestones and professional experience.
2. Execute the synchronization pipeline:
   ```bash
   python sync.py
   ```
3. The script will rebuild the required state payloads and rewrite static DOM sections for both English and Indonesian documents.

## Local Execution

### Prerequisites
- Python 3.8 or higher

### Installation and Server Launch
1. Clone the repository:
   ```bash
   git clone https://github.com/Novazeb/PortoV3.git
   cd PortoV3
   ```
2. Start the local server:
   ```bash
   python server.py
   ```
3. Access the application via standard web browsers:
   - English: `http://localhost:3000/`
   - Indonesian: `http://localhost:3000/id`

## Deployment

The repository includes a production-ready `vercel.json` specification for zero-configuration static deployment:
1. Commit and push repository updates to GitHub.
2. Connect the repository to Vercel or any static hosting provider.
3. Deploy without build overrides; root directory static files will be served automatically.

## Contact Information

- **Full Name:** Nova Berkat Syukur Zebua
- **GitHub:** https://github.com/Novazeb
- **LinkedIn:** https://linkedin.com/in/novazebua
- **Instagram:** https://instagram.com/zebua_1011
- **Email:** novaberkatsyukurzebua@gmail.com

---

Copyright 2026 Nova Berkat Syukur Zebua. All rights reserved.

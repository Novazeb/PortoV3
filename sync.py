import json, os, re, codecs, shutil

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'portfolio.config.json')

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_pages():
    cfg = load_config()
    print("Loaded portfolio.config.json...")
    
    # 1. Update English index.html
    update_single_page('index.html', cfg, lang='en')
    # 2. Update Indonesian id.html
    update_single_page('id.html', cfg, lang='id')

    # 3. Clean up obsolete cdn-cgi folder
    cdn_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cdn-cgi')
    if os.path.exists(cdn_dir):
        shutil.rmtree(cdn_dir, ignore_errors=True)
        print("[CLEANUP] Removed obsolete cdn-cgi/ Cloudflare assets.")

    # 4. Update preload logo with user's custom logo
    custom_logo_src = r"C:\Users\NOVA ZE\.gemini\antigravity\brain\ebc36c23-1a84-4cfb-8b01-d1bec4273374\.user_uploaded\media_1788406459501.png"
    logo_dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')
    if os.path.exists(custom_logo_src):
        try:
            shutil.copyfile(custom_logo_src, logo_dst)
            print("[OK] Preload logo updated to new custom logo!")
        except Exception as e:
            print(f"[WARN] Could not copy logo: {e}")

    # 5. Generate push.bat helper
    push_bat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'push.bat')
    with open(push_bat_path, 'w', encoding='utf-8') as f:
        f.write('''@echo off
echo Committing granular updates to Git...
git add portfolio.config.json
git commit -m "feat(config): customize portfolio with real projects, roadmap 2021-2026, and authentic profile"
git add projects/
git commit -m "feat(assets): add authentic project mockups (sinar design build, sumatra tour, anak cerdas)"
git add sync.py
git commit -m "feat(build): implement automated JSON-to-HTML flight sync with cloudflare cleanup"
git add server.py
git commit -m "refactor(server): clean up legacy cloudflare routes and optimize local preview server"
git add _next/
git commit -m "fix(contact): patch contact section to render direct GitHub profile link"
git add index.html id.html
git commit -m "feat(pages): synchronize dual-language entry points with authentic portfolio data"
git add README.md package.json .gitignore
git commit -m "docs(meta): update documentation, email, and package build scripts"
echo Pushing to GitHub main...
git push origin main
echo Done!
pause
''')

    print("[OK] All portfolio pages synchronized successfully with portfolio.config.json!")

def update_single_page(filename, cfg, lang='en'):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename} (not found)")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update About Modal in Push 4
    about_text = cfg['about']['full_en'] if lang == 'en' else cfg['about']['full_id']
    escaped_about = about_text.replace('\n', '\\n')
    pattern_about = r'20:T[0-9a-fA-F]+,(.*?)(?=\"\]\))'
    m_about = re.search(pattern_about, html, re.DOTALL)
    if m_about:
        decoded = json.loads('"' + escaped_about + '"')
        byte_len = len(decoded.encode('utf-8'))
        hex_len = hex(byte_len)[2:]
        html = html[:m_about.start()] + f'20:T{hex_len},{escaped_about}' + html[m_about.end():]

    # Build formatted projects
    formatted_projects = []
    for p in cfg['projects']:
        formatted_projects.append({
            "id": p.get("id", ""),
            "title": p.get("title", ""),
            "category": p.get("category_en", "") if lang == 'en' else p.get("category_id", ""),
            "description": p.get("description_en", "") if lang == 'en' else p.get("description_id", ""),
            "image": p.get("image", ""),
            "tech": p.get("tech", []),
            "demoUrl": p.get("demoUrl", ""),
            "sourceUrl": p.get("sourceUrl", "")
        })

    # Build formatted roadmap
    formatted_roadmap = []
    for r in cfg['roadmap']:
        formatted_roadmap.append({
            "id": r.get("id", ""),
            "year": r.get("year", ""),
            "description": r.get("description_en", "") if lang == 'en' else r.get("description_id", ""),
            "stack": r.get("stack", [])
        })

    # Shared social links
    social_links = []
    if "github" in cfg['profile']['social']:
        social_links.append({"label": "GitHub", "href": cfg['profile']['social']['github']})
    if "linkedin" in cfg['profile']['social']:
        social_links.append({"label": "Linkedin", "href": cfg['profile']['social']['linkedin']})
    if "instagram" in cfg['profile']['social']:
        social_links.append({"label": "Instagram", "href": cfg['profile']['social']['instagram']})

    dictionary = {
        "nav": {"home": "Home", "about": "About", "stack": "Stack", "projects": "Projects", "roadmap": "Roadmap", "contact": "Contact"} if lang == 'en' else {"home": "Beranda", "about": "Tentang", "stack": "Keahlian", "projects": "Proyek", "roadmap": "Roadmap", "contact": "Kontak"},
        "title": {"about": "About", "stack": "Stack", "projects": "Projects", "roadmap": "Roadmap", "contact": "Contact"} if lang == 'en' else "Portofolio",
        "scrollDown": "Scroll" if lang == 'en' else "Gulir ke Bawah",
        "contactMe": "Contact Me" if lang == 'en' else "Hubungi Saya",
        "exploreProjects": "Explore Projects" if lang == 'en' else "Jelajahi Proyek",
        "readFullVersion": "Read Full Version" if lang == 'en' else "Baca Versi Lengkap",
        "frontendStack": "Frontend Technologies" if lang == 'en' else "Teknologi Frontend",
        "backendStack": "Backend Technologies" if lang == 'en' else "Teknologi Backend",
        "databaseStack": "Databases & ORMs" if lang == 'en' else "Databases & ORMs",
        "toolsStack": "Tools & Infrastructure" if lang == 'en' else "Tools & Infrastruktur",
        "projectsIntro": "A collection of *experiments*, *products*, and *digital artifacts* forged in the **void**." if lang == 'en' else "Kumpulan proyek unggulan, sistem web modern, dan arsitektur aplikasi yang pernah saya kembangkan.",
        "projectsScrollText": "Scroll to explore" if lang == 'en' else "Gulir untuk melihat proyek",
        "projectsEndText": "End" if lang == 'en' else "Akhir dari daftar proyek",
        "roadmapDescription": "A roadmap where I share the experiences I've gained throughout my software journey and the technologies I've learned." if lang == 'en' else "Perjalanan eksplorasi teknologi dan pengembangan keahlian software engineering saya.",
        "contactIntroText": "Whether we start fresh to bring a project to life or take an existing system further." if lang == 'en' else "Tertarik berkolaborasi atau membangun proyek bersama? Jangan ragu untuk menghubungi saya.",
        "sendEmail": "Send an Email" if lang == 'en' else "Kirim Email",
        "directLine": "GitHub",
        "allRightsReserved": "All rights reserved." if lang == 'en' else "Hak Cipta Dilindungi",
        "contactModalDescription": "Send me a message and I'll get back to you as soon as possible." if lang == 'en' else "Silakan kirim pesan atau hubungi saya langsung melalui saluran berikut.",
        "projectDetails": "Details about" if lang == 'en' else "Detail Proyek",
        "aboutProject": "About the Project" if lang == 'en' else "Tentang Proyek",
        "technologies": "Technologies" if lang == 'en' else "Teknologi",
        "liveDemo": "Live Demo" if lang == 'en' else "Demo Langsung",
        "sourceCode": "Source Code" if lang == 'en' else "Kode Sumber",
        "notFound": {"title": "Page Not Found", "description": "The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.", "goHome": "Back to Home"} if lang == 'en' else "Halaman Tidak Ditemukan"
    }

    props = {
        "lang": lang,
        "dictionary": dictionary,
        "contents": {
            "about": {
                "intro": "I'm a *Full Stack Developer* focused on building **clean and sustainable systems**." if lang == 'en' else "Saya seorang *Full Stack Developer* yang berfokus membangun **sistem web bersih, cepat, dan scalable**.",
                "description": cfg['about']['short_en'] if lang == 'en' else cfg['about']['short_id'],
                "full": "$20",
                "title": "I'm a *Full Stack Developer* focused on building **clean and sustainable systems**." if lang == 'en' else "Saya seorang *Full Stack Developer* yang berfokus membangun **sistem web bersih, cepat, dan scalable**."
            },
            "manifesto": [
                "RADICAL TRANSPARENCY",
                "INTENTIONAL MINIMALISM",
                "ARCHITECTURAL INTEGRITY",
                "FIRST PRINCIPLES THINKING",
                "PERFORMANCE WITHOUT COMPROMISE",
                "SCALABLE VISION"
            ],
            "projects": formatted_projects,
            "roadmap": formatted_roadmap
        },
        "shared": {
            "contact": {
                "location": cfg['profile'].get('location', 'Indonesia'),
                "email": cfg['profile']['email'],
                "phone": "github.com/Novazeb"
            },
            "social": social_links,
            "stack": cfg['stack']
        }
    }

    push_data = ["$", "html", None, {
        "lang": "en" if lang == 'en' else "id",
        "suppressHydrationWarning": True,
        "children": ["$", "body", None, {
            "className": "inter_5901b7c6-module__ec5Qua__variable syne_950e48a-module__CJAAbq__variable font-sans bg-background text-foreground antialiased",
            "children": ["$", "$L1f", None, {
                **props,
                "children": "$L21"
            }]
        }]
    }]

    new_json_str = json.dumps(push_data, ensure_ascii=False)
    encoded_escaped = json.dumps(new_json_str, ensure_ascii=False)[1:-1]
    new_push = f'self.__next_f.push([1,"8:{encoded_escaped}\\n"])'

    m_p5 = re.search(r'self\.__next_f\.push\(\[1,\"8:.*?\]\)', html, re.DOTALL)
    if m_p5:
        html = html[:m_p5.start()] + new_push + html[m_p5.end():]

    # Replace Project Titles & Categories in HTML markup
    html = html.replace('Lumina Studio', 'SINAR DESIGN & BUILD')
    html = html.replace('Mergeall Platform', 'Sumatra Tour')
    html = html.replace('CekNet Suite', 'Anak Cerdas')
    html = html.replace('/projects/20260427093247885.jpg', '/projects/sinardbmockup.jpg')
    html = html.replace('/projects/20260427093247620.jpg', '/projects/sumatratourmockup.jpg')
    html = html.replace('/projects/20260305210513749.jpg', '/projects/anakcerdasmockup.jpg')

    # Replace old email and clean Cloudflare email-protection tags
    email = cfg['profile']['email']
    html = html.replace('[email&#160;protected]', email)
    html = html.replace('[email protected]', email)
    html = re.sub(r'\[email(&#160;|&nbsp;|\s)*protected\]', email, html)
    html = re.sub(r'<a[^>]*class="__cf_email__"[^>]*>.*?</a>', email, html)
    html = re.sub(r'href="[^"]*email-protection[^"]*"', f'href="mailto:{email}"', html)
    html = re.sub(r'<script[^>]*email-decode\.min\.js[^>]*></script>', '', html)
    html = re.sub(r'<script[^>]*cloudflareinsights\.com[^>]*>.*?</script>', '', html)
    html = html.replace('mustafw42@gmail.com', email)
    html = html.replace('novaberkatsyukurzebua@gmail.com', email)
    html = html.replace('novanerkatsyukurzebua@gmail.com', email)

    # Replace DIRECT LINE with GITHUB
    html = html.replace('DIRECT LINE', 'GITHUB')
    html = html.replace('Direct Line', 'GitHub')
    html = html.replace('Saluran Langsung', 'GitHub')
    html = html.replace('Not added yet.', 'github.com/Novazeb')
    html = re.sub(r'href="tel:[^"]*"', 'href="https://github.com/Novazeb" target="_blank" rel="noopener noreferrer"', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Synchronized {filename} for language: [{lang.upper()}]")

if __name__ == '__main__':
    build_pages()

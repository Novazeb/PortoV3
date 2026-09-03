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

    # 4. Generate high-resolution solid white 'N' logo and favicon.ico if on Windows
    import platform
    if platform.system() == "Windows":
        try:
            ps_cmd = (
                "[void][System.Reflection.Assembly]::LoadWithPartialName('System.Drawing'); "
                "$bmp = New-Object System.Drawing.Bitmap 512, 512; "
                "$g = [System.Drawing.Graphics]::FromImage($bmp); "
                "$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic; "
                "$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias; "
                "$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAlias; "
                "$g.Clear([System.Drawing.Color]::Transparent); "
                "$bBlack = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::Black); "
                "$g.FillEllipse($bBlack, 16, 16, 480, 480); "
                "$fontFamily = New-Object System.Drawing.FontFamily('Arial Black'); "
                "$path = New-Object System.Drawing.Drawing2D.GraphicsPath; "
                "$sf = New-Object System.Drawing.StringFormat; "
                "$sf.Alignment = [System.Drawing.StringAlignment]::Center; "
                "$sf.LineAlignment = [System.Drawing.StringAlignment]::Center; "
                "$path.AddString('N', $fontFamily, [int][System.Drawing.FontStyle]::Bold, 295, (New-Object System.Drawing.RectangleF 0, 8, 512, 512), $sf); "
                "$bWhite = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White); "
                "$g.FillPath($bWhite, $path); "
                "$penWhite = New-Object System.Drawing.Pen([System.Drawing.Color]::White, 24); "
                "$penWhite.LineJoin = [System.Drawing.Drawing2D.LineJoin]::Round; "
                "$g.DrawPath($penWhite, $path); "
                "$dest = 'd:\\ANIME\\PortoV3\\logo.png'; "
                "$bmp.Save($dest, [System.Drawing.Imaging.ImageFormat]::Png); "
                "$favBmp = New-Object System.Drawing.Bitmap 64, 64; "
                "$favG = [System.Drawing.Graphics]::FromImage($favBmp); "
                "$favG.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic; "
                "$favG.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias; "
                "$favG.DrawImage($bmp, 0, 0, 64, 64); "
                "$hIcon = $favBmp.GetHicon(); "
                "$icon = [System.Drawing.Icon]::FromHandle($hIcon); "
                "$fs = [System.IO.File]::Create('d:\\ANIME\\PortoV3\\favicon.ico'); "
                "$icon.Save($fs); "
                "$fs.Close(); $icon.Dispose(); $favG.Dispose(); $favBmp.Dispose(); "
                "$g.Dispose(); $bmp.Dispose();"
            )
            import subprocess
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False)
            print("[OK] Preload logo and favicon.ico updated with ultra-bold white 'N'!")
        except Exception as e:
            print(f"[WARN] Could not generate solid white logo/favicon: {e}")

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
        "projectsEndText": "MORE IN GITHUB",
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

    # Replace END text with MORE IN GITHUB
    html = html.replace('>End<', '>MORE IN GITHUB<')
    html = html.replace('>END<', '>MORE IN GITHUB<')
    html = html.replace('>Akhir dari daftar proyek<', '>MORE IN GITHUB<')

    # Synchronize pre-rendered Roadmap HTML section
    roadmap_pattern = r'<section id="roadmap">.*?</section></section>'
    title = "Roadmap"
    desc = "A roadmap where I share the experiences I&#x27;ve gained throughout my software journey and the technologies I&#x27;ve learned." if lang == 'en' else "Perjalanan eksplorasi teknologi dan pengembangan keahlian software engineering saya."
    
    items_html = []
    for i, item in enumerate(cfg['roadmap']):
        is_even = (i % 2 == 0)
        flex_dir = "flex-row" if is_even else "flex-row-reverse"
        text_align = "md:text-right" if is_even else "md:text-left"
        badge_align = "md:justify-end" if is_even else "md:justify-start"
        margin_style = "margin-left:auto" if is_even else "margin-left:0"
        stack_align = "md:justify-end" if is_even else "justify-start"
        bg_pos = "-left-12" if is_even else "-right-12 text-right"
        
        item_id = item.get("id", f"{i+1:02d}")
        year = item.get("year", "")
        short_year = year[-2:] if len(year) >= 2 else year
        item_desc = item.get("description_en", "") if lang == 'en' else item.get("description_id", "")
        item_desc = item_desc.replace("'", "&#x27;")
        
        stack_spans = "".join([
            f'<span class="text-xs uppercase tracking-wider text-muted-foreground font-medium px-3 py-1 rounded-full border border-border/40 bg-background/50 shadow-sm">{tech}</span>'
            for tech in item.get("stack", [])
        ])
        
        items_html.append(
            f'<div class="relative flex items-center justify-between w-full {flex_dir}">'
            f'<div class="w-[calc(50%-3rem)] hidden md:block"></div>'
            f'<div class="absolute left-6 md:left-1/2 -translate-x-1/2 w-8 h-8 md:w-10 md:h-10 rounded-full border border-border/50 bg-background z-20 flex items-center justify-center shadow-lg group-hover:border-primary/50 transition-colors duration-500">'
            f'<div class="w-2.5 h-2.5 md:w-3 md:h-3 rounded-full bg-primary shadow-[0_0_10px_rgba(var(--primary),0.8)]"></div>'
            f'</div>'
            f'<div class="w-full md:w-[calc(50%-3rem)] pl-16 md:pl-0 relative group">'
            f'<div class="will-change-[opacity,filter,transform]" style="opacity:0;filter:blur(15px);transform:translateY(30px)">'
            f'<div class="relative p-8 md:p-10 border border-border/50 bg-secondary/5 backdrop-blur-md overflow-hidden transition-all duration-700 ease-out hover:bg-secondary/20 hover:border-border hover:shadow-2xl {text_align}">'
            f'<span class="max-sm:hidden text-xs font-mono tracking-widest text-muted-foreground uppercase flex mb-4 {badge_align}">{item_id}</span>'
            f'<div class="flex flex-col gap-3 relative z-10">'
            f'<h3 class="text-4xl md:text-5xl lg:text-6xl tracking-tighter font-serif italic font-semibold text-foreground uppercase mt-2 group-hover:text-primary transition-colors duration-500">{year}</h3>'
            f'<p class="text-muted-foreground text-sm md:text-base leading-relaxed mt-2 max-w-sm ml-0 md:max-w-md" style="{margin_style}">{item_desc}</p>'
            f'<div class="flex flex-wrap gap-2 mt-6 {stack_align}">{stack_spans}</div>'
            f'</div>'
            f'<div class="absolute top-1/2 -translate-y-1/2 text-[10rem] font-black italic text-foreground/3 select-none pointer-events-none transition-all duration-700 {bg_pos}">{short_year}</div>'
            f'</div></div></div></div>'
        )
    
    all_items = "".join(items_html)
    new_roadmap = (
        f'<section id="roadmap">'
        f'<section class="relative container-void overflow-hidden py-32 xl:py-48 border-t border-border/50">'
        f'<div class="absolute top-1/4 left-0 w-full max-w-lg h-[500px] bg-primary/5 blur-[120px] rounded-full pointer-events-none -translate-x-1/2"></div>'
        f'<div class="absolute bottom-1/4 right-0 w-full max-w-lg h-[500px] bg-primary/5 blur-[120px] rounded-full pointer-events-none translate-x-1/2"></div>'
        f'<div class="absolute top-0 left-0 right-0 bottom-0 pointer-events-none flex items-center justify-center opacity-[0.02] z-0 overflow-hidden" style="transform:none">'
        f'<div class="text-[20vw] font-black tracking-tighter uppercase whitespace-nowrap">{title}</div>'
        f'</div>'
        f'<div class="container mx-auto px-container max-w-6xl relative z-10">'
        f'<div class="flex flex-col md:items-center mb-24 md:mb-40 gap-4 text-center">'
        f'<div class="will-change-[opacity,filter,transform]" style="opacity:0;filter:blur(15px);transform:translateY(30px)"><span class="title-counter">[004]</span></div>'
        f'<div class="will-change-[opacity,filter,transform]" style="opacity:0;filter:blur(15px);transform:translateY(30px)"><h2 class="title">{title}</h2></div>'
        f'<div class="will-change-[opacity,filter,transform]" style="opacity:0;filter:blur(15px);transform:translateY(30px)"><p class="text-lg mt-3 max-w-xl italic font-medium tracking-tight text-foreground/60">{desc}</p></div>'
        f'</div>'
        f'<div class="relative">'
        f'<div class="absolute left-6 md:left-1/2 top-0 bottom-0 w-px bg-border/40 -translate-x-1/2"></div>'
        f'<div class="absolute left-6 md:left-1/2 top-0 bottom-0 w-[2px] bg-linear-to-b from-primary via-primary to-transparent shadow-[0_0_10px_rgba(var(--primary),0.5)] -translate-x-1/2 z-10" style="transform:scaleY(0);transform-origin:50% 0% 0"></div>'
        f'<div class="flex flex-col w-full gap-8 md:gap-24 relative z-20">{all_items}</div>'
        f'</div></div></section></section>'
    )
    
    m_road = re.search(roadmap_pattern, html, re.DOTALL)
    if m_road:
        html = html[:m_road.start()] + new_roadmap + html[m_road.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Synchronized {filename} for language: [{lang.upper()}]")

if __name__ == '__main__':
    build_pages()

import json, os, re, codecs

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

    # Update Push 5 JSON Data
    m_p5 = re.search(r'self\.__next_f\.push\(\[1,\"8:.*?\]\)', html, re.DOTALL)
    if m_p5:
        push_str = m_p5.group(0)
        start = push_str.find('"8:') + 3
        end = push_str.rfind('"]')
        inner_escaped = push_str[start:end]
        decoded = codecs.decode(inner_escaped.encode('utf-8'), 'unicode_escape').strip()
        data = json.loads(decoded)
        
        lang_props = data[3]['children'][3]['children'][3]
        lang_props['lang'] = lang
        
        # Shared stack
        lang_props['shared']['stack'] = cfg['stack']
        
        # Contents about
        lang_props['contents']['about']['title'] = (
            "I'm a *Full Stack Developer* focused on building **clean and sustainable systems**."
            if lang == 'en' else
            "Saya seorang *Full Stack Developer* yang berfokus membangun **sistem web bersih, cepat, dan scalable**."
        )
        lang_props['contents']['about']['description'] = cfg['about']['short_en'] if lang == 'en' else cfg['about']['short_id']
        
        # Contents projects
        formatted_projects = []
        for p in cfg['projects']:
            formatted_projects.append({
                "id": p["id"],
                "title": p["title"],
                "category": p["category_en"] if lang == 'en' else p["category_id"],
                "description": p["description_en"] if lang == 'en' else p["description_id"],
                "image": p["image"],
                "tech": p["tech"],
                "demoUrl": p["demoUrl"],
                "sourceUrl": p["sourceUrl"]
            })
        lang_props['contents']['projects'] = formatted_projects
        
        # Contents roadmap
        formatted_roadmap = []
        for r in cfg['roadmap']:
            formatted_roadmap.append({
                "id": r["id"],
                "year": r["year"],
                "description": r["description_en"] if lang == 'en' else r["description_id"],
                "stack": r["stack"]
            })
        lang_props['contents']['roadmap'] = formatted_roadmap
        
        # Re-encode JSON push
        new_json_str = json.dumps(data)
        encoded_escaped = json.dumps(new_json_str)[1:-1]
        new_push = f'self.__next_f.push([1,"8:{encoded_escaped}\\n"])'
        html = html[:m_p5.start()] + new_push + html[m_p5.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Synchronized {filename} for language: [{lang.upper()}]")

if __name__ == '__main__':
    build_pages()

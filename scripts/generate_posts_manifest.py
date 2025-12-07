#!/usr/bin/env python3
"""
Simple manifest generator for posts.
Scans `content/posts/*.md`, extracts basic frontmatter fields (title, date, excerpt first paragraph)
and writes `posts/posts.json` which is used by `index.html`.

No extra packages required.

Usage:
  python scripts/generate_posts_manifest.py

"""
import os
import json
import re

ROOT = os.path.dirname(os.path.dirname(__file__))
CONTENT_DIR = os.path.join(ROOT, 'content', 'posts')
OUT_DIR = os.path.join(ROOT, 'posts')
OUT_FILE = os.path.join(OUT_DIR, 'posts.json')

def parse_frontmatter(text):
    fm = {}
    m = re.match(r'^---\n([\s\S]*?)\n---', text)
    if not m:
        return fm
    body = m.group(1)
    for line in body.splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k = k.strip()
        v = v.strip()
        # remove wrapping quotes
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        # keep raw for possible JSON-like values (e.g., tags: ["a","b"])
        fm[k] = v
    return fm

def first_paragraph_after_fm(text):
    # remove frontmatter
    content = re.sub(r'^---[\s\S]*?---\n?', '', text)
    # split into paragraphs
    parts = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]
    if parts:
        # return first paragraph without markdown headers
        return re.sub(r'^#+\s*', '', parts[0]).strip()
    return ''

def main():
    if not os.path.isdir(CONTENT_DIR):
        print('No content/posts directory found at', CONTENT_DIR)
        return
    posts = []
    for fname in sorted(os.listdir(CONTENT_DIR)):
        if not fname.lower().endswith('.md'):
            continue
        path = os.path.join(CONTENT_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        fm = parse_frontmatter(text)
        excerpt = first_paragraph_after_fm(text)
        # try to parse tags if present and looks like a list
        tags = fm.get('tags', '')
        parsed_tags = None
        if tags:
            try:
                # tags in frontmatter usually look like: ["tag1","tag2"] (valid JSON)
                parsed_tags = json.loads(tags)
            except Exception:
                # fallback: try to parse a comma-separated string
                parsed_tags = [t.strip().strip('"').strip("'") for t in re.split(r',\s*', tags) if t.strip()]

        item = {
            'title': fm.get('title') or os.path.splitext(fname)[0],
            'date': fm.get('date',''),
            'path': os.path.join('content','posts', fname).replace('\\','/'),
            'excerpt': excerpt
        }
        if parsed_tags:
            item['tags'] = parsed_tags
        posts.append(item)

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print('Wrote', OUT_FILE)

if __name__ == '__main__':
    main()

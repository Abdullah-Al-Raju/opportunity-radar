#!/usr/bin/env python3
"""
Tech & AI Radar - Article Image Manager
Allows you to list, inspect, set, or replace respected images for any article.

Usage:
  python3 scripts/manage_images.py --list
  python3 scripts/manage_images.py --set <slug> <image_url_or_filepath>
  python3 scripts/manage_images.py --download-missing
"""

import sys
import re
import shutil
import argparse
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT_DIR / "src" / "content" / "posts"
PUBLIC_POST_IMG_DIR = ROOT_DIR / "public" / "img" / "posts"

def list_post_images():
    PUBLIC_POST_IMG_DIR.mkdir(parents=True, exist_ok=True)
    posts = sorted(list(POSTS_DIR.glob("*.md")))
    if not posts:
        print("No articles found in src/content/posts/.")
        return

    print(f"\n{'SLUG':<45} | {'COVER PATH':<35} | {'LOCAL FILE':<12} | {'SIZE (KB)'}")
    print("-" * 105)

    for p in posts:
        slug = p.stem
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r'cover:\s*["\']([^"\']+)["\']', content)
        cover = match.group(1) if match else "None"

        local_img = PUBLIC_POST_IMG_DIR / f"{slug}.jpg"
        has_file = local_img.exists()
        size_kb = f"{local_img.stat().st_size / 1024:.1f}" if has_file else "N/A"

        status_str = "✓ Exists" if has_file else "✗ Missing"
        print(f"{slug:<45} | {cover:<35} | {status_str:<12} | {size_kb}")
    print("-" * 105)

def set_image(slug: str, source: str):
    PUBLIC_POST_IMG_DIR.mkdir(parents=True, exist_ok=True)
    target_img = PUBLIC_POST_IMG_DIR / f"{slug}.jpg"
    web_path = f"/img/posts/{slug}.jpg"

    print(f"[Image Manager] Setting image for article: {slug}")
    print(f"[Image Manager] Source: {source}")

    if source.startswith("http://") or source.startswith("https://"):
        try:
            req = urllib.request.Request(
                source,
                headers={"User-Agent": "Mozilla/5.0 (TechRadar/1.0; Edge/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                with open(target_img, "wb") as f:
                    f.write(data)
            print(f"✓ Downloaded image ({len(data)//1024} KB) -> {target_img}")
        except Exception as e:
            print(f"✗ Error downloading image: {e}")
            return False
    else:
        src_path = Path(source)
        if not src_path.exists():
            print(f"✗ Local file not found: {source}")
            return False
        shutil.copy2(src_path, target_img)
        print(f"✓ Copied local image -> {target_img}")

    # Update article markdown file
    post_file = POSTS_DIR / f"{slug}.md"
    if post_file.exists():
        with open(post_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Update frontmatter cover
        if 'cover:' in content:
            content = re.sub(r'cover:\s*["\'][^"\']+["\']', f'cover: "{web_path}"', content)
        else:
            content = re.sub(r'^(---\n)', f'\\1cover: "{web_path}"\n', content)

        # Update in-article figure if present
        content = re.sub(
            r'<img src="[^"]+" alt="([^"]+)" class="w-full rounded-2xl',
            f'<img src="{web_path}" alt="\\1" class="w-full rounded-2xl',
            content
        )

        with open(post_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Updated frontmatter and in-article figure in {post_file}")
    else:
        print(f"! Notice: Markdown post {post_file} does not exist yet. Image is ready in {target_img}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Tech & AI Radar Image Management Tool")
    parser.add_argument("--list", action="store_true", help="List all articles and their cover image status")
    parser.add_argument("--set", nargs=2, metavar=("SLUG", "SOURCE"), help="Set or update cover image for a slug")

    args = parser.parse_args()

    if args.set:
        slug, source = args.set
        set_image(slug, source)
    else:
        list_post_images()

if __name__ == "__main__":
    main()

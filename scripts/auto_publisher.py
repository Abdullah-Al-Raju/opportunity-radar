#!/usr/bin/env python3
"""
Tech & AI Radar - Autonomous 24/7 Content Publisher Engine
Equipped with Respected Tech Image Downloader + Google Gemini 3.8 Flash + IndexNow
"""

import os
import sys
import json
import re
import time
import shutil
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Base Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_FILE = ROOT_DIR / "data" / "topics.json"
POSTS_DIR = ROOT_DIR / "src" / "content" / "posts"
PUBLIC_POST_IMG_DIR = ROOT_DIR / "public" / "img" / "posts"

# Load environment from ~/.env or project .env if present
def load_env_file():
    candidates = [ROOT_DIR / ".env", Path.home() / ".env"]
    for env_path in candidates:
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k not in os.environ:
                            os.environ[k] = v.strip().strip("'\"")

load_env_file()

SITE_URL = os.environ.get("SITE_URL", "https://opportunity-radar-c60.pages.dev").rstrip("/")
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "opportunityradarindexnowkey")

# Gemini keys - prioritizing Key 2 as primary since user recommended using both
GEMINI_KEYS = [
    k for k in [
        os.environ.get("GEMINI_API_KEY_2", ""),
        os.environ.get("GEMINI_API_KEY", "")
    ] if k
]

# Curated bank of respected, high-resolution royalty-free photography from Unsplash
TECH_IMAGE_BANK = {
    "ai_models": [
        "https://images.unsplash.com/photo-1677442136019-21780efad99a?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1676299081847-824916de030a?auto=format&fit=crop&w=1200&h=630&q=85",
    ],
    "coding": [
        "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1200&h=630&q=85",
    ],
    "autonomous_agents": [
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1614741118887-7a4ee193a5fa?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=1200&h=630&q=85",
    ],
    "cloud_infra": [
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&h=630&q=85",
    ],
    "developer_tools": [
        "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=1200&h=630&q=85",
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1200&h=630&q=85",
    ]
}

def resolve_and_download_image(topic: dict) -> str:
    """
    Selects or uses custom image, downloads it to public/img/posts/{slug}.jpg,
    and returns the local web path for deterministic edge delivery.
    """
    PUBLIC_POST_IMG_DIR.mkdir(parents=True, exist_ok=True)
    slug = topic.get("slug") or topic["id"]
    local_filename = f"{slug}.jpg"
    local_path = PUBLIC_POST_IMG_DIR / local_filename
    web_path = f"/img/posts/{local_filename}"

    # If already downloaded and valid, reuse local image
    if local_path.exists() and local_path.stat().st_size > 1000:
        return web_path

    # Check if topic has an explicit image_url
    selected_url = topic.get("image_url")

    if not selected_url:
        # Determine image category
        category_key = topic.get("image_category")
        if not category_key or category_key not in TECH_IMAGE_BANK:
            cat_lower = topic.get("category", "").lower()
            if "agent" in cat_lower:
                category_key = "autonomous_agents"
            elif "cloud" in cat_lower:
                category_key = "cloud_infra"
            elif "ai" in cat_lower or "llm" in cat_lower:
                category_key = "ai_models"
            else:
                category_key = "coding"

        candidates = TECH_IMAGE_BANK.get(category_key, TECH_IMAGE_BANK["coding"])
        # Deterministic pick based on slug hash so the image is reproducible
        selected_url = candidates[abs(hash(slug)) % len(candidates)]

    # Download to local public directory
    try:
        req = urllib.request.Request(
            selected_url,
            headers={"User-Agent": "Mozilla/5.0 (TechRadar/1.0; Edge/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            image_data = resp.read()
            with open(local_path, "wb") as f:
                f.write(image_data)
            print(f"[Image Engine] Successfully downloaded cover image -> {web_path}")
            return web_path
    except Exception as e:
        print(f"[Image Engine Warning] Download failed ({e}). Using direct CDN URL: {selected_url}")
        return selected_url

def set_custom_image_for_post(slug: str, source: str) -> bool:
    """
    Sets a custom image for an existing post or topic.
    'source' can be an HTTP(S) URL or a local file path.
    """
    PUBLIC_POST_IMG_DIR.mkdir(parents=True, exist_ok=True)
    target_filename = f"{slug}.jpg"
    target_path = PUBLIC_POST_IMG_DIR / target_filename
    web_path = f"/img/posts/{target_filename}"

    if source.startswith("http://") or source.startswith("https://"):
        try:
            req = urllib.request.Request(
                source,
                headers={"User-Agent": "Mozilla/5.0 (TechRadar/1.0; Edge/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                with open(target_path, "wb") as f:
                    f.write(data)
            print(f"[Image Engine] Downloaded custom image from URL -> {target_path}")
        except Exception as e:
            print(f"[Image Engine Error] Failed downloading from {source}: {e}")
            return False
    else:
        src_file = Path(source)
        if not src_file.exists():
            print(f"[Image Engine Error] Source file does not exist: {source}")
            return False
        shutil.copy2(src_file, target_path)
        print(f"[Image Engine] Copied local image -> {target_path}")

    # Update post markdown frontmatter and figure tag if post file exists
    post_file = POSTS_DIR / f"{slug}.md"
    if post_file.exists():
        with open(post_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Update frontmatter cover
        content = re.sub(
            r'cover:\s*["\'][^"\']+["\']',
            f'cover: "{web_path}"',
            content
        )
        # Update figure img src
        content = re.sub(
            r'<img src="[^"]+" alt="([^"]+)" class="w-full rounded-2xl',
            f'<img src="{web_path}" alt="\\1" class="w-full rounded-2xl',
            content
        )

        with open(post_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Image Engine] Updated post frontmatter and figure in {post_file}")

    return True

def load_topics():
    if not TOPICS_FILE.exists():
        print(f"[Error] Topics file not found at: {TOPICS_FILE}")
        return []
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_topics(topics):
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)
        f.write("\n")

def ping_indexnow(url_list):
    """Notify Microsoft Bing, Yandex, and IndexNow engines for instant indexing."""
    if not url_list:
        return
    host = SITE_URL.replace("https://", "").replace("http://", "").split("/")[0]
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": url_list,
    }
    
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[IndexNow] Successfully submitted {len(url_list)} URL(s). HTTP status: {resp.status}")
    except Exception as e:
        print(f"[IndexNow Warning] Could not notify IndexNow (normal during offline/dry-run testing): {e}")

def call_gemini(prompt: str) -> str:
    """Generate article content via Gemini with model fallback and dual key rotation."""
    if not GEMINI_KEYS:
        raise ValueError("No GEMINI_API_KEY configured in environment or ~/.env")

    # Maiden best models
    models_to_try = [
        "gemini-3.8-flash",
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-pro-latest"
    ]
    last_err = None

    for model in models_to_try:
        for idx, key in enumerate(GEMINI_KEYS):
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.35,
                    "maxOutputTokens": 8192
                }
            }
            
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        print(f"[Gemini AI] Successfully generated via {model} (Key {idx+1})")
                        return "".join(part.get("text", "") for part in parts)
            except urllib.error.HTTPError as e:
                last_err = e
                # If 503 (temporary high load), sleep briefly
                if e.code == 503:
                    time.sleep(2)
                print(f"[Gemini Notice] Model {model} with Key {idx+1} notice: HTTP {e.code}. Trying next...")
            except Exception as e:
                last_err = e
                print(f"[Gemini Notice] Model {model} with Key {idx+1} notice: {e}. Trying next...")

    raise RuntimeError(f"All Gemini models and keys exhausted. Last error: {last_err}")

def generate_fallback_article(topic: dict, cover_img: str) -> str:
    """High-quality deterministic fallback generation for AI & Tech articles."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = topic["title"]
    category = topic["category"]
    tags_str = json.dumps(topic["tags"])
    keyword = topic["keyword"]

    affiliate_callout = """
> [!TIP]
> **Cloud Credits & GPU Acceleration**: Looking to deploy these models or run serverless microservices with zero infrastructure costs? Check out our verified guide on claiming **[$1,000+ in Free AWS, Azure & Google Cloud Credits](/p/free-cloud-credits-aws-azure-gcp-guide/)** and high-speed GPU instances for AI inference.
"""

    content = f"""---
title: "{title}"
description: "In-depth technical breakdown and implementation guide for {keyword}. Includes architecture benchmarks, installation commands, code snippets, and production best practices."
date: {today}
categories: ["{category}"]
tags: {tags_str}
cover: "{cover_img}"
toc: true
home: true
---

# {title}

{affiliate_callout}

<figure class="my-6">
  <img src="{cover_img}" alt="{title}" class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 shadow-md object-cover max-h-[420px]" loading="lazy" />
  <figcaption class="text-xs text-center text-slate-500 dark:text-slate-400 mt-2 italic">
    Architecture & Workflow Overview: {title}
  </figcaption>
</figure>

## 1. Executive Summary & Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **Focus Area** | {keyword} |
| **Primary Domain** | {category} |
| **License / Tier** | Open Source / Free Community Tier Available |
| **Compatibility** | Linux (Ubuntu/Debian), macOS (Apple Silicon M1-M4), Windows WSL2 |
| **Primary Execution** | Local Runtime, Docker Container, or Edge Microservice |

---

## 2. Core Architecture & Developer Advantage

Modern artificial intelligence and developer engineering tools have transitioned from monolithic cloud APIs to ultra-fast, decentralized, and agentic workflows. 

The focus of **{keyword}** is to eliminate developer friction, dramatically reduce API inference costs, and provide deterministic, reproducible engineering pipelines. By mastering these setups, engineers can run state-of-the-art models locally, automate repetitive terminal tasks, and ship scalable production microservices.

---

## 3. Step-by-Step Installation & Setup Roadmap

### Step 1: Environment Preparation
Ensure your development environment meets the baseline hardware and runtime requirements:

```bash
# Check Python and Node.js environments
python3 --version
node -v

# Verify hardware acceleration (NVIDIA CUDA or Apple Metal)
nvidia-smi || sysctl -n machdep.cpu.brand_string
```

### Step 2: Package & Dependency Installation
Pull the official runtime and required dependencies:

```bash
# Initialize isolated project environment
python3 -m venv .venv
source .venv/bin/activate

# Install core SDKs and utilities
pip install --upgrade requests rich pydantic httpx
```

### Step 3: Configuration & Execution
Configure environment parameters and initiate the service:

```bash
# Export configuration flags
export AI_MODEL_ENV="production"
export LOG_LEVEL="info"

# Run initialization routine
python3 main.py --verbose
```

---

## 4. Key Performance Benchmarks & Trade-Offs

When deploying this architecture in real-world scenarios, keep the following trade-offs in mind:

1. **Inference Latency vs. Parameter Count**: Smaller quantized models (e.g. 7B/14B Q4_K_M) deliver near-instant token generation (50+ tokens/sec) on consumer laptops, while larger 70B models provide superior reasoning at lower throughput.
2. **Context Window Utilization**: Managing prompt caching and KV-cache compression prevents runaway VRAM consumption during extended multi-turn coding sessions.
3. **Data Privacy**: Local runtime execution guarantees zero data egress, ensuring sensitive source code and proprietary databases remain confidential.

---

## 5. Frequently Asked Questions (FAQs)

### Can I run this without a dedicated high-end GPU?
Yes. Modern quantization methods (GGUF, AWQ) and CPU offloading allow many of these models and developer tools to run on standard modern laptops with 16GB+ of unified RAM.

### Is commercial use permitted under the license?
Most open-source tools featured here are distributed under Apache 2.0, MIT, or permissive open-weights licenses. Always verify the specific model weights repository for custom commercial thresholds.

### How does this compare to closed-source paid alternatives?
Open-source and self-hosted developer tools offer complete privacy, zero per-token billing, and full customization, making them significantly more cost-effective for high-volume pipelines.

---

## 6. Official Resources & Next Steps

Continue exploring next-generation developer tooling by browsing our [AI Tools](/categories/ai-tools/) library and staying subscribed to our RSS feed for immediate alerts on breakthrough model releases.
"""
    return content

def generate_article(topic: dict) -> str:
    """Generate article via Gemini API or fallback, complete with respected cover image."""
    keyword = topic["keyword"]
    category = topic["category"]
    title = topic["title"]
    tags = ", ".join(topic["tags"])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Resolve and download respected image
    cover_img = resolve_and_download_image(topic)

    prompt = f"""
You are an expert AI researcher, principal software engineer, and technical author for "Tech & AI Radar".
Write an extensive, comprehensive, highly authoritative 1,800-word guide for:
Topic: "{keyword}"
Title: "{title}"
Category: "{category}"
Tags: {tags}
Cover Image: "{cover_img}"
Date: {today}

Requirements:
1. Strict Markdown format with YAML frontmatter at the top:
---
title: "{title}"
description: "In-depth technical breakdown of {keyword}..."
date: {today}
categories: ["{category}"]
tags: {json.dumps(topic["tags"])}
cover: "{cover_img}"
toc: true
home: true
---
2. Include an in-article respected image figure:
<figure class="my-6">
  <img src="{cover_img}" alt="{title}" class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 shadow-md object-cover max-h-[420px]" loading="lazy" />
  <figcaption class="text-xs text-center text-slate-500 dark:text-slate-400 mt-2 italic">
    Architecture & Workflow Overview: {title}
  </figcaption>
</figure>
3. Include an Executive Summary / Technical Specifications Markdown table.
4. Provide copy-pasteable terminal commands, bash scripts, or Python code snippets.
5. Provide detailed architectural analysis, memory/hardware benchmarks, and production best practices.
6. Include a developer resource tip box (recommending free cloud credits or developer tool perks).
7. Include 4-5 comprehensive FAQ entries.
8. Return ONLY the raw Markdown document without enclosing markdown code fences.
"""

    if GEMINI_KEYS:
        try:
            print(f"[Gemini AI] Drafting article for: {title}...")
            content = call_gemini(prompt)
            # Strip enclosing ```markdown if Gemini added it
            content = re.sub(r"^```markdown\s*", "", content.strip(), flags=re.MULTILINE)
            content = re.sub(r"^```\s*", "", content.strip(), flags=re.MULTILINE)
            content = re.sub(r"```$", "", content.strip())
            return content
        except Exception as e:
            print(f"[Gemini API Warning] {e}. Falling back to high-grade structured generator.")
            return generate_fallback_article(topic, cover_img)
    else:
        return generate_fallback_article(topic, cover_img)

def publish_next_topics(count=1, dry_run=False, specific_id=None):
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    topics = load_topics()
    
    pending_topics = [t for t in topics if t.get("status") == "pending"]
    if specific_id:
        pending_topics = [t for t in topics if t.get("id") == specific_id]

    if not pending_topics:
        print("[Info] No pending topics in queue.")
        return []

    published_urls = []
    to_process = pending_topics[:count]

    for topic in to_process:
        slug = topic.get("slug") or topic["id"]
        filename = f"{slug}.md"
        target_path = POSTS_DIR / filename

        print(f"[Publishing] '{topic['title']}' -> {filename}")
        content = generate_article(topic)

        if dry_run:
            print(f"--- [DRY RUN PREVIEW ({filename})] ---")
            print(content[:500] + "...\n[truncated]")
        else:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Update topic record
            topic["status"] = "published"
            topic["published_date"] = datetime.now(timezone.utc).isoformat()
            topic["slug"] = slug
            article_url = f"{SITE_URL}/p/{slug}/"
            published_urls.append(article_url)
            print(f"[Success] Written to {target_path}")

    if not dry_run:
        save_topics(topics)
        ping_indexnow(published_urls)

    return published_urls

def main():
    parser = argparse.ArgumentParser(description="Autonomous Tech & AI Radar Publisher")
    parser.add_argument("--count", type=int, default=1, help="Number of pending topics to publish")
    parser.add_argument("--dry-run", action="store_true", help="Preview output without writing or indexing")
    parser.add_argument("--seed", type=int, default=0, help="Bulk publish initial cornerstone topics")
    parser.add_argument("--id", type=str, default="", help="Publish a specific topic ID")
    parser.add_argument("--set-image", nargs=2, metavar=("SLUG", "SOURCE"), help="Set or replace cover image for a slug (URL or file)")

    args = parser.parse_args()

    if args.set_image:
        slug, source = args.set_image
        print(f"[Custom Image] Setting image for '{slug}' from {source}...")
        success = set_custom_image_for_post(slug, source)
        sys.exit(0 if success else 1)

    count = args.seed if args.seed > 0 else args.count
    specific_id = args.id if args.id else None

    print(f"==================================================")
    print(f"    Tech & AI Radar Autonomous Publishing Engine   ")
    print(f"    Target: {SITE_URL}")
    print(f"    Gemini AI: {'Active (Gemini 3.8 Flash / Dual Key Rotation)' if GEMINI_KEYS else 'Offline / Structured Fallback'}")
    print(f"==================================================")

    urls = publish_next_topics(count=count, dry_run=args.dry_run, specific_id=specific_id)
    print(f"[Done] Total articles published: {len(urls)}")

if __name__ == "__main__":
    main()

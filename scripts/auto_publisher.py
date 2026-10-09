#!/usr/bin/env python3
"""
Opportunity Radar - Autonomous 24/7 Content Publisher Engine
Powered by Google Gemini API + IndexNow Instant Search Engine Indexing
"""

import os
import sys
import json
import re
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
TOPICS_FILE = ROOT_DIR / "data" / "topics.json"
POSTS_DIR = ROOT_DIR / "src" / "content" / "posts"

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
GEMINI_KEYS = [
    k for k in [
        os.environ.get("GEMINI_API_KEY", ""),
        os.environ.get("GEMINI_API_KEY_2", "")
    ] if k
]

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
    """Generate article content via Gemini 3.8 Flash using key rotation."""
    if not GEMINI_KEYS:
        raise ValueError("No GEMINI_API_KEY configured in environment or ~/.env")

    models_to_try = ["gemini-flash-latest", "gemini-3.8-flash", "gemini-3.7-flash"]
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
                    "temperature": 0.5,
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
            except Exception as e:
                last_err = e
                print(f"[Gemini Notice] Model {model} with Key {idx+1} notice: {e}. Trying next...")

    raise RuntimeError(f"All Gemini models and keys exhausted. Last error: {last_err}")

def generate_fallback_article(topic: dict) -> str:
    """High-quality fallback generation to ensure robust offline testing and initial seeding."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = topic["title"]
    category = topic["category"]
    tags_str = json.dumps(topic["tags"])
    slug = topic["slug"]
    keyword = topic["keyword"]

    is_scholarship = category == "Scholarships"
    is_dev = category == "Developer Tools"

    affiliate_box = ""
    if is_scholarship or topic.get("target_affiliate") == "wise":
        affiliate_box = """
> [!TIP]
> **Pro Tip for International Applicants**: When traveling abroad or receiving international stipend disbursements, standard retail banks take 3%–5% in hidden currency conversion markups. We recommend opening a free **[Wise Multi-Currency Student Account](https://wise.com)** to receive international funds in EUR, USD, and GBP with zero hidden markups.
"""
    elif is_dev:
        affiliate_box = """
> [!TIP]
> **Cloud Credits & IDE Perk**: Combine this guide with your verified academic email to activate free JetBrains licenses and $1,000+ in AWS and Azure student credits.
"""

    content = f"""---
title: "{title}"
description: "Comprehensive step-by-step application blueprint for {keyword}. Includes eligibility criteria, funding details, deadline alerts, and required documents."
date: {today}
categories: ["{category}"]
tags: {tags_str}
cover: "/img/brand/solitude-banner.webp"
toc: true
home: true
---

# {title}

{affiliate_box}

## 1. Quick Opportunity Snapshot (Key Highlights)

| Feature | Details |
| :--- | :--- |
| **Program / Opportunity** | {keyword} |
| **Funding Level** | Fully Funded / 100% Tuition Waiver + Monthly Living Allowance |
| **Eligible Degree Levels** | Bachelor's, Master's, Doctoral & Professional Fellowships |
| **Coverage Scope** | Airfare, Health Insurance, Monthly Stipend & Research Grants |
| **Application Cycle** | 2026 / 2027 Academic Year |

---

## 2. Program Overview & Strategic Importance

Securing an international scholarship or top-tier developer grant represents one of the highest return-on-investment pathways available to students and researchers worldwide. 

The **{keyword}** is designed to foster global academic exchange and empower high-achieving scholars. Successful candidates benefit not only from full tuition relief, but also gain access to world-class research facilities, global alumni networks, and institutional mentorship.

---

## 3. Financial Benefits & Complete Funding Package

Recipients of this opportunity receive an all-inclusive financial support structure designed to alleviate all cost-of-living constraints:

1. **Full Tuition Waiver**: 100% exemption from all university admission and administrative fees.
2. **Monthly Living Stipend**: Competitive monthly allowance pegged to local cost of living to support accommodation and daily meals.
3. **Round-Trip Travel Allowance**: Direct flight subsidies from your home country to the host institution and return upon completion.
4. **Comprehensive Health & Accident Insurance**: Mandatory health cover throughout the full duration of your study stay.
5. **Research & Conference Allowance**: Special grants dedicated to field research, thesis publication, and international conferences.

---

## 4. Eligibility Checklist & Criteria

To qualify for consideration, candidates must meet the core prerequisites:

- **Academic Merit**: A strong undergraduate or graduate track record with demonstrated academic rigor.
- **Language Proficiency**: Proficiency in the language of instruction (English or host nation tongue). Many programs waive official tests if your prior degree was English-taught.
- **Statement of Motivation**: A persuasive, well-researched Statement of Purpose (SOP) articulating your academic goals.
- **Letters of Recommendation**: 2 academic or professional references attesting to your capabilities.

---

## 5. Step-by-Step Application Roadmap

Follow this structured roadmap to submit a competitive application:

1. **Phase 1: Program Research & University Selection**
   - Review eligible universities and partner faculties.
   - Confirm program-specific deadlines and advisor availability.

2. **Phase 2: Document Compilation & Verification**
   - Translate all academic transcripts and degree certificates into English or the host language.
   - Craft a tailored CV following the Europass or international academic format.
   - Finalize your research proposal and motivation essay.

3. **Phase 3: Online Submission**
   - Create your applicant profile on the official application portal.
   - Upload required credentials in PDF format (under 5MB per document).
   - Double-check all entries and submit before the stated cutoff time.

4. **Phase 4: Interview & Award Confirmation**
   - Shortlisted candidates undergo a 20–30 minute virtual panel interview.
   - Official award letters are dispatched within 6 to 8 weeks post-interview.

---

## 6. Frequently Asked Questions (FAQs)

### Is IELTS or TOEFL strictly mandatory?
Many host universities accept an official **English Proficiency Certificate** issued by your previous university if your undergraduate studies were taught entirely in English. Always verify with your specific department.

### Can final-year students apply before graduating?
Yes. Candidates in their final undergraduate or graduate year may apply by submitting their most recent interim transcripts along with a provisional certificate of enrollment.

### Are there any application or processing fees?
The official application process for this program is **100% free of charge**. Never pay third-party agents claiming to guarantee scholarship placement.

---

## 7. Official Portal & Next Steps

Prepare your documentation early to prevent last-minute server congestion on deadline day. Bookmark this guide for reference, and subscribe to our RSS feed to receive immediate alerts on upcoming global scholarship openings.
"""
    return content

def generate_article(topic: dict) -> str:
    """Generate article via Gemini API if key is available, else fallback."""
    keyword = topic["keyword"]
    category = topic["category"]
    title = topic["title"]
    tags = ", ".join(topic["tags"])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    prompt = f"""
You are an expert scholarship advisor, academic counselor, and technical writer for "Opportunity Radar".
Write an extensive, comprehensive, highly authoritative 1,800-word guide for:
Topic: "{keyword}"
Title: "{title}"
Category: "{category}"
Tags: {tags}
Date: {today}

Requirements:
1. Strict Markdown format with YAML frontmatter at the top:
---
title: "{title}"
description: "Comprehensive guide for {keyword}..."
date: {today}
categories: ["{category}"]
tags: {json.dumps(topic["tags"])}
cover: "/img/brand/solitude-banner.webp"
toc: true
home: true
---
2. Include a high-CTR Quick Snapshot Markdown table (Funding, Level, Scope, Deadlines).
3. Detailed breakdown of benefits, monthly stipend, health insurance, and travel coverage.
4. Step-by-step roadmap from document preparation to submission and interviews.
5. In-article partner callout tip (e.g. Wise international student banking for fee-free stipend transfers or dev tools).
6. 4-5 comprehensive FAQ entries.
7. Return ONLY the raw Markdown document without enclosing backticks or markdown fences.
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
            return generate_fallback_article(topic)
    else:
        return generate_fallback_article(topic)

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
            print(content[:400] + "...\n[truncated]")
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
    parser = argparse.ArgumentParser(description="Autonomous Opportunity Radar Publisher")
    parser.add_argument("--count", type=int, default=1, help="Number of pending topics to publish")
    parser.add_argument("--dry-run", action="store_true", help="Preview output without writing or indexing")
    parser.add_argument("--seed", type=int, default=0, help="Bulk publish initial cornerstone topics")
    parser.add_argument("--id", type=str, default="", help="Publish a specific topic ID")

    args = parser.parse_args()

    count = args.seed if args.seed > 0 else args.count
    specific_id = args.id if args.id else None

    print(f"==================================================")
    print(f"  Opportunity Radar Autonomous Publishing Engine   ")
    print(f"  Target: {SITE_URL}")
    print(f"  Gemini API: {'Configured' if GEMINI_KEYS else 'Offline / Deterministic Fallback'}")
    print(f"==================================================")

    urls = publish_next_topics(count=count, dry_run=args.dry_run, specific_id=specific_id)
    print(f"[Done] Total articles published: {len(urls)}")

if __name__ == "__main__":
    main()

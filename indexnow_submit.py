"""
IndexNow URL Submission Script — Backend / Admin Use Only
=========================================================
Submits URLs from the sitemap to Bing IndexNow API.

DO NOT run this in a browser or include it in frontend JS.
Run manually or as part of a post-deploy admin step.

Usage:
    python indexnow_submit.py              # submit all URLs from sitemap
    python indexnow_submit.py --dry-run    # preview without sending
    python indexnow_submit.py --url https://pod.softcoverbooks.co.za/designs/

Requirements: Python 3.8+ (stdlib only — no pip install needed)

IndexNow docs: https://www.indexnow.org/documentation
"""

import json
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
INDEXNOW_API     = "https://api.indexnow.org/IndexNow"
API_KEY          = "213e4add805347a492ede4a5d74ab931"
KEY_LOCATION     = f"https://pod.softcoverbooks.co.za/{API_KEY}.txt"
HOST             = "pod.softcoverbooks.co.za"
SITEMAP_URL      = "https://pod.softcoverbooks.co.za/sitemap.xml"
LOCAL_SITEMAP    = "public/sitemap.xml"   # used as fallback / offline
BATCH_SIZE       = 100                    # IndexNow allows up to 10 000; keep ≤100 for safety
# ─────────────────────────────────────────────────────────────────────────────


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def load_urls_from_local_sitemap(path: str) -> list[str]:
    """Parse URLs out of a local sitemap.xml file."""
    urls: list[str] = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        # Handle the sitemap namespace
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for loc in root.findall(".//sm:loc", ns):
            if loc.text:
                urls.append(loc.text.strip())
    except FileNotFoundError:
        log(f"ERROR: Local sitemap not found at '{path}'")
    except ET.ParseError as exc:
        log(f"ERROR: Failed to parse sitemap XML — {exc}")
    return urls


def load_urls_from_remote_sitemap(sitemap_url: str) -> list[str]:
    """Fetch and parse URLs from a remote sitemap.xml."""
    log(f"Fetching sitemap from {sitemap_url} …")
    try:
        with urllib.request.urlopen(sitemap_url, timeout=15) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        return [
            loc.text.strip()
            for loc in root.findall(".//sm:loc", ns)
            if loc.text
        ]
    except Exception as exc:
        log(f"WARNING: Could not fetch remote sitemap ({exc}). Falling back to local file.")
        return []


def submit_batch(urls: list[str], dry_run: bool = False) -> bool:
    """Submit a batch of URLs to the IndexNow API via HTTP POST."""
    payload = {
        "host":        HOST,
        "key":         API_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList":     urls,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    if dry_run:
        log(f"[DRY-RUN] Would POST {len(urls)} URL(s) to {INDEXNOW_API}")
        for u in urls:
            print(f"  -> {u}")
        return True

    req = urllib.request.Request(
        INDEXNOW_API,
        data=body,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent":   "IndexNow-Submit/1.0 (pod.softcoverbooks.co.za)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = resp.status
    except urllib.error.HTTPError as exc:
        status = exc.code
        body_text = exc.read().decode("utf-8", errors="replace")
        log(f"ERROR: HTTP {status} from IndexNow API — {body_text}")
        return False
    except urllib.error.URLError as exc:
        log(f"ERROR: Network error — {exc.reason}")
        return False

    # 200 = OK (URL submitted), 202 = Accepted (queued)
    if status in (200, 202):
        log(f"OK: Submitted {len(urls)} URL(s) -- HTTP {status}")
        return True
    else:
        log(f"WARNING: Unexpected HTTP {status} from IndexNow API")
        return False


def main() -> None:
    args = sys.argv[1:]
    dry_run       = "--dry-run" in args
    single_urls   = [a for a in args if a.startswith("http") and "--" not in a]

    if dry_run:
        log("=== DRY-RUN MODE — no requests will be sent ===")

    # ── Determine URL list ────────────────────────────────────────────────────
    if single_urls:
        urls = single_urls
        log(f"Single-URL mode: {urls}")
    else:
        # Try remote sitemap first, fall back to local copy
        urls = load_urls_from_remote_sitemap(SITEMAP_URL)
        if not urls:
            log(f"Falling back to local sitemap: {LOCAL_SITEMAP}")
            urls = load_urls_from_local_sitemap(LOCAL_SITEMAP)

    if not urls:
        log("No URLs found. Aborting.")
        sys.exit(1)

    log(f"Total URLs to submit: {len(urls)}")

    # ── Submit in batches ─────────────────────────────────────────────────────
    success = True
    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i : i + BATCH_SIZE]
        log(f"Submitting batch {i // BATCH_SIZE + 1} ({len(batch)} URLs) …")
        if not submit_batch(batch, dry_run=dry_run):
            success = False

    if success:
        log("All batches submitted successfully.")
    else:
        log("One or more batches failed — check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

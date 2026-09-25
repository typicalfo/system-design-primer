#!/usr/bin/env python3
"""Request external http(s) URLs from the same docs as check_links.py.

Stdlib only. URLs are deduped. Each request uses a timeout and a browser-like
User-Agent, HEAD first and GET if HEAD is refused or fails. Concurrency is
capped. Exit status is 0 unless --strict is passed, in which case any failed
URL exits 1.

Repo-local GitHub links (blob/tree on typicalfo/system-design-primer) are
skipped. scripts/check_links.py checks those against the working tree, and
master may not contain uncommitted files yet.

README.md is limited to the fork preamble and Enterprise update callouts.
TRANSLATIONS.md is limited to the fork note. The original study guide is not
fetched.

Hosts in IGNORE_HOSTS are reported and are not failures. Add a host only when
it rejects this client and the page is still a real document.

    python3 scripts/check_external_links.py
    python3 scripts/check_external_links.py --strict
"""

from __future__ import annotations

import argparse
import re
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_links  # noqa: E402

URL_RE = re.compile(r"https?://[^\s<>\]\)\"'`]+")
REPO_LOCAL = re.compile(
    r"^https://github\.com/typicalfo/system-design-primer/(blob|tree)/master/"
)
TRAILING = ".,;:\"'`>"
USER_AGENT = (
    "system-design-primer-link-check/1.0 "
    "(+https://github.com/typicalfo/system-design-primer)"
)
TIMEOUT = 20
WORKERS = 8

# Sites that answer a real page to browsers and reject this checker.
# example.com is the RFC 2606 documentation host used in sample payloads.
IGNORE_HOSTS: set[str] = {"example.com"}


def collect_urls() -> tuple[list[str], list[str]]:
    found: set[str] = set()
    skipped: set[str] = set()
    for path in check_links.iter_files():
        text = path.read_text(encoding="utf-8")
        scanned = check_links.scanned_text(path, text)
        for raw in URL_RE.findall(scanned):
            # An ellipsis in prose ("blob/master/...") is not a URL.
            if "..." in raw:
                continue
            url = raw.rstrip(TRAILING)
            if not url:
                continue
            if REPO_LOCAL.match(url):
                skipped.add(url)
                continue
            found.add(url)
    return sorted(found), sorted(skipped)


def host_of(url: str) -> str:
    host = urlsplit(url).hostname or ""
    return host.lower()


def request(url: str, method: str) -> tuple[int | None, str]:
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CONTEXT) as resp:
            if method == "GET":
                resp.read(512)
            code = resp.getcode()
            return code, ""
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc.reason)
    except urllib.error.URLError as exc:
        return None, str(exc.reason)
    except TimeoutError as exc:
        return None, str(exc)
    except OSError as exc:
        return None, str(exc)


def check_one(url: str) -> tuple[str, str, str]:
    """Return (status, url, detail). status is ok, fail, or ignored."""
    host = host_of(url)
    if host in IGNORE_HOSTS:
        return "ignored", url, "ignore list"
    code, detail = request(url, "HEAD")
    if code is not None and 200 <= code < 300:
        return "ok", url, str(code)
    get_code, get_detail = request(url, "GET")
    if get_code is not None and 200 <= get_code < 300:
        return "ok", url, f"GET {get_code} after HEAD {code}"
    shown = get_code if get_code is not None else code
    reason = get_detail or detail or "no response"
    return "fail", url, f"{shown} {reason}".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 when any URL fails",
    )
    args = parser.parse_args()
    urls, skipped = collect_urls()
    results: list[tuple[str, str, str]] = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(check_one, url) for url in urls]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: item[1])
    ok = [item for item in results if item[0] == "ok"]
    failed = [item for item in results if item[0] == "fail"]
    ignored = [item for item in results if item[0] == "ignored"]
    print(
        f"checked {len(urls)} unique URLs; "
        f"ok {len(ok)}; failed {len(failed)}; ignored {len(ignored)}; "
        f"skipped {len(skipped)} repo-local GitHub URLs"
    )
    for _status, url, detail in ok:
        print(f"ok {detail} {url}")
    for _status, url, detail in ignored:
        print(f"ignored {detail} {url}")
    for _status, url, detail in failed:
        print(f"fail {detail} {url}")
    if skipped:
        print("skipped repo-local GitHub URLs (checked by scripts/check_links.py):")
        for url in skipped:
            print(f"skip {url}")
    if args.strict and failed:
        return 1
    return 0


SSL_CONTEXT = ssl.create_default_context()


if __name__ == "__main__":
    sys.exit(main())

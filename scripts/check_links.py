#!/usr/bin/env python3
"""Check relative Markdown links and frontmatter `related` paths.

Covers enterprise/, patterns/, templates/, pack/, AGENTS.md, CLAUDE.md,
CONTRIBUTING.md, llms.txt, and the fork additions in README.md (the preamble
plus callouts).
External URLs are not fetched. Standard library only.

    python3 scripts/check_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
RELATED_RE = re.compile(r"^related:\s*(?:\[(.*?)\]\s*)?$", re.MULTILINE)


def strip_fences(text: str) -> str:
    return FENCE_RE.sub("", text)


def github_slugs(text: str) -> set[str]:
    body = strip_fences(text)
    seen: dict[str, int] = {}
    slugs: set[str] = set()
    for match in HEADING_RE.finditer(body):
        raw = re.sub(r"<[^>]+>", "", match.group(2))
        slug = raw.strip().lower()
        slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
        slug = re.sub(r"\s+", "-", slug).strip("-")
        if not slug:
            continue
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        slugs.add(slug if n == 0 else f"{slug}-{n}")
    return slugs


def parse_target(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    if raw.startswith("<"):
        end = raw.find(">")
        if end != -1:
            return unquote(raw[1:end].strip())
    return unquote(raw.split()[0])


def frontmatter_related(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---\n", 4)
    if end == -1:
        return []
    raw = text[4:end]
    paths: list[str] = []
    in_related = False
    for line in raw.splitlines():
        if line.startswith("related:"):
            rest = line.split(":", 1)[1].strip()
            in_related = True
            if rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
                if inner:
                    paths.extend(
                        p.strip().strip("\"'") for p in inner.split(",") if p.strip()
                    )
                in_related = False
            continue
        if in_related:
            if line.startswith("  - "):
                paths.append(line[4:].strip().strip("\"'"))
                continue
            in_related = False
    return paths


def iter_files() -> list[Path]:
    files: list[Path] = []
    for name in ("enterprise", "patterns", "templates", "pack"):
        base = ROOT / name
        if base.exists():
            files.extend(p for p in base.rglob("*.md") if p.is_file())
    for name in ("AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "llms.txt", "README.md"):
        p = ROOT / name
        if p.exists():
            files.append(p)
    return files


def readme_addition_text(text: str) -> str:
    lines = text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.startswith("*[English]")),
        len(lines),
    )
    chunks = ["\n".join(lines[:start])]
    i = start
    while i < len(lines):
        if lines[i].startswith("> **Enterprise update (fork):**"):
            block = [lines[i]]
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i])
                i += 1
            chunks.append("\n".join(block))
        else:
            i += 1
    return "\n".join(chunks)


def check_file(path: Path, text: str, errors: list[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    scanned = readme_addition_text(text) if path.name == "README.md" and path.parent == ROOT else text
    slugs_cache: dict[Path, set[str]] = {path: github_slugs(text)}

    def slugs_for(target: Path) -> set[str]:
        if target not in slugs_cache:
            if target.suffix.lower() in {".md", ".txt"} and target.exists():
                slugs_cache[target] = github_slugs(target.read_text(encoding="utf-8"))
            else:
                slugs_cache[target] = set()
        return slugs_cache[target]

    for raw in LINK_RE.findall(strip_fences(scanned)):
        target = parse_target(raw)
        if not target or target.startswith(("http://", "https://", "mailto:", "irc:")):
            continue
        path_part, _, frag = target.partition("#")
        if path_part == "":
            if frag and frag not in slugs_for(path):
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        resolved = (path.parent / path_part).resolve()
        if not resolved.exists():
            errors.append(f"{rel}: missing file {target}")
            continue
        if frag and resolved.suffix.lower() in {".md", ".txt"}:
            if frag not in slugs_for(resolved):
                errors.append(f"{rel}: missing anchor {target}")

    for rel_path in frontmatter_related(text if path.name != "README.md" else scanned):
        path_part, _, frag = rel_path.partition("#")
        resolved = (path.parent / path_part).resolve()
        if not resolved.exists():
            errors.append(f"{rel}: frontmatter related missing {rel_path}")
            continue
        if frag and frag not in slugs_for(resolved):
            errors.append(f"{rel}: frontmatter related missing anchor {rel_path}")


def main() -> int:
    errors: list[str] = []
    files = iter_files()
    for path in files:
        text = path.read_text(encoding="utf-8")
        check_file(path, text, errors)
    if errors:
        print(f"{len(errors)} broken links")
        for err in errors:
            print(err)
        return 1
    print(f"ok ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

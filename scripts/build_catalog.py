#!/usr/bin/env python3
"""Regenerate catalog.json, llms.txt, llms-full.txt, llms-full/, and README counts.

    pip install -r scripts/requirements.txt
    python3 scripts/build_catalog.py
    python3 scripts/build_catalog.py --check

--check regenerates every output in memory and exits non-zero if a committed
file differs or if llms-full/ contains a file this run would not generate.
It does not write.

source_hash is SHA-256 over catalogued documents in path order. For each
document the hash is updated with an 8-byte big-endian UTF-8 path length, the
path, an 8-byte big-endian file length, and the raw file bytes. No commit id
and no timestamp.

Enterprise full text stays one file, llms-full/enterprise.txt, while that
rendered file is at most MAX_FULL bytes. If the rendered enterprise bundle
would exceed the cap, the generator writes llms-full/enterprise-<subfolder>.txt
per subfolder instead, and keeps files that sit directly in enterprise/ in
llms-full/enterprise.txt. A file that still exceeds the cap is an error.
Nothing is deleted to get under the cap.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "PyYAML is required. Run: pip install -r scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
MAX_FULL = 1_000_000
SCAN_ROOTS = ("enterprise", "patterns", "templates", "pack")
GITHUB = "https://github.com/typicalfo/system-design-primer"
REPO_URL = re.compile(
    r"^https://github\.com/typicalfo/system-design-primer/(blob|tree)/master/([^?#]+)"
)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")

REQUIRED_DOC_FIELDS = (
    "title",
    "summary",
    "tags",
    "when_to_use",
    "related",
    "last_reviewed",
)
TYPES = (
    "doc",
    "example",
    "pattern",
    "reference-architecture",
    "skill",
    "template",
)

# Display order for llms.txt enterprise subfolders. Unknown folders are
# appended after these, sorted by folder name.
ENTERPRISE_ORDER = (
    "identity",
    "security",
    "tenancy",
    "compliance",
    "reliability",
    "observability",
    "data",
    "apis",
    "delivery",
    "cost",
    "organization",
    "modernization",
    "ai",
    "reference-architectures",
)
ENTERPRISE_TITLES = {
    "identity": "Identity",
    "security": "Security",
    "tenancy": "Tenancy",
    "compliance": "Compliance",
    "reliability": "Reliability",
    "observability": "Observability",
    "data": "Data",
    "apis": "APIs",
    "delivery": "Delivery",
    "cost": "Cost",
    "organization": "Organization",
    "modernization": "Modernization",
    "ai": "AI",
    "reference-architectures": "Reference architectures",
}

START_HERE = (
    ("AGENTS.md", "How a coding agent should use this repo and which files to load."),
    ("README.md", "Fork landing page, then the original System Design Primer study guide."),
    ("CONTRIBUTING.md", "Pull-request conventions, frontmatter, and how to regenerate the catalog."),
    ("CHANGELOG.md", "Notable changes to this fork."),
    ("catalog.json", "Machine-readable index of every catalogued doc (schema version 2)."),
    ("llms-full.txt", "Index of the full-text bundles under llms-full/."),
)

COUNTS_START = "<!-- counts:start -->"
COUNTS_END = "<!-- counts:end -->"

errors: list[str] = []


def err(path: str, reason: str) -> None:
    errors.append(f"{path}: {reason}")


def flush_errors() -> None:
    if not errors:
        return
    for line in errors:
        print(line, file=sys.stderr)
    sys.exit(1)


def iter_docs() -> list[Path]:
    found: list[Path] = []
    for root_name in SCAN_ROOTS:
        base = ROOT / root_name
        if base.exists():
            found.extend(p for p in base.rglob("*.md") if p.is_file())
    return sorted(found, key=lambda p: p.relative_to(ROOT).as_posix())


def split_frontmatter(text: str, rel: str) -> tuple[object, str]:
    if not text.startswith("---\n"):
        err(rel, "missing YAML frontmatter")
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        err(rel, "unterminated YAML frontmatter")
        return None, text
    raw = text[4:end]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        err(rel, f"invalid YAML: {exc}")
        return None, text[end + 5 :]
    return data, text[end + 5 :]


def classify(rel: str) -> str:
    if rel.startswith("pack/skills/") and rel.endswith("/SKILL.md"):
        return "skill"
    if rel.startswith("pack/examples/"):
        return "example"
    if rel.startswith("enterprise/reference-architectures/") and not rel.endswith(
        "/README.md"
    ):
        return "reference-architecture"
    if rel.startswith("templates/") and not rel.endswith("/README.md"):
        return "template"
    if rel.startswith("patterns/") and not rel.endswith("/README.md"):
        return "pattern"
    return "doc"


def normalize_date(value: object, rel: str) -> str | None:
    if isinstance(value, dt.datetime):
        if (
            value.hour
            or value.minute
            or value.second
            or value.microsecond
            or value.tzinfo is not None
        ):
            err(rel, f"last_reviewed is not a date: {value!r}")
            return None
        value = value.date()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, str):
        try:
            parsed = dt.date.fromisoformat(value)
        except ValueError:
            err(rel, f"last_reviewed is not a valid date: {value!r}")
            return None
        if parsed.isoformat() != value:
            err(rel, f"last_reviewed must be YYYY-MM-DD: {value!r}")
            return None
        return value
    err(rel, f"last_reviewed is not a valid date: {value!r}")
    return None


def plain_summary(value: object, rel: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        err(rel, "missing required field summary")
        return None
    text = " ".join(value.split())
    if text.startswith("#") or MARKDOWN_LINK.search(text):
        err(rel, "summary must be plain text, not a heading or a markdown link")
        return None
    return text


def require_text(meta: dict, field: str, rel: str) -> str | None:
    value = meta.get(field)
    if not isinstance(value, str) or not value.strip():
        err(rel, f"missing required field {field}")
        return None
    return " ".join(value.split())


def normalize_related(doc: Path, item: object, rel: str) -> str | None:
    if not isinstance(item, str) or not item.strip():
        err(rel, f"related entry is not a path: {item!r}")
        return None
    path_part = item.strip().split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        err(rel, f"related path does not exist: {item}")
        return None
    if path_part.startswith(("http://", "https://", "/")):
        err(rel, f"related must be a relative path: {item}")
        return None
    resolved = (doc.parent / path_part).resolve()
    try:
        repo_rel = resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        err(rel, f"related path does not exist: {item}")
        return None
    if not resolved.exists():
        err(rel, f"related path does not exist: {item}")
        return None
    return repo_rel


def repo_path_from_link(doc: Path, target: str) -> str | None:
    """Return a repo-relative path for a markdown link target, or None to skip."""
    target = target.strip()
    if not target or target.startswith(("mailto:", "irc:", "#")):
        return None
    base, _, _frag = target.partition("#")
    base = base.split("?", 1)[0].strip()
    if not base:
        return None
    match = REPO_URL.match(base)
    if match:
        repo_rel = match.group(2).strip("/")
        resolved = (ROOT / repo_rel).resolve()
    elif base.startswith(("http://", "https://")):
        return None
    else:
        resolved = (doc.parent / base).resolve()
        try:
            repo_rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            err(doc.relative_to(ROOT).as_posix(), f"link leaves the repo: {target}")
            return None
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        err(doc.relative_to(ROOT).as_posix(), f"link leaves the repo: {target}")
        return None
    if not resolved.exists():
        rel = doc.relative_to(ROOT).as_posix()
        err(rel, f"related path does not exist: {target}")
        return None
    return resolved.relative_to(ROOT.resolve()).as_posix()


def related_from_body(doc: Path, body: str) -> list[str]:
    self_rel = doc.relative_to(ROOT).as_posix()
    found: list[str] = []
    seen: set[str] = set()
    scanned = FENCE_RE.sub("", body)
    for raw in LINK_RE.findall(scanned):
        url = raw.strip().split()[0] if raw.strip() else ""
        if url.startswith("<") and url.endswith(">"):
            url = url[1:-1]
        repo_rel = repo_path_from_link(doc, url)
        if not repo_rel or repo_rel == self_rel or repo_rel in seen:
            continue
        seen.add(repo_rel)
        found.append(repo_rel)
    return found


def parse_doc(path: Path) -> dict | None:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    nlines = len(text.splitlines())
    if nlines > 300:
        err(rel, f"{nlines} lines exceeds 300")
    data, body = split_frontmatter(text, rel)
    kind = classify(rel)
    if data is None:
        return None
    if not isinstance(data, dict):
        err(rel, "invalid YAML: frontmatter must be a mapping")
        return None
    section = rel.split("/", 1)[0]
    if kind == "skill":
        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not name.strip():
            err(rel, "missing required field name")
            name = ""
        else:
            name = name.strip()
        if not isinstance(description, str) or not description.strip():
            err(rel, "missing required field description")
            description = ""
        else:
            description = " ".join(description.split())
            if not description.startswith("Use this when"):
                err(rel, "description must start with 'Use this when'")
        return {
            "path": path,
            "rel": rel,
            "kind": kind,
            "section": section,
            "title": name,
            "summary": description,
            "tags": ["skill"],
            "when_to_use": description,
            "related": related_from_body(path, body),
            "last_reviewed": None,
            "text": text,
        }
    for field in REQUIRED_DOC_FIELDS:
        if field not in data:
            err(rel, f"missing required field {field}")
    title = require_text(data, "title", rel) if "title" in data else None
    summary = plain_summary(data.get("summary"), rel) if "summary" in data else None
    when = require_text(data, "when_to_use", rel) if "when_to_use" in data else None
    tags = data.get("tags") if "tags" in data else None
    if "tags" in data:
        if not isinstance(tags, list) or len(tags) == 0:
            err(rel, "empty tags")
            tags = []
        elif any(not isinstance(tag, str) or not tag.strip() for tag in tags):
            err(rel, "empty tags")
            tags = []
        else:
            tags = [tag.strip() for tag in tags]
    related_raw = data.get("related") if "related" in data else None
    related: list[str] = []
    if "related" in data:
        if not isinstance(related_raw, list):
            err(rel, "related must be a list of paths")
        else:
            seen: set[str] = set()
            for item in related_raw:
                norm = normalize_related(path, item, rel)
                if norm and norm not in seen:
                    seen.add(norm)
                    related.append(norm)
    reviewed = None
    if "last_reviewed" in data:
        reviewed = normalize_date(data.get("last_reviewed"), rel)
    if title is None or summary is None or when is None or tags is None or reviewed is None:
        return None
    return {
        "path": path,
        "rel": rel,
        "kind": kind,
        "section": section,
        "title": title,
        "summary": summary,
        "tags": tags,
        "when_to_use": when,
        "related": related,
        "last_reviewed": reviewed,
        "text": text,
    }


def apply_skill_dates(docs: list[dict]) -> None:
    for doc in docs:
        if doc["kind"] != "skill":
            continue
        prefix = str(Path(doc["rel"]).parent.as_posix()) + "/"
        dates = [
            other["last_reviewed"]
            for other in docs
            if other["rel"].startswith(prefix)
            and not other["rel"].endswith("/SKILL.md")
            and other["last_reviewed"]
        ]
        doc["last_reviewed"] = max(dates) if dates else None


def source_hash(docs: list[dict]) -> str:
    digest = hashlib.sha256()
    for doc in docs:
        rel_b = doc["rel"].encode("utf-8")
        data = doc["path"].read_bytes()
        digest.update(len(rel_b).to_bytes(8, "big"))
        digest.update(rel_b)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def catalog_object(docs: list[dict]) -> dict:
    by_type = {name: 0 for name in TYPES}
    by_section: dict[str, int] = {}
    entries = []
    for doc in docs:
        by_type[doc["kind"]] = by_type.get(doc["kind"], 0) + 1
        by_section[doc["section"]] = by_section.get(doc["section"], 0) + 1
        entries.append(
            {
                "path": doc["rel"],
                "type": doc["kind"],
                "section": doc["section"],
                "title": doc["title"],
                "summary": doc["summary"],
                "tags": doc["tags"],
                "when_to_use": doc["when_to_use"],
                "related": doc["related"],
                "last_reviewed": doc["last_reviewed"],
            }
        )
    return {
        "schema_version": 2,
        "source_hash": source_hash(docs),
        "counts": {
            "total": len(entries),
            "by_type": by_type,
            "by_section": {key: by_section[key] for key in sorted(by_section)},
        },
        "entries": entries,
    }


def dump_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def section_title(folder: str) -> str:
    if folder in ENTERPRISE_TITLES:
        return ENTERPRISE_TITLES[folder]
    return " ".join(part.capitalize() for part in folder.split("-"))


def llms_group(rel: str) -> tuple[int, str, str]:
    """Sort key (order, title, path-tiebreak) and the H2 title is element 1."""
    parts = rel.split("/")
    top = parts[0]
    if top == "pack":
        if len(parts) > 1 and parts[1] == "examples":
            return (300, "Examples", rel)
        return (10, "Skills pack", rel)
    if top == "patterns":
        return (200, "Pattern cards", rel)
    if top == "templates":
        return (210, "Templates", rel)
    if top == "enterprise":
        if len(parts) == 2:
            return (20, "Enterprise guide", rel)
        folder = parts[1]
        if folder in ENTERPRISE_ORDER:
            return (30 + ENTERPRISE_ORDER.index(folder), section_title(folder), rel)
        return (80, section_title(folder), rel)
    return (400, section_title(top), rel)


def render_llms(docs: list[dict]) -> str:
    lines = [
        "# System Design Primer (enterprise fork)",
        "",
        "> Enterprise-augmented fork of Donne Martin's System Design Primer (CC BY 4.0). Original study guide preserved; guides, pattern cards, templates, and skills cover production systems.",
        "",
        "Generated by scripts/build_catalog.py. Do not edit by hand. The file list follows the llms.txt convention at https://llmstxt.org/.",
        "",
        "## Start here",
        "",
    ]
    for path, summary in START_HERE:
        lines.append(f"- [{path}]({path}): {summary}")
    grouped: dict[tuple[int, str], list[dict]] = {}
    for doc in docs:
        order, title, _rel = llms_group(doc["rel"])
        grouped.setdefault((order, title), []).append(doc)
    seen_paths: list[str] = []
    for key in sorted(grouped):
        title = key[1]
        lines.extend(["", f"## {title}", ""])
        for doc in sorted(grouped[key], key=lambda item: item["rel"]):
            lines.append(f"- [{doc['title']}]({doc['rel']}): {doc['summary']}")
            seen_paths.append(doc["rel"])
    expected = [doc["rel"] for doc in docs]
    if seen_paths != expected and sorted(seen_paths) != sorted(expected):
        err("llms.txt", "catalogued docs are not listed exactly once")
    if len(seen_paths) != len(set(seen_paths)) or set(seen_paths) != set(expected):
        err("llms.txt", "catalogued docs are not listed exactly once")
    lines.append("")
    return "\n".join(lines)


def bundle(title: str, intro: list[str], docs: list[Path]) -> str:
    parts = [f"# {title}\n", "\n"]
    for line in intro:
        parts.append(line + "\n")
    parts.append("\n")
    parts.append(f"Docs: {len(docs)}\n")
    parts.append("Generated by scripts/build_catalog.py. Do not edit by hand.\n")
    ordered = sorted(docs, key=lambda path: path.relative_to(ROOT).as_posix())
    for path in ordered:
        rel = path.relative_to(ROOT).as_posix()
        parts.append(f"\n\n---\n\n# Source: {rel}\n\n")
        body = path.read_text(encoding="utf-8")
        parts.append(body)
        if not body.endswith("\n"):
            parts.append("\n")
    return "".join(parts)


def ensure_cap(name: str, text: str) -> None:
    size = len(text.encode("utf-8"))
    if size > MAX_FULL:
        err(
            name,
            f"{size} bytes exceeds the {MAX_FULL}-byte cap. "
            "Refusing to write or drop this file. Split the section further and re-run.",
        )


def enterprise_files(docs: list[dict]) -> list[Path]:
    return [doc["path"] for doc in docs if doc["section"] == "enterprise"]


def render_enterprise(docs: list[dict]) -> tuple[dict[str, str], tuple[int, bool]]:
    files = enterprise_files(docs)
    combined = bundle(
        "Enterprise guide",
        ["Catalogued docs under enterprise/, in path order."],
        files,
    )
    current = len(combined.encode("utf-8"))
    if current <= MAX_FULL:
        return {"enterprise.txt": combined}, (current, False)
    groups: dict[str, list[Path]] = {}
    for path in files:
        rel = path.relative_to(ROOT / "enterprise")
        key = rel.parts[0] if len(rel.parts) > 1 else ""
        groups.setdefault(key, []).append(path)
    outputs: dict[str, str] = {}
    for key in sorted(groups):
        name = "enterprise.txt" if key == "" else f"enterprise-{key}.txt"
        if key == "":
            intro = [
                "Catalogued docs that sit directly in enterprise/.",
                "Subfolders are in llms-full/enterprise-<subfolder>.txt because the rendered enterprise bundle exceeds the size cap.",
            ]
            heading = "Enterprise guide"
        else:
            intro = [
                f"Catalogued docs under enterprise/{key}/, in path order.",
                "Split from the enterprise bundle because that rendered file exceeds the size cap.",
            ]
            heading = section_title(key)
        text = bundle(heading, intro, groups[key])
        ensure_cap(f"llms-full/{name}", text)
        outputs[name] = text
    return outputs, (current, True)


def render_simple(docs: list[dict], section: str, filename: str, heading: str) -> dict[str, str]:
    files = [doc["path"] for doc in docs if doc["section"] == section]
    text = bundle(
        heading,
        [f"Catalogued docs under {section}/, in path order."],
        files,
    )
    ensure_cap(f"llms-full/{filename}", text)
    return {filename: text}


def render_primer(readme_text: str) -> str:
    body = readme_text
    if not body.endswith("\n"):
        body += "\n"
    text = (
        "# Primer\n"
        "\n"
        "Root README.md of this repository.\n"
        "\n"
        "The original study guide in that file is The System Design Primer by Donne Martin, "
        "copyright 2017, licensed under Creative Commons Attribution 4.0 International "
        "(CC BY 4.0): https://creativecommons.org/licenses/by/4.0/\n"
        "Upstream: https://github.com/donnemartin/system-design-primer\n"
        "\n"
        'The file also contains this fork\'s preamble above the heading "Original study guide". '
        "That preamble is fork text. The study guide below that heading is the original work, "
        'aside from callouts marked "Enterprise update (fork)".\n'
        "\n"
        "Docs: 1\n"
        "Generated by scripts/build_catalog.py. Do not edit by hand.\n"
        "\n"
        "\n---\n\n"
        "# Source: README.md\n"
        "\n"
        f"{body}"
    )
    ensure_cap("llms-full/primer.txt", text)
    return text


def full_index(files: dict[str, str], counts: dict[str, int]) -> str:
    lines = [
        "# Full text index",
        "",
        "Per-section concatenations of the catalogued docs, plus the Primer README. Generated by scripts/build_catalog.py. Do not edit by hand.",
        "",
        "primer.txt is the root README.md. The study guide in it is The System Design Primer by Donne Martin, CC BY 4.0. An attribution header is inside that file.",
        "",
        f"Size cap: {MAX_FULL} bytes per file. The generator never deletes or skips a bundle for being large. If a file would exceed the cap, the command exits non-zero and names the file to split.",
        "",
        "Enterprise stays one file, llms-full/enterprise.txt, while that rendered file is within the cap. "
        "If the rendered enterprise bundle would exceed the cap, the generator writes one file per enterprise subfolder (enterprise-<subfolder>.txt) and keeps docs that sit directly in enterprise/ in enterprise.txt. "
        "A file that still exceeds the cap is an error. Nothing is deleted to get under the cap.",
        "",
        "## Files",
        "",
    ]
    for name in index_order(files):
        count = counts[name]
        noun = "doc" if count == 1 else "docs"
        lines.append(f"- [llms-full/{name}](llms-full/{name}): {count} {noun}")
    lines.append("")
    return "\n".join(lines)


def index_order(files: dict[str, str]) -> list[str]:
    def key(name: str) -> tuple[int, str]:
        if name == "enterprise.txt":
            return (0, "")
        if name.startswith("enterprise-"):
            return (1, name)
        order = {
            "patterns.txt": 2,
            "templates.txt": 3,
            "pack.txt": 4,
            "primer.txt": 5,
        }
        return (order.get(name, 9), name)

    return sorted(files, key=key)


def counts_inner(docs: list[dict]) -> str:
    def prefixed(prefix: str) -> int:
        return sum(1 for doc in docs if doc["rel"].startswith(prefix))

    rows = (
        ("Enterprise docs", "enterprise/README.md", prefixed("enterprise/")),
        ("AI docs", "enterprise/ai/README.md", prefixed("enterprise/ai/")),
        (
            "Reference architectures",
            "enterprise/reference-architectures/README.md",
            sum(1 for doc in docs if doc["kind"] == "reference-architecture"),
        ),
        ("Pattern cards", "patterns/README.md", sum(1 for doc in docs if doc["kind"] == "pattern")),
        ("Templates", "templates/README.md", sum(1 for doc in docs if doc["kind"] == "template")),
        ("Skills", "pack/README.md", sum(1 for doc in docs if doc["kind"] == "skill")),
        ("Total catalogued docs", "", len(docs)),
    )
    lines = ["| Kind | Count |", "|---|---:|"]
    for name, href, count in rows:
        label = f"[{name}]({href})" if href else name
        lines.append(f"| {label} | {count} |")
    lines.append("")
    lines.append(
        "Enterprise docs count every catalogued file under `enterprise/`, including the AI docs and reference architectures listed on their own rows. Pattern cards omit `patterns/README.md`. Templates omit `templates/README.md`. Skills are the `SKILL.md` files."
    )
    return "\n".join(lines)


def rewrite_readme(text: str, inner: str) -> str:
    start = text.find(COUNTS_START)
    end = text.find(COUNTS_END)
    if start < 0 or end < 0 or end < start:
        err("README.md", "missing counts markers")
        return text
    if text.find(COUNTS_START, start + len(COUNTS_START)) != -1:
        err("README.md", "multiple counts:start markers")
        return text
    return (
        text[: start + len(COUNTS_START)]
        + "\n"
        + inner.strip("\n")
        + "\n"
        + text[end:]
    )


def build() -> tuple[dict[str, str], tuple[int, bool]]:
    parsed: list[dict] = []
    for path in iter_docs():
        doc = parse_doc(path)
        if doc is not None:
            parsed.append(doc)
    flush_errors()
    apply_skill_dates(parsed)
    catalog = catalog_object(parsed)
    outputs: dict[str, str] = {
        "catalog.json": dump_json(catalog),
        "llms.txt": render_llms(parsed),
    }
    flush_errors()
    enterprise, projection = render_enterprise(parsed)
    bundles = {}
    bundles.update(enterprise)
    bundles.update(render_simple(parsed, "patterns", "patterns.txt", "Pattern cards"))
    bundles.update(render_simple(parsed, "templates", "templates.txt", "Templates"))
    bundles.update(render_simple(parsed, "pack", "pack.txt", "Skills pack"))
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        err("README.md", "missing file")
        flush_errors()
    readme_text = rewrite_readme(
        readme_path.read_text(encoding="utf-8"),
        counts_inner(parsed),
    )
    primer = render_primer(readme_text)
    bundles["primer.txt"] = primer
    counts = {name: text.count("\n# Source: ") for name, text in bundles.items()}
    outputs["llms-full.txt"] = full_index(bundles, counts)
    for name, text in bundles.items():
        outputs[f"llms-full/{name}"] = text
    outputs["README.md"] = readme_text
    flush_errors()
    return outputs, projection


def stale_full_files(generated: dict[str, str]) -> list[str]:
    folder = ROOT / "llms-full"
    if not folder.exists():
        return []
    stale: list[str] = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel not in generated:
            stale.append(rel)
    return stale


def check(outputs: dict[str, str]) -> int:
    problems: list[str] = []
    for rel, text in sorted(outputs.items()):
        path = ROOT / rel
        data = text.encode("utf-8")
        if not path.exists():
            problems.append(f"{rel}: missing")
            continue
        if path.read_bytes() != data:
            problems.append(f"{rel}: differs")
    for rel in stale_full_files(outputs):
        problems.append(f"{rel}: stale, would not be generated")
    if problems:
        print(f"{len(problems)} drifted outputs")
        for line in problems:
            print(line)
        return 1
    print(f"ok ({len(outputs)} files)")
    return 0


def write_outputs(outputs: dict[str, str]) -> None:
    for rel, text in sorted(outputs.items()):
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        print(f"wrote {rel}")
    for rel in stale_full_files(outputs):
        (ROOT / rel).unlink()
        print(f"removed {rel}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare generated outputs to the working tree and do not write",
    )
    args = parser.parse_args()
    outputs, (current, split) = build()
    print(
        "enterprise bundle: "
        f"current={current} cap={MAX_FULL} split={'yes' if split else 'no'}"
    )
    if args.check:
        return check(outputs)
    write_outputs(outputs)
    return 0


if __name__ == "__main__":
    sys.exit(main())

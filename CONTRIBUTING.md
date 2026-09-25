# Contributing

Pull requests are welcome. GitHub Issues are intentionally turned off, so open a pull request instead of requesting a change. AI-assisted pull requests are welcome.

## Conventions

- One topic per file, roughly under 300 lines.
- New docs under `enterprise/`, `patterns/`, and `templates/` start with YAML frontmatter: `title`, `summary`, `tags`, `when_to_use`, `related`.
- Regenerate [catalog.json](catalog.json) with `python3 scripts/build_catalog.py`. That command also refreshes [llms-full.txt](llms-full.txt) when the concatenation stays under the size limit. Update [llms.txt](llms.txt) when the short index should list the new page.
- Cite external sources by link. State a license only when it is already verified in [pack/corpora/INDEX.md](pack/corpora/INDEX.md). Do not copy non-redistributable text.
- Do not rewrite original Primer text, translations, or `solutions/`. Add a clearly marked `Enterprise update (fork)` callout instead.
- Run `python3 scripts/check_links.py` before opening a pull request.

Agent workflow and which files to load: [AGENTS.md](AGENTS.md).

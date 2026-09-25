# Contributing

Pull requests are welcome. GitHub Issues are intentionally turned off, so open a pull request instead of requesting a change. AI-assisted pull requests are welcome.

## Conventions

- One topic per file, roughly under 300 lines. `scripts/build_catalog.py` rejects a catalogued doc over 300 lines.
- New docs under `enterprise/`, `patterns/`, `templates/`, and `pack/` (except `SKILL.md`) start with YAML frontmatter: `title`, `summary`, `tags`, `when_to_use`, `related`, and `last_reviewed` as `YYYY-MM-DD`. Update `last_reviewed` when you change the page. `SKILL.md` keeps only `name` and `description`, and the description starts with "Use this when".
- Install the catalog tool with `pip install -r scripts/requirements.txt`. Regenerate [catalog.json](catalog.json), [llms.txt](llms.txt), [llms-full.txt](llms-full.txt), `llms-full/`, and the counts table in [README.md](README.md) with `python3 scripts/build_catalog.py`. `python3 scripts/build_catalog.py --check` exits non-zero if any of those drift, and it does not write. `catalog.json` is schema version 2: `schema_version`, `source_hash`, `counts`, and `entries`.
- The full-text files are capped at 1,000,000 bytes. The command fails instead of deleting a file that is too large. Enterprise text stays in `llms-full/enterprise.txt` while that rendered file is within the cap. If the rendered bundle would exceed the cap, the generator writes `llms-full/enterprise-<subfolder>.txt` and leaves files that sit directly in `enterprise/` in `enterprise.txt`. A file that is still over the cap is an error. Nothing is deleted to get under the cap. `--check` also fails if `llms-full/` contains a file this run would not generate.
- Cite external sources by link. State a license only when it is already verified in [pack/corpora/INDEX.md](pack/corpora/INDEX.md). Do not copy non-redistributable text.
- Do not rewrite original Primer text, translations, or `solutions/`. Add a clearly marked `Enterprise update (fork)` callout instead.
- Run `python3 scripts/check_links.py` before opening a pull request. `python3 scripts/check_external_links.py` reports remote URL failures and exits 0 unless you pass `--strict`. The weekly workflow runs it without `--strict`.

Agent workflow and which files to load: [AGENTS.md](AGENTS.md).

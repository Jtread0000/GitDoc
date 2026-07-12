# CLAUDE.md

This repo's operating instructions live in [`AGENTS.md`](AGENTS.md) — read it first.
It covers onboarding a new writer, editing the manuscript as Word tracked changes,
and the versioning/worklog conventions.

Claude Code auto-discovers two skills under `.claude/skills/`:
- **`gitdoc-setup`** — run it on a fresh clone (or say "set up my document") to
  onboard the writer and bootstrap their first `.docx`.
- **`tracked-doc-sync`** — the tracked-changes editing API for day-to-day writing.

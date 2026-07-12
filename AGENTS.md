# AGENTS.md — instructions for the AI working in this repo

You are the writing collaborator for a **GitDoc** manuscript workspace. A person
cloned this template to draft long-form writing (a paper, dissertation, chapter, or
article) where **every edit you make is a real Word tracked change** they can
Accept or Reject, the document lives in **git**, and it optionally syncs to a
storage folder they open in Word.

This file is your standing brief. Read `docs/tracked-changes.md` and
`docs/editing-protocol.md` before you edit a document. Claude Code auto-discovers two
skills in `.claude/skills/`: **`gitdoc-setup`** (run it on a fresh clone to onboard
the writer) and **`tracked-doc-sync`** (the tracked-changes editing API).

## First run: onboard the writer

If there is **no manuscript `.docx`** in the repo root yet (only the template's
example files), this is a fresh adoption. Don't guess what they're writing — help
them set it up:

1. **Have a short conversation about the work.** Ask, in plain language:
   - What are they writing? (paper, dissertation chapter, proposal, article…)
   - What's the topic / working title, in one line?
   - A rough structure, if they have one (sections/headings) — or offer a sensible
     default for that document type and let them adjust.
   - Their name (or preferred author label) for the document.
   - Where they want it synced, if at all — the storage folder path (or "git only
     for now"). See `docs/setup-dropbox.md`; storage secrets are theirs to add.
   A writer who'd rather just talk through goals than answer a checklist is fine —
   draw the same details out of the conversation.
2. **Bootstrap the document.** Use `new_docx([...])` (see `docs/tracked-changes.md`)
   to create `<their-title>.docx` in the repo root with their headings and a
   `[[WRITE: …]]` marker under anything to be filled later. This first skeleton can
   be a plain document (it's the `0.1.0` baseline); everything *after* it is tracked.
3. **Wire the basics.**
   - Set `SYNC_FILES` (repo variable) or rely on the default (`*.docx` in root).
   - If they chose storage sync, set `DROPBOX_DEST_DIR` to *their* folder and point
     them to `docs/setup-dropbox.md` for the three secrets. Never hard-code a
     personal path into committed files — it goes in the repo variable.
   - Seed `CHANGELOG.md` with their `0.1.0`, add the first `LOG.md` entry, and fill
     the `## Current placeholders` table in `PLACEHOLDERS.md`.
4. **Commit** the bootstrapped doc and settings with a clear message.

If a manuscript `.docx` already exists, skip onboarding and just help them write.

## Placeholder markers

The document carries its own to-do list as bracket tags (full spec:
`PLACEHOLDERS.md`). Author them as you draft and keep the `## Current placeholders`
table current — it's **agent-curated**; you have the doc in git, so don't lean on a
generator. **Blockers** (`WRITE/CITE/VERIFY/Q/REF`) must be zero before a share;
**author-only** (`NOTE/CUT?`) are private, stripped before sharing. Gate every share
with the lint: `python3 scripts/check_tags.py` (nonzero if a blocker survives
Accept-All).

## Author-writes mode (venues with AI-authorship rules)

Some venues restrict AI-**written** prose (ISACA and many journals). Ask during
onboarding whether the writer's target has such a rule. If it does, run in
**author-writes mode**:

- The `0.1.0` baseline is a **skeleton + markers, not AI-written prose** — section
  headings with a `[[WRITE: …]]` under each for the writer to draft themselves.
- Carry the settled arguments, evidence, and structure you'd otherwise draft as
  `[[NOTE: …]]` **author-only guidance** (stripped before sharing) and
  `[[CITE: …]]` / `[[VERIFY: …]]` on claims — so the writer has the material at their
  fingertips but the words are theirs.
- You scaffold, organize, source, and fact-check; **you do not write the prose**. The
  document stays the author's own creation, which keeps it clean under the rule.

Without such a rule, draft prose normally (as tracked `[[WRITE:]]` fills the writer
reviews). Either way, every change you make is still a tracked change.

## Editing: every change is a tracked change

Never rewrite the document opaquely. Use `scripts/docx_tracked_changes.py`:

- `TrackedEditor(path, author="…", date="<ISO date>")` with `.replace_text(old, new)`
  and `.insert_after(anchor, text)`. Anchors match on **visible text** and must be
  unique — lengthen them until they resolve to exactly one spot.
- **Group one decision under a single `author` string** so the writer accepts or
  rejects it as a unit. (Their construct-removal across five paragraphs should be one
  author group, not five.)
- **Verify before you ship, every time:** assert `accept_all(path)` reads clean and
  `reject_all(path)` restores the original. Do not skip this.
- Commit to git with a clear message; if sync is on, the workflow mirrors it.

## Decisions, versioning, and the suggestion engine

- A **decision** is one coherent, doc-wide edit (add/remove one thing). Carry all its
  tracked changes under a single **named** `author` label (e.g. `Claude —
  trim-to-pitch`) and list it under `CHANGELOG.md` **[Unreleased]**.
- A **version** is a share-point the **writer declares**, not a per-edit counter
  (`MAJOR.MINOR.PATCH`; `0.1.0` baseline, `1.0.0` first final draft).
- **Suggestion engine:** watch the [Unreleased] decisions and *proactively suggest
  cutting a version* when they form a coherent, right-sized unit (~2–4 related
  decisions, or one complete decision worth sharing) so versions stay small. On a
  bump: run `check_tags.py`, roll [Unreleased] into a dated `CHANGELOG.md` entry with
  a **commit link per bullet** (the recovery index for removed text), tag the
  release, and note it in `LOG.md`. You *suggest*; the writer *declares*. Full model:
  `docs/workflow.md`.

## One writer at a time

A `.docx` is binary and can't be merged. If the writer says "hands off," stop
editing, let them work in Word, and **capture their storage-side edits into git
before you touch the file again** (`scripts/dropbox_sync.py` does this
automatically; see `docs/editing-protocol.md`). Never overwrite a change made in
storage.

## Keep the paper trail

- `LOG.md` — reverse-dated worklog: one short entry per working session or notable
  touch.
- `CHANGELOG.md` — one entry per declared version/share-point; decisions accumulate
  under [Unreleased] between them.
- `PLACEHOLDERS.md` — the live marker tracker; update it as you fill markers.
- Keep the manuscript lean and the tone modest; be confident about the substance,
  not showy about it.

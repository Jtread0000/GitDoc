---
name: tracked-doc-sync
description: >-
  Author and revise Word (.docx) documents as an LLM using real Word tracked
  changes, version-controlled in git and two-way synced to Dropbox with
  conflict capture. Use when a user wants a document (memo, proposal, report,
  chapter) drafted or edited so every change is a reviewable Word revision they
  can Accept/Reject, and kept in sync with a Dropbox folder they open in Word.
  Triggers: "tracked changes", "edit my .docx", "draft a memo/proposal I can
  review in Word", "keep it synced to Dropbox", "set up the doc workflow".
---

# tracked-doc-sync

Reusable workflow for LLM-driven document authoring where **every edit is a real
Word tracked change** (Accept/Reject-able), the document lives in **git**, and it
**syncs both ways to Dropbox** without ever clobbering a human's edits.

## When to use
- The user wants a `.docx` drafted/edited with changes they can review in Word.
- They want it kept in a Dropbox folder they open on desktop/mobile.
- They want version history + the ability to accept/reject the LLM's edits.

## Files this skill provides
| File | Role |
| --- | --- |
| `scripts/docx_tracked_changes.py` | Create a `.docx`; apply `<w:ins>`/`<w:del>` tracked changes matched on visible text; simulate Accept-All / Reject-All to verify. |
| `scripts/dropbox_sync.py` | Sync files git↔Dropbox with conflict **capture** (never overwrites a Dropbox-side edit). |
| `.github/workflows/sync-to-dropbox.yml` | Runs the sync on push (binary-safe, via the Dropbox HTTP API). |
| `docs/setup-dropbox.md` | One-time Dropbox app + offline-refresh-token + secrets setup. |
| `docs/tracked-changes.md` | The OOXML tracked-changes concepts + the edit/verify loop. |
| `docs/editing-protocol.md` | One-writer-at-a-time rule that prevents Dropbox "conflicted copy" files. |
| `docs/workflow.md` | The authoring model: chat-vs-doc, decisions, versioning, the suggestion engine. |
| `scripts/check_tags.py` | Pre-share lint: fails if any blocker marker survives Accept-All. |
| `PLACEHOLDERS.md` | The marker vocabulary + the live, agent-curated placeholder tracker. |

## How to drive it (agent workflow)
1. **Bootstrap or import the doc.** New doc: `new_docx([...paragraphs...], "doc.docx")`
   (author placeholder markers for anything to fill later). Or start from a
   Word/Docs export so it carries real styles.
2. **Edit as tracked changes.** Use `TrackedEditor(path, author="…", date="…")`
   with `.replace_text(old, new)` (fills placeholders / swaps phrases) and
   `.insert_after(anchor, text)` (adds sentences). Group one **decision** under a
   single `author` string so it accepts/rejects as a group (see below).
3. **Verify before shipping.** Assert `accept_all(path)` reads clean and
   `reject_all(path)` restores the original. Never skip this.
4. **Keep the paper trail current.** Update the `PLACEHOLDERS.md` tracker as you fill
   markers, add the decision under `CHANGELOG.md` **[Unreleased]**, and log the touch
   in `LOG.md`.
5. **Commit to git**, then let the sync push it to Dropbox. If the user is editing
   in Word, follow `docs/editing-protocol.md` (one writer at a time; capture their
   Dropbox edits into git before you write).

See `docs/tracked-changes.md` for the exact API and rules. Anchors must be unique
(each edit matches exactly one spot or it errors — lengthen the anchor).

## Placeholder markers
The document carries its own to-do list as bracket tags (full spec:
`PLACEHOLDERS.md`). **Blockers** — `WRITE`, `CITE`, `VERIFY`, `Q`, `REF` — must be
zero before a shareable version. **Author-only** — `NOTE`, `CUT?` — are private;
strip them before sharing. Keep the `## Current placeholders` table in
`PLACEHOLDERS.md` up to date by hand (you have the doc in git — don't rely on a
generator). Before any share, run the lint and clear every blocker:
```bash
python3 scripts/check_tags.py            # nonzero exit if any blocker survives Accept-All
```

## Decisions, versioning, and the suggestion engine
- A **decision** is one coherent, doc-wide edit (add/remove one thing). Carry all its
  tracked changes under a single, named `author` label (e.g. `Claude — trim-to-pitch`)
  and list it under `CHANGELOG.md` **[Unreleased]**.
- A **version** is a share-point the **user declares** (`MAJOR.MINOR.PATCH`; `0.1.0`
  baseline; `1.0.0` first final draft) — never bump it per edit.
- **Suggestion engine:** watch the [Unreleased] list and *proactively suggest cutting
  a version* when the pending decisions form a coherent, right-sized unit (rule of
  thumb ~2–4 related decisions, or one complete decision worth sharing alone) — so
  versions stay small and legible. On a bump: run `check_tags.py`, roll the
  [Unreleased] decisions into a dated `CHANGELOG.md` entry with a **commit link per
  bullet** (the recovery index for removed text), tag the release, and note it in
  `LOG.md`. You *suggest*; the user *declares*. See `docs/workflow.md`.

## Setup checklist (once per project)
- [ ] Copy this repo's `scripts/`, `.github/workflows/`, and `docs/` into the project.
- [ ] `pip install -r requirements.txt` (python-docx; pyyaml only if you use the DB add-on).
- [ ] Follow `docs/setup-dropbox.md`: create the Dropbox app, get an **offline**
      refresh token, add the 3 secrets + `DROPBOX_DEST_DIR` variable.
- [ ] Put the target Dropbox folder in `DROPBOX_DEST_DIR` (create a new subfolder
      for each project).

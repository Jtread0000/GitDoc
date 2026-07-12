---
name: gitdoc-setup
description: >-
  Set up a new manuscript in a freshly cloned GitDoc repo: interview the writer
  about what they're writing, bootstrap their first Word .docx (tracked-changes
  ready) as the 0.1.0 baseline, seed CHANGELOG/LOG, and wire the basic settings.
  Use on first run of a GitDoc clone, or when the user says "set up my document",
  "start my paper/dissertation/chapter", "onboard me", "get me going". If a
  manuscript .docx already exists, skip this and just help them write.
---

# gitdoc-setup

First-run onboarding for a GitDoc manuscript workspace. Run this when the repo has
no manuscript `.docx` yet (only the template's example files). It turns an empty
clone into a document the writer can start editing as tracked changes.

Read [`AGENTS.md`](../../../AGENTS.md) and [`docs/tracked-changes.md`](../../../docs/tracked-changes.md)
for the full conventions; this skill is the setup procedure.

## Procedure

1. **Interview the writer — one short round, not a form.** Draw these out (they may
   prefer to just talk through their goals; pull the details from that):
   - What are they writing? (paper, dissertation chapter, proposal, article…)
   - Working title and one-line topic.
   - A rough structure (sections) — or propose a sensible default for the document
     type and let them adjust.
   - The author label to attach to tracked changes.
   - Storage: git only for now, or sync to a folder they open in Word? (Secrets are
     theirs to add per `docs/setup-dropbox.md`; you only set the folder.)

2. **Confirm the plan** back in a few lines before creating anything.

3. **Bootstrap the document.** With `python-docx` installed
   (`pip install -r requirements.txt`), create `<title>.docx` in the repo root:
   ```python
   import sys; sys.path.insert(0, "scripts")
   from docx_tracked_changes import new_docx
   new_docx([
       "<Title>",
       "<Section heading>",
       "[[WRITE: what goes here]]",
       # …one string per paragraph/heading from their structure
   ], "<title>.docx")
   ```
   Use the placeholder vocabulary for markers — `[[WRITE: …]]` for content to draft,
   and `[[CITE: …]]` / `[[VERIFY: …]]` / `[[Q: …]]` where relevant (full set:
   `PLACEHOLDERS.md`). This first skeleton is the `0.1.0` baseline (a plain doc).
   **Everything after it is a tracked change** — see the `tracked-doc-sync` skill.

4. **Wire the basics.**
   - Seed `CHANGELOG.md` at `0.1.0` and add the first `LOG.md` entry (reverse-dated).
   - Fill in the `## Current placeholders` table in `PLACEHOLDERS.md` for the new
     doc (list each marker, its location, and OPEN status); keep it current as you
     fill markers. It's agent-curated — don't rely on a generator.
   - If syncing, tell them the `DROPBOX_DEST_DIR` repo-variable value to set (a **new
     subfolder per project**) and point to `docs/setup-dropbox.md`. Never hard-code a
     personal storage path into committed files.
   - Default `SYNC_FILES` (every `*.docx` in root) is usually fine.

5. **Commit** the new `.docx` and settings with a clear message. If sync is on, the
   push mirrors it to storage.

## After setup

Hand off to normal writing: every edit is a tracked change grouped by author, a
version is a share-point the writer declares (not a per-edit bump), and it's one
writer at a time on the binary `.docx`. See `AGENTS.md` and
`docs/editing-protocol.md`.

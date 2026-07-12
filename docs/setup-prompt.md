# Setup prompt — start a new chat with the repo attached

Use this when you open a **fresh chat thread** with your GitDoc repo attached (a
GitHub connector, or the files uploaded) and want the AI to *lead* the setup — read
the repo, ask you a few things, then stand up your document. It's the hands-off
sibling of [`kickoff-template.md`](kickoff-template.md): there you fill in the
blanks; here you let the AI draw the details out and drive.

> **Using Claude Code?** You don't need this prompt — just run **`/gitdoc-setup`**
> in the cloned repo and the setup skill drives the same flow. The prompt below is
> for any other chat/AI where the repo is attached.

Copy the block below and paste it as your first message.

---

```text
This chat has my GitDoc repository attached. GitDoc is a template for writing a
long-form document (paper, dissertation, chapter, article) where every AI edit is a
reviewable Word tracked change, the file lives in git, and it optionally syncs to
cloud storage I open in Word.

Please get me set up. Work in this order:

1. Read AGENTS.md, docs/getting-started.md, and docs/tracked-changes.md so you
   follow this repo's conventions (tracked changes for every edit; a "version" is a
   share-point I declare, not a per-edit bump; one writer at a time).

2. Interview me briefly — one short round of questions, not a form:
   - What am I writing, and a one-line topic / working title?
   - A rough structure (sections), or propose a sensible default for this document
     type and let me adjust.
   - The author name to attach to tracked changes.
   - Storage: git only for now, or sync to a folder I open in Word? (If syncing,
     I'll add the secrets from docs/setup-dropbox.md; you just set the folder.)
   I'm happy to just talk through my goals instead — pull the details from that.

3. Confirm the plan back to me in a few lines before creating anything.

4. Then set it up:
   - Create <my-title>.docx in the repo root from my structure, with [[WRITE: …]]
     markers under anything to fill in later. This first skeleton is the 0.1.0
     baseline; everything after it is a tracked change.
   - Seed CHANGELOG.md at 0.1.0 and add the first LOG.md entry.
   - If I chose sync, note the DROPBOX_DEST_DIR value I should set (don't hard-code a
     personal path into committed files) and point me to docs/setup-dropbox.md.
   - Commit with a clear message.

Capability check: if you can run code and commit in this environment, do steps 2–4
directly. If you're a read-only chat that can see my files but not run them, do the
interview and the plan, then hand me back exactly what I need to finish — the
paragraph list for new_docx([...]), the CHANGELOG/LOG starter text, and the git
commands — so I (or a coding agent) can run it. Either way, start with step 1 now.
```

---

After setup, you're writing: ask for edits in plain language and review them in Word.
See [`getting-started.md`](getting-started.md) for the day-to-day loop.

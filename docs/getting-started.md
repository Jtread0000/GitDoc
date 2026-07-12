# Getting started

GitDoc is a template you copy into your own repo and drive with the AI of your
choice. This walks you from an empty repo to a first draft you can review in Word.
It takes about five minutes; you never touch the tracked-changes plumbing yourself.

## 1. Make it your repo

- On GitHub, open the GitDoc repo and click **Use this template → Create a new
  repository** (or **Fork**, or just clone and re-point the remote). Name the new
  repo for *your* manuscript.
- Keep it **private** if the manuscript is unpublished; the workflow and scripts
  don't care either way.

## 2. Clone it and install the one dependency

```bash
git clone https://github.com/<you>/<your-repo>.git
cd <your-repo>
pip install -r requirements.txt   # python-docx, used only to create the first .docx
```

Everything else (editing tracked changes, verifying them) uses the Python standard
library.

## 3. Open your AI in the repo and let it onboard you

Open the folder with a coding agent (Claude Code, or any agent that reads
`AGENTS.md`). Tell it you just cloned GitDoc and want to start a document. It will:

- ask what you're writing, the working title, a rough structure, and your author
  name — **or** just talk through your goals and pull those details out of the
  conversation;
- create `<your-title>.docx` in the repo root, with `[[WRITE: …]]` markers wherever
  you'll fill things in later;
- seed `CHANGELOG.md` at `0.1.0` and start `LOG.md`;
- commit it.

Ready-made first prompts if you'd rather not wing it:
- [`setup-prompt.md`](setup-prompt.md) — let the AI lead: it reads the repo,
  interviews you, and sets things up. Best when the repo is attached to a fresh chat.
- [`kickoff-template.md`](kickoff-template.md) — you fill in the blanks and hand over
  a complete brief.
- [`migrate-prompt.md`](migrate-prompt.md) — already been working the paper out in a
  chat? Formalize that discussion into a GitDoc document, in place.

## 4. Write by asking for tracked changes

From here, ask for edits in plain language: *"draft the introduction,"* *"tighten
the third paragraph,"* *"remove every mention of the X construct."* Each edit comes
back as a real Word revision with an author and date. Open the `.docx` in Word, set
**Review → All Markup** to see every insertion and deletion inline (Simple/No Markup
hides them), then use **Review → Accept / Reject** — edits that belong to one decision
are grouped under one author, so you accept or reject them together.

The agent verifies every change before committing (it simulates Word's Accept-All
and Reject-All), so what you see in Word matches what it intended.

As you draft, unfinished spots are held by **placeholder markers** — `[[WRITE: …]]`
for content to fill, plus `CITE / VERIFY / REF / NOTE / Q / CUT?`. The agent keeps a
live [`PLACEHOLDERS.md`](../PLACEHOLDERS.md) tracker so you always know what's still
open. The *blockers* among them must be cleared before you share (below).

## 5. (Optional) Sync to storage you open in Word

If you want the live `.docx` on your desktop or phone, turn on storage sync:

- Follow [`setup-dropbox.md`](setup-dropbox.md) once to create a storage app, get an
  offline refresh token, and add the three secrets.
- Set the `DROPBOX_DEST_DIR` repo variable to your own folder (use a **new subfolder
  per project**).

Skip this entirely and nothing breaks — your document is still fully version-
controlled in git. The workflow stays inert until the secrets exist.

## 6. Cut versions when a draft is ready to share

A version is a **share-point you declare**, not a bump per edit. Between shares, work
accumulates as named **decisions** under `CHANGELOG.md` [Unreleased]; the agent
*suggests* cutting a version when they add up to a coherent, right-sized unit, so
versions stay small. When you agree, it rolls the decisions into a dated
`CHANGELOG.md` entry (each bullet linking to its commit — your recovery index), tags
the release, and notes it in `LOG.md`.

Before you share, clear the blocker markers:

```bash
python3 scripts/check_tags.py    # nonzero exit if any WRITE/CITE/VERIFY/Q/REF is still open
```

The full authoring model — chat-vs-doc, decisions, the suggestion engine — is in
[`workflow.md`](workflow.md).

## Editing etiquette (one writer at a time)

A `.docx` is binary and can't be auto-merged. When *you* want to edit in Word, tell
the agent "hands off," make your edits, wait for storage to finish syncing, then
hand back — it captures your version into git before making further changes. Details
in [`editing-protocol.md`](editing-protocol.md).

## Where to look next

- [`workflow.md`](workflow.md) — the authoring model: decisions, versioning, the
  suggestion engine.
- [`../PLACEHOLDERS.md`](../PLACEHOLDERS.md) — the marker vocabulary and live tracker.
- [`tracked-changes.md`](tracked-changes.md) — how the tracked-changes machinery
  works and its rules.
- [`editing-protocol.md`](editing-protocol.md) — avoiding "conflicted copy" files.
- [`setup-dropbox.md`](setup-dropbox.md) — one-time storage setup.
- [`../AGENTS.md`](../AGENTS.md) — what your AI is following on your behalf.

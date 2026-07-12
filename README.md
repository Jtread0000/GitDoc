# GitDoc | Word Tracked Change Manager

**A boilerplate for writing long-form documents — papers, dissertations, articles —
with an AI collaborator whose every edit is a reviewable Word tracked change,
version-controlled in git, released like software, and synced to storage you open
in Word anywhere.**

Clone this into your own repo, open the AI of your choice, tell it what you're
writing (or just talk through your goals), and it sets up your first `.docx` and
the basic settings. From then on the AI drafts and revises your manuscript as
**Word revisions you Accept or Reject** — never an opaque rewrite — while git keeps
the history and named versions, and an optional sync mirrors the file to a storage
folder you open in Word on your desktop or phone.

## Who this is for

Anyone doing long-form writing who wants an **external, permanent AI thought-organizer**
that helps with structure, formatting, and references without taking the pen out of
your hand:

- A PhD student drafting a dissertation.
- A researcher writing a paper with many cross-references and a moving argument.
- Anyone maintaining a manuscript they want to review, version, and keep durable.

## Why it works

- **Reviewable, not opaque.** Changes are real `<w:ins>`/`<w:del>` Word revisions
  carrying an author and date, so you Accept/Reject them in Word like any human
  editor's. Edits that belong to one decision share an author string, so a whole
  change accepts or rejects as a group.
- **Versioned like software.** The document lives in git. You declare *share-points*
  as releases (`0.1.0`, `0.2.0`, …) — a version is a milestone you choose to send
  out, not a bump per keystroke.
- **Durable.** Git history plus a plain-text worklog beats a lone binary lost in a
  cloud folder.
- **Openable anywhere.** An optional, binary-safe sync mirrors your `.docx` to a
  storage folder (Dropbox reference implementation included) you open in Word on
  desktop or mobile. If you edit it there, your change is *captured into git*, never
  overwritten.

### What that feels like in practice

You decide to cut a construct from your paper — but it's referenced across four
paragraphs on three pages. One instruction to your AI, and every mention is removed
as tracked changes you can review. Accept them together, and the manuscript moves
from `0.1.0` to `0.2.0` as **one** decision instead of a dozen scattered edits.

## How it fits together

- **Placeholder markers** let the document carry its own to-do list — `[[WRITE: …]]`
  for content to draft, plus `CITE / VERIFY / REF / NOTE / Q / CUT?` for sources,
  facts, references, private notes, questions, and deletion candidates. The
  *blockers* (`WRITE/CITE/VERIFY/Q/REF`) must be cleared before you share; a one-line
  lint (`scripts/check_tags.py`) enforces it. Full spec + live tracker:
  [`PLACEHOLDERS.md`](PLACEHOLDERS.md).
- **Decisions** are the unit of work: one coherent, document-wide edit, grouped under
  a single author label so it accepts/rejects as a group in Word.
- **Versions** are share-points *you* declare (`0.1.0 → 0.2.0`); the AI suggests when
  to cut one so they stay small, and rolls the decisions into a `CHANGELOG.md` entry
  whose commit links double as your recovery index. See
  [`docs/workflow.md`](docs/workflow.md).

## Quick Start

> Full walkthrough: [`docs/getting-started.md`](docs/getting-started.md).

1. **Make it your repo.** Click **Use this template** on GitHub (or fork/clone),
   then create a repo for *your* manuscript.
2. **Clone and install.**
   ```bash
   git clone https://github.com/<you>/<your-repo>.git && cd <your-repo>
   pip install -r requirements.txt
   ```
3. **Open your AI in the repo** (Claude Code, or any coding agent). It reads
   [`AGENTS.md`](AGENTS.md) and offers to onboard you. In Claude Code, just run
   **`/gitdoc-setup`** — the setup skill drives the whole thing.
4. **Tell it what you're writing** — the doc type, the topic, a rough structure — or
   just talk through your goals. It bootstraps your `.docx` (with `[[WRITE: …]]`
   markers for anything to fill later) at version `0.1.0`.
5. **Draft as tracked changes.** Ask for edits; review them in Word; Accept/Reject.
   Commit as you go.
6. **(Optional) Turn on storage sync.** Follow
   [`docs/setup-dropbox.md`](docs/setup-dropbox.md) to mirror the file to a folder
   you open in Word. Skip this and everything still works in git.
7. **Cut versions.** When a draft is a share-point, tag a release (`0.2.0`) and note
   it in [`CHANGELOG.md`](CHANGELOG.md).

Two ready-made first prompts, depending on how you like to work:
- [`docs/setup-prompt.md`](docs/setup-prompt.md) — paste into a fresh chat with the
  repo attached and let the AI **lead**: read the repo, interview you, set it up.
- [`docs/kickoff-template.md`](docs/kickoff-template.md) — you **fill in the blanks**
  up front and hand the agent a complete brief.

## What's inside

| Path | Role |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Standing instructions any AI reads on clone: onboarding + editing + versioning rules. |
| [`PLACEHOLDERS.md`](PLACEHOLDERS.md) | The marker vocabulary (`WRITE/CITE/VERIFY/REF/NOTE/Q/CUT?`) + the live placeholder tracker. |
| `scripts/docx_tracked_changes.py` | Create a `.docx`; apply tracked changes matched on visible text; simulate Accept-All / Reject-All to verify. |
| `scripts/check_tags.py` | Pre-share lint: fails if any blocker marker still survives Accept-All. |
| `scripts/dropbox_sync.py` | git↔storage sync with conflict **capture** (never clobbers a storage-side edit). |
| `.github/workflows/sync-to-dropbox.yml` | Runs the sync on push (binary-safe, via the storage HTTP API). |
| `docs/getting-started.md` | The human quick-start walkthrough. |
| `docs/workflow.md` | The authoring model: chat-vs-doc, decisions, versioning, the suggestion engine. |
| `docs/setup-prompt.md` | Copy-paste prompt: let the AI lead setup in a fresh chat with the repo attached. |
| `docs/kickoff-template.md` | Copy-paste first prompt where you fill in the details up front. |
| `docs/tracked-changes.md` | The tracked-changes API and rules. |
| `docs/editing-protocol.md` | One-writer-at-a-time rule that prevents "conflicted copy" files. |
| `docs/setup-dropbox.md` | One-time storage app + offline token + secrets setup. |
| `.claude/skills/gitdoc-setup/` | Claude Code skill: onboard a new writer and bootstrap their doc (run `/gitdoc-setup`). |
| `.claude/skills/tracked-doc-sync/` | Claude Code skill: the tracked-changes editing API. |
| `examples/quickstart.py` | Runnable end-to-end demo of the tracked-changes loop. |

## A note on storage

Your document is version-controlled in **git** no matter what — storage sync is an
optional convenience so you can open the live `.docx` in Word. The included
implementation targets **Dropbox** (a self-contained script that speaks the Dropbox
HTTP API directly, so it handles binary `.docx` files). Prefer another provider? The
sync is one small script (`scripts/dropbox_sync.py`); adapt its upload/download calls
to your provider's API and keep the rest.

## License

MIT — see [LICENSE](LICENSE). Fork it, adapt it, share it with your cohort.

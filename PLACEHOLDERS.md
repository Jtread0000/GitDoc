# Placeholders

Placeholder markers let the document carry its own to-do list. Each marker is a
bracket tag naming the content it stands in for, so nothing ships with a hidden
hole. Your AI keeps this file current as it works; you never have to run anything.

Every marker is:
- **Greppable** — search `[[` to find every open spot at once.
- **Tracked-change safe** — a marker is filled by *deleting* it and *inserting* the
  real text, both as Word revisions. On **Accept-All** every marker clears; on
  **Reject-All** they return. Nothing is silently lost.
- **Optionally highlighted** — highlight them yellow in Word if you like open spots
  to jump out.

## Tag types

| Tag | What it's for | Example |
| --- | --- | --- |
| `[[WRITE: … ]]` | **Draft content here.** The primary tag. | `[[WRITE: the executive-abstract hook]]` |
| `[[CITE: … ]]` | A claim that **needs a citation** — find/attach a source. | `[[CITE: only 14% permit autonomous remediation]]` |
| `[[VERIFY: … ]]` | A fact / number / quote to **confirm against its source** before sharing. | `[[VERIFY: contractors face 3× the loss]]` |
| `[[REF: id ]]` | Pointer to a **knowledge-base / lit record** (e.g. a `lit.yaml` id, or a personal-canon link). | `[[REF: nyilasy-aihr]]` |
| `[[NOTE: … ]]` | A **private author note** — reminder to self; strip before sharing. | `[[NOTE: tighten once the title lands]]` |
| `[[Q: … ]]` | An **open question** for the PI / committee / reviewer. | `[[Q: is 50–150 enough for the movement analysis?]]` |
| `[[CUT?: … ]]` | A **candidate for deletion** — "should this stay?" | `[[CUT?: the ISACA paragraph if space is tight]]` |

**Blockers vs. author-only.** `WRITE`, `CITE`, `VERIFY`, `Q`, `REF` are **blockers**
— a shareable draft should have **none open**. `NOTE` and `CUT?` are **author-only**
— strip them before sharing. The lint below enforces exactly this line.

## Current placeholders

_Your AI updates the table below as it fills markers. Status: **OPEN** = still to
resolve (survives Accept-All); **FILLED** = the real text is in place as a pending
tracked change (clears on Accept-All, recoverable via Reject-All or git)._

<!-- Once your document exists, this becomes a live table, e.g.:

## Current placeholders — `my-paper.docx`

| Marker | Location | Status |
| --- | --- | --- |
| `[[WRITE: the delegation-threshold literature]]` | Background ¶ | ✅ FILLED — Malatji 2025; South et al. 2025 |
| `[[CITE: only 14% permit autonomous remediation]]` | Background ¶1 | ⬜ OPEN |

**Open blockers: 1.**
-->

_No document yet — run `/gitdoc-setup` (or see [`docs/getting-started.md`](docs/getting-started.md))
and this fills in._

## Pre-share check

Before you cut a shareable version, confirm no blocker markers survive Accept-All:

```bash
python3 scripts/check_tags.py            # every *.docx in the repo root
python3 scripts/check_tags.py --quiet    # only problems + the verdict
```

It exits nonzero if any **blocker** (`WRITE/CITE/VERIFY/Q/REF`) is still open, and
lists any **author-only** (`NOTE/CUT?`) tags to strip. Wire it into CI to gate
shares automatically (see [`docs/workflow.md`](docs/workflow.md)).

## Adding your own tags

The set is a convention, not a hard schema. If you add one (say `[[TODO: …]]`), tell
your AI what it means and document it here. `check_tags.py` treats any tag outside
the blocker list as author-only unless you add it to `BLOCKERS` in the script.

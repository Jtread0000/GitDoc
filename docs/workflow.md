# How you write with GitDoc

GitDoc splits writing into two surfaces that stay out of each other's way:

- **The chat is where you think.** You talk through the outline, the argument, what
  to cut, what's missing — in whatever order your head works. No formatting, no
  hunting for every place a change ripples to.
- **The document is where decisions land.** When you ask for something, the AI makes
  the change in the `.docx` as **Word tracked changes** — insertions and deletions
  with an author and date. You keep the pen: open it in Word and **Accept**,
  **Reject**, or rewrite. Nothing changes silently.

That separation is the whole point. You get an AI that helps with structure,
formatting, references, and threading a change through many paragraphs — without it
quietly rewriting your voice. Every edit is visible and reversible.

## The loop

1. **Talk.** Describe the change: *"draft the intro,"* *"tighten paragraph three,"*
   *"remove every mention of the delegation construct,"* *"find a source for the 14%
   claim."*
2. **The AI edits as tracked changes.** A change that spans four paragraphs on three
   pages comes back as one reviewable set, not a mystery rewrite. Before committing,
   the AI verifies it (Accept-All reads clean, Reject-All restores the original).
3. **You review in Word.** Accept, reject, or say "redo it differently." Edits that
   belong to one decision share an author label, so **Review → Show Markup →
   Specific People** lets you accept or reject a whole decision as a group.
4. **Commit.** Git keeps the history; if sync is on, the file lands in your storage.

## Decisions: the unit between versions

Between shared versions, work accumulates as **decisions** — a *decision* is one
coherent, document-wide edit that adds or removes a single thing (a construct, a
section, a citation pass). The AI groups all the tracked changes for a decision
under **one author label** (e.g. `Claude — trim-to-pitch`), so the decision accepts
or rejects as a unit in Word, and lists it under **[Unreleased]** in
[`CHANGELOG.md`](../CHANGELOG.md).

Naming decisions is what keeps a version's diff legible: "restructure,"
"cite-background," "cut-ISACA-para" — each one a line you'll recognize later.

## Versioning: a version is a share-point

A **version** is a milestone **you declare** when you share the document — it does
**not** bump per edit. `MAJOR.MINOR.PATCH`:

- `0.1.0` — the baseline skeleton, first committed.
- **minor** (`0.2.0`) — a material milestone you'd re-share (a round of decisions).
- **patch** (`0.2.1`) — a small share (a fix, a formatting pass).
- `1.0.0` — the first final draft.

When you cut a version, the accumulated **[Unreleased]** decisions roll into a dated
`CHANGELOG.md` entry, each bullet **linking to its commit** — so a version is also
your recovery index: to get back text a decision removed, follow its commit link (or
Reject-All / `git show`).

## The suggestion engine (keep versions small)

Left alone, an [Unreleased] list grows until a version becomes a sprawling,
hard-to-review dump. The AI watches for that and **proposes cutting a version when
the pending decisions form a coherent, right-sized unit** — a rule of thumb of
**~2–4 related decisions**, or whenever a single decision is complete and worth
sharing on its own. It will:

1. Notice the pending decisions add up to something shareable.
2. Suggest the bump (`0.1.0 → 0.2.0`) with a one-line rationale.
3. Draft the `CHANGELOG.md` entry (title + per-decision bullets with commit links).
4. Leave the call to **you** — it suggests; you declare.

You can always say "not yet, keep going" or "cut it now." The goal is many small,
legible versions over a few giant ones.

## Before you share: the pre-share check

A shareable version should carry no open **blocker** markers (`WRITE/CITE/VERIFY/
Q/REF`) and no private ones (`NOTE/CUT?`). Run the lint:

```bash
python3 scripts/check_tags.py            # nonzero exit if any blocker is still open
```

See [`../PLACEHOLDERS.md`](../PLACEHOLDERS.md) for the marker vocabulary and the live
tracker. To gate shares automatically, add `check_tags.py` as a CI step on `*.docx`
changes.

## One writer at a time

A `.docx` is binary and can't be merged. When you want to edit in Word, tell the AI
"hands off"; it stops and **captures your storage-side edits into git before it
touches the file again**. Details in [`editing-protocol.md`](editing-protocol.md).

# Migrate a chat into a GitDoc document

Use this when you've **already been working a paper out in a chat** — the topic,
outline, themes, arguments, decisions — and you want to **formalize it into a
durable, versioned document** instead of leaving it stranded in a conversation. It
turns "we've discussed this a lot" into a tracked-changes `.docx` in its own repo,
synced to storage you open in Word.

**Where to paste it.** Two ways, both work:

- **Best — paste it into the chat that already holds the discussion**, *if* that chat
  is an agent that can clone a repo and run code (e.g. Claude Code with your new repo
  connected). The agent already has all the context, so you skip re-explaining and it
  goes straight to building.
- **Fresh session** — start a new agent on the new repo and paste a summary of where
  the paper stands into the slot below. (Tip: in the old chat, ask *"summarize the
  current draft, outline, decisions, and open questions for handoff,"* then paste
  that.)

Either way it needs an agent that can **clone repos and run code** (Claude Code on
web/CLI, or similar). A plain chat can help draft the plan but can't build the repo.

Fill the `<…>` slots and paste:

---

```text
I'm formalizing a paper we've been working through into a durable,
version-controlled GitDoc workspace. Its new home is this repo: <NEW_REPO_URL>

GitDoc — the template to adopt:
GitDoc authors a manuscript as Word tracked changes, versioned in git and synced to
storage I open in Word: https://github.com/Jtread0000/GitDoc
Bring it into <NEW_REPO_URL>: clone GitDoc and copy its machinery in — scripts/,
docs/, .claude/, .github/, AGENTS.md, CLAUDE.md, PLACEHOLDERS.md, CHANGELOG.md,
LOG.md, requirements.txt (keep the new repo's own LICENSE if it has one). Then
`pip install -r requirements.txt` and follow AGENTS.md (the gitdoc-setup flow).

Where the paper stands (the migrated context):
If you're reading this in the chat where we've already worked through the topic,
outline, themes, and decisions, use that as the baseline — don't make me repeat it.
Otherwise (a fresh session), here it is:
<Paste your current draft, or an outline plus the sections you have, the core
argument, decisions already settled, and open questions. Prose becomes the baseline
so we don't start from zero or relitigate what's already resolved.>

Do this, in order:
1. Read AGENTS.md and docs/ so you follow GitDoc's conventions: every edit is a
   tracked change I Accept/Reject; placeholder markers (blockers vs. author-only);
   a version is a share-point I declare; work groups into named "decisions".
2. Confirm the plan back to me FIRST in a few lines — the document title, the
   section structure, and the Dropbox folder name — before creating anything.
3. Bootstrap <title>.docx as the 0.1.0 baseline from the migrated context above.
   Use [[WRITE: …]] where prose is still needed, [[CITE: …]] / [[VERIFY: …]] on any
   claim or number that needs a source or check, and [[Q: …]] for open questions.
   Seed CHANGELOG.md at 0.1.0, start LOG.md, and fill the PLACEHOLDERS.md tracker.
4. Wire Dropbox sync to a folder of my choosing: set the DROPBOX_DEST_DIR repo
   variable to <e.g. /Research/<my-project-folder>> (a new subfolder), and tell me
   the three secrets to add from docs/setup-dropbox.md. Once synced, the .docx lands
   in that Dropbox folder, shows up in my local Dropbox, and opens in Word.
5. Commit, then from here make every change a tracked change I can Accept/Reject.

One writer at a time: if I say "hands off," stop and capture my Dropbox edits into
git before editing again.
```

---

After it confirms the plan and bootstraps the file, you're writing — see
[`getting-started.md`](getting-started.md) for the day-to-day loop and
[`workflow.md`](workflow.md) for decisions and versioning.

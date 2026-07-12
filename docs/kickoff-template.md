# Kickoff template — your first message to the AI

Copy everything in the box below, fill in the `<…>` blanks (delete any line that
doesn't apply), and paste it as your first message to the AI you've opened in your
fresh GitDoc clone. It's optional — you can also just talk through your goals and
let the agent draw the details out — but this gets you to a document fast.

---

```text
I've just cloned GitDoc to start a new document. Follow AGENTS.md.

## What I'm writing
A <TYPE: paper / dissertation chapter / proposal / article> titled
"<WORKING TITLE>", about <ONE-LINE TOPIC>.
Author label for tracked changes: <MY NAME>.

## Rough structure (optional — suggest one if I leave this blank)
- <Section 1>
- <Section 2>
- <Section 3>
(Drop a [[WRITE: …]] marker under anything we'll fill in later.)

## Storage sync
<Pick one:>
- Git only for now — I'll turn on storage sync later.
- Sync to my storage folder: <e.g. /Research/<PROJECT_FOLDER>>. I'll add the
  secrets from docs/setup-dropbox.md; set the DROPBOX_DEST_DIR repo variable.

## How I want us to work
1. Bootstrap the .docx as the 0.1.0 baseline, then make EVERY later edit a tracked
   change I can Accept/Reject. Group one decision under a single author string.
2. Verify each change before committing (accept_all reads clean, reject_all restores
   the original) — never skip this.
3. Commit with clear messages. Treat a version bump as a share-point I declare, not
   a per-edit counter; record it in CHANGELOG.md and LOG.md.
4. One writer at a time: if I say "hands off," stop and capture my storage edits into
   git before making changes.

Start by confirming the plan and (if syncing) the storage folder name, then
bootstrap the .docx.
```

---

That's it. Once the agent confirms and bootstraps the file, you're writing.

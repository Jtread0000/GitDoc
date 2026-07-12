# Editing protocol (avoid "conflicted copy" files)

A `.docx` is a **binary** file: Dropbox cannot merge two diverging versions, so if
it is edited in two places at once it keeps one and saves the other as a
`(… conflicted copy …)` file. That happens when a human edits in Word **while** a
git push also writes the file to Dropbox — the sync's conflict guard only sees what
is already uploaded to Dropbox's servers, not edits still open/unsynced in Word.

**One writer at a time on each document.**

- **Human wants to edit:** tell the agent "hands off `<file>`," edit in Word, then
  wait for Dropbox to show it fully synced (green check) before handing back. The
  agent will *capture* the Dropbox version into git before making changes.
- **Agent is editing:** it pushes to git and (when sync is enabled) the file lands
  in Dropbox; open that fresh copy, not an older local one.
- **A conflicted copy appears anyway:** nothing is lost. Give it to the agent to
  diff against the canonical and merge into git, then delete the copy.

## Pausing the sync during rapid co-editing
When a human and agent are trading edits quickly, comment out the `push:` block in
`.github/workflows/sync-to-dropbox.yml` so pushes can't overwrite a file that's
open in Word. Sync then runs only on demand (**Actions → Run workflow**). Re-enable
the `push:` block once editing settles.

## How capture works (so you trust it)
On each run the sync compares Dropbox's version fingerprint (`rev`) to the marker
it wrote last time. If Dropbox changed underneath it, it **downloads and commits**
the Dropbox copy into git instead of overwriting — your edit is persisted, then the
agent re-applies the intended changes on top. No Dropbox data is ever clobbered.

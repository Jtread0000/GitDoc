# Dropbox sync setup

The sync uses a Dropbox app + an **offline refresh token** so the GitHub Action
can mint short-lived access tokens forever without a human re-authorizing. Do this
once per Dropbox account.

## 1. Create a Dropbox app
1. Go to <https://www.dropbox.com/developers/apps> → **Create app**.
2. Choose **Scoped access** → **Full Dropbox** (or App folder if you keep
   everything under one folder).
3. On the app's **Permissions** tab enable: `files.metadata.read`,
   `files.content.read`, `files.content.write`. Click **Submit**.
4. From the **Settings** tab copy the **App key** and **App secret**.

## 2. Get an offline refresh token
The `token_access_type=offline` part is REQUIRED — without it you get a
short-lived token that expires in hours.

1. Visit this URL in a browser (replace `APP_KEY`):
   ```
   https://www.dropbox.com/oauth2/authorize?client_id=APP_KEY&token_access_type=offline&response_type=code
   ```
2. Approve, copy the **authorization code**.
3. Exchange it for a refresh token (replace all three placeholders):
   ```bash
   curl https://api.dropbox.com/oauth2/token \
     -d code=AUTHORIZATION_CODE \
     -d grant_type=authorization_code \
     -u APP_KEY:APP_SECRET
   ```
4. In the JSON response, copy `refresh_token`.

## 3. Add repo secrets and variables

> **Who sets what.** The three **secrets** and the `DROPBOX_DEST_DIR` **variable** are
> yours to add — an agent can't set GitHub secrets, and often can't set repo variables
> either, so it will hand you the exact value. [`.env.example`](../.env.example) is the
> one-glance checklist of every key and where it goes.

In the GitHub repo → **Settings → Secrets and variables → Actions**:

**Repository secrets** (not Environment secrets):
| Secret | Value |
| --- | --- |
| `DROPBOX_APP_KEY` | the App key |
| `DROPBOX_APP_SECRET` | the App secret |
| `DROPBOX_REFRESH_TOKEN` | the `refresh_token` from step 2 |

**Repository variables**:
| Variable | Value |
| --- | --- |
| `DROPBOX_DEST_DIR` | Dropbox folder to sync into, e.g. `/Research/MyProject` |
| `SYNC_FILES` | *(optional)* comma-separated files; default = every `*.docx` in the repo root |

## 4. Verify
Push a change to a `.docx` (or run the workflow manually via **Actions → Sync docs
to Dropbox → Run workflow**). The run log should say `created …` or `uploaded …`.
A green run that says `Dropbox sync skipped` means the secrets aren't set.

## Notes
- The sync writes tiny marker files under `<DROPBOX_DEST_DIR>/.sync/` to remember
  each file's last-synced version. Leave them alone.
- Nothing is ever hard-deleted. A Dropbox-side edit is captured into git, never
  overwritten (see `docs/editing-protocol.md`). The full loop is diagrammed in the
  README's **Storage sync** section.
- **Dropbox is the first backend, not the only planned one** — more storage targets
  (Google Drive, OneDrive) are on the roadmap. Track it in the repo issues.

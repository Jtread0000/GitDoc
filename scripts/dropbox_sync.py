#!/usr/bin/env python3
"""dropbox_sync.py — sync one or more files between git and Dropbox, safely,
with two-way conflict CAPTURE (never clobber a Dropbox-side edit).

Per-file logic each run:
  * Identical (Dropbox content == git content)      -> nothing to do.
  * git changed, Dropbox untouched since last sync   -> upload (overwrite Dropbox).
  * Dropbox changed since last sync (a conflict)     -> CAPTURE: download the
      Dropbox version, commit it into git, do NOT overwrite. Re-apply the desired
      changes on top of the captured version afterward.

"Changed since last sync" is judged by Dropbox's version fingerprint (`rev`),
recorded in a marker at <dest>/.sync/<file>.rev after each write. Whether two
copies are byte-identical is judged by Dropbox's `content_hash` (computed locally
too), so a no-op never churns.

Config (env):
  DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN   (required)
  DROPBOX_DEST_DIR    Dropbox folder to sync into (e.g. /Research/MyProject)
  SYNC_FILES          comma/space-separated files to sync; default: every *.docx
                      in the repo root
  GITHUB_REF_NAME     branch to push captures to (set automatically in Actions)

This is connector-independent: it talks to the Dropbox HTTP API directly with a
stored offline refresh token, so it handles binary files (e.g. .docx) that most
MCP connectors refuse.
"""
import base64
import glob
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEST_DIR = (os.environ.get("DROPBOX_DEST_DIR") or "/Documents").rstrip("/")
SYNC_DIR = f"{DEST_DIR}/.sync"
APP_KEY = os.environ["DROPBOX_APP_KEY"]
APP_SECRET = os.environ["DROPBOX_APP_SECRET"]
REFRESH_TOKEN = os.environ["DROPBOX_REFRESH_TOKEN"]
BRANCH = os.environ.get("GITHUB_REF_NAME", "").strip()


def _files():
    raw = os.environ.get("SYNC_FILES", "").replace(",", " ").split()
    return raw or sorted(glob.glob("*.docx"))


def _req(url, data, headers, retries=3):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=90) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(3 * (attempt + 1))
    raise SystemExit(f"::error title=Dropbox network error::{last}")


def get_access_token():
    data = urllib.parse.urlencode(
        {"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN}).encode()
    basic = base64.b64encode(f"{APP_KEY}:{APP_SECRET}".encode()).decode()
    _, body = _req("https://api.dropbox.com/oauth2/token", data,
                   {"Authorization": f"Basic {basic}",
                    "Content-Type": "application/x-www-form-urlencoded"})
    try:
        tok = json.loads(body).get("access_token")
    except Exception:
        tok = None
    if not tok:
        print(f"::error title=Dropbox token exchange failed::{body.decode(errors='replace')}")
        sys.exit(1)
    return tok


def get_metadata(token, path):
    status, body = _req("https://api.dropboxapi.com/2/files/get_metadata",
                        json.dumps({"path": path}).encode(),
                        {"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    if status == 200:
        return json.loads(body)
    if "not_found" in body.decode(errors="replace"):
        return None
    raise SystemExit(f"::error title=Dropbox get_metadata failed::{body.decode(errors='replace')}")


def download_bytes(token, path):
    status, body = _req("https://content.dropboxapi.com/2/files/download", None,
                        {"Authorization": f"Bearer {token}",
                         "Dropbox-API-Arg": json.dumps({"path": path})})
    return body if status == 200 else None


def upload_bytes(token, path, data):
    arg = {"path": path, "mode": "overwrite", "mute": True, "autorename": False}
    status, body = _req("https://content.dropboxapi.com/2/files/upload", data,
                        {"Authorization": f"Bearer {token}",
                         "Dropbox-API-Arg": json.dumps(arg),
                         "Content-Type": "application/octet-stream"})
    if status != 200:
        raise SystemExit(f"::error title=Dropbox upload failed::{path}: {body.decode(errors='replace')}")
    return json.loads(body)


def dropbox_content_hash(filepath):
    block = 4 * 1024 * 1024
    outer = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(block)
            if not chunk:
                break
            outer.update(hashlib.sha256(chunk).digest())
    return outer.hexdigest()


def marker_path(name):
    return f"{SYNC_DIR}/{os.path.basename(name)}.rev"


def read_marker(token, name):
    data = download_bytes(token, marker_path(name))
    return data.decode(errors="replace").strip() if data else None


def write_marker(token, name, rev):
    upload_bytes(token, marker_path(name), rev.encode())


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit(f"::error title=git {args[0]} failed::{(r.stderr or r.stdout).strip()}")
    return r


def configure_git():
    git("config", "--global", "--add", "safe.directory", os.getcwd(), check=False)
    git("config", "user.name", "github-actions[bot]", check=False)
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com", check=False)


def push_captures():
    target = BRANCH if BRANCH else "HEAD"
    for _ in range(3):
        r = git("push", "origin", f"HEAD:{target}", check=False)
        if r.returncode == 0:
            return True
        if BRANCH:
            git("fetch", "origin", BRANCH, check=False)
            git("rebase", f"origin/{BRANCH}", check=False)
        time.sleep(2)
    return False


def main():
    token = get_access_token()
    print("Access token acquired.")
    captured = []

    for name in _files():
        if not os.path.isfile(name):
            print(f"Skipping {name} (not present in this commit).")
            continue
        dest = f"{DEST_DIR}/{os.path.basename(name)}"
        meta = get_metadata(token, dest)

        if meta is None:
            m = upload_bytes(token, dest, open(name, "rb").read())
            write_marker(token, name, m["rev"])
            print(f"  created {name} -> {m.get('path_display')} ({m.get('size')} bytes)")
            continue

        dbx_rev, dbx_hash = meta.get("rev"), meta.get("content_hash")
        modified = meta.get("server_modified", "unknown time")

        if dropbox_content_hash(name) == dbx_hash:
            if read_marker(token, name) != dbx_rev:
                write_marker(token, name, dbx_rev)
            print(f"{name}: already in sync.")
            continue

        marker_rev = read_marker(token, name)
        if marker_rev and dbx_rev != marker_rev:
            data = download_bytes(token, dest)
            if data is None:
                raise SystemExit(f"::error title=Capture failed::could not download {dest}")
            with open(name, "wb") as fh:
                fh.write(data)
            captured.append((name, dbx_rev, modified))
            print(f"::notice title=Dropbox edit captured::'{name}' was edited in Dropbox "
                  f"(modified {modified}); capturing into git instead of overwriting.")
        else:
            m = upload_bytes(token, dest, open(name, "rb").read())
            write_marker(token, name, m["rev"])
            print(f"  uploaded {name} -> {m.get('path_display')} ({m.get('size')} bytes)")

    if captured:
        names = [c[0] for c in captured]
        configure_git()
        git("add", *names)
        git("commit", "-m", "Capture Dropbox edits: " + ", ".join(names) +
            "\n\nAuto-captured by the sync so Dropbox/reviewer edits are persisted "
            "into git before any overwrite. Re-apply pending desired changes on top.")
        if push_captures():
            for name, rev, _ in captured:
                write_marker(token, name, rev)
            print(f"::notice title=Captured to git::Persisted {len(names)} Dropbox edit(s).")
        else:
            print("::error title=Capture push failed::Committed the Dropbox edits locally but "
                  "could not push. Markers unchanged; next run retries. No Dropbox data overwritten.")
            sys.exit(1)

    print("Sync complete.")


if __name__ == "__main__":
    main()

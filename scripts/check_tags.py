#!/usr/bin/env python3
"""check_tags.py — pre-share lint for GitDoc placeholder tags.

A shareable draft should carry no OPEN blocker tags. This inspects the **Accept-All**
view of each `.docx` (what the document becomes if you accept every tracked change)
and reports any placeholder marker that still survives there. A marker you FILLED via
a tracked change is already gone from Accept-All, so it won't trip the check.

Tag classes (see PLACEHOLDERS.md):
  * BLOCKERS — must be zero before you cut a shareable version:
        WRITE  CITE  VERIFY  Q  REF
  * AUTHOR-ONLY — reported but never fail the check; strip before sharing:
        NOTE  CUT?

Exit status is nonzero if any OPEN BLOCKER remains, so a pre-share step or CI job can
gate on it. Standard library only; no dependencies.

Usage:
    python3 scripts/check_tags.py                 # every *.docx in the repo root
    python3 scripts/check_tags.py paper.docx …    # specific files
    python3 scripts/check_tags.py --quiet         # print only problems and the verdict
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_tracked_changes import accept_all  # noqa: E402

TAG_RE = re.compile(r"\[\[([A-Z]+\??)\s*:\s*(.*?)\]\]", re.S)
BLOCKERS = {"WRITE", "CITE", "VERIFY", "Q", "REF"}
AUTHOR_ONLY = {"NOTE", "CUT?"}


def open_tags(path):
    """Tags surviving Accept-All, as (tag, full_marker) pairs in document order."""
    text = accept_all(path)
    return [(m.group(1), m.group(0)) for m in TAG_RE.finditer(text)]


def check_file(path, quiet=False):
    tags = open_tags(path)
    blockers = [t for t in tags if t[0] in BLOCKERS]
    notes = [t for t in tags if t[0] not in BLOCKERS]
    if not quiet or blockers or notes:
        print(f"\n{path}: {len(blockers)} open blocker(s), {len(notes)} author-only tag(s)")
    for tag, full in blockers:
        print(f"  ✗ BLOCKER  {full}")
    for tag, full in notes:
        note = "strip before sharing" if tag == "NOTE" else "resolve the deletion"
        print(f"  · {tag:<5} {full}   ({note})")
    return len(blockers)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    quiet = "--quiet" in sys.argv[1:]
    files = args or sorted(glob.glob("*.docx"))
    if not files:
        print("No .docx found in the repo root yet — nothing to check.")
        return 0
    total = 0
    for f in files:
        if not os.path.isfile(f):
            print(f"skip {f} (not found)")
            continue
        total += check_file(f, quiet=quiet)
    print()
    if total:
        print(f"::warning:: {total} open blocker(s) remain — resolve before cutting a shareable version.")
        return 1
    print("✓ clean — no open blockers. Safe to cut a version (remember to strip NOTE/CUT? tags).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""End-to-end example: create a doc, make tracked edits, verify both views.
Run:  python3 examples/quickstart.py   (from the repo root)
"""
import sys
sys.path.insert(0, "scripts")
from docx_tracked_changes import TrackedEditor, accept_all, reject_all, new_docx  # noqa: E402

DOC = "quickstart.docx"

# 1. Bootstrap a document with a placeholder to fill later.
new_docx([
    "Executive Summary",
    "This proposal describes the study and what we need from you.",
    "[[WRITE: the one-line hook]]",
], DOC)

# 2. Edit as tracked changes (author groups the decision for Accept/Reject).
ed = TrackedEditor(DOC, author="Agent (draft)", date="2026-07-11T00:00:00Z")
ed.replace_text("[[WRITE: the one-line hook]]",
                "A unique, time-boxed opportunity to collect data most studies can't.")
ed.insert_after("what we need from you.",
                " In short: your sponsorship and a one-week runway.")
ed.save()

# 3. Verify BOTH directions before shipping.
acc, rej = accept_all(DOC), reject_all(DOC)
assert "[[WRITE" not in acc and "one-line hook" not in acc, "accept view should be clean"
assert "[[WRITE: the one-line hook]]" in rej, "reject view should restore the placeholder"
print("Accept-All view:\n" + acc)
print("\nOK — tracked changes verified. Now commit " + DOC + " and let the sync push it.")

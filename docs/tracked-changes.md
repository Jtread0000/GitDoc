# Tracked changes: how it works

A `.docx` is a zip; its body is `word/document.xml`. Word "tracked changes" are
two element types inside that XML:

- **Insertion** — `<w:ins w:id w:author w:date>…<w:r><w:t>NEW</w:t></w:r>…</w:ins>`
- **Deletion** — `<w:del w:id w:author w:date>…<w:r><w:delText>OLD</w:delText></w:r>…</w:del>`

`python-docx` cannot author these, so `scripts/docx_tracked_changes.py` edits the
XML directly. Every edit carries `w:author` + `w:date`, which is how Word lets a
reviewer **Accept/Reject "By Specific People"** (Review → Show Markup → Specific
People). Use the **same author string** for every edit that belongs to one
decision, so it accepts/rejects as a group.

## The loop
```python
from docx_tracked_changes import TrackedEditor, accept_all, reject_all, new_docx

# 1. Start from a base doc (bootstrap, or a Word/Google-Docs export with styles)
new_docx(["Executive Summary", "Body paragraph.", "[[WRITE: the hook]]"], "memo.docx")

# 2. Apply tracked changes. Anchors match on visible text — no run juggling.
ed = TrackedEditor("memo.docx", author="Claude (draft)", date="2026-07-11T00:00:00Z")
ed.replace_text("[[WRITE: the hook]]", "One compelling sentence.")  # tracked del+ins
ed.insert_after("Body paragraph.", " An added sentence.")           # tracked insert
ed.save()

# 3. ALWAYS verify both directions before shipping:
assert "[[WRITE" not in accept_all("memo.docx")   # Accept-All view is clean
assert "[[WRITE" in reject_all("memo.docx")        # Reject-All restores the original
```

## Rules that keep it reliable
- **Anchors must be unique.** Each `replace_text` / `insert_after` must match
  exactly one spot, or it raises — lengthen the anchor until it's unique.
- **`insert_after` anchors on the END of a run's text** (a sentence tail).
- **`replace_text` targets a substring inside one run** (a placeholder like
  `[[WRITE: …]]`, or a phrase). If a phrase spans runs, pick a shorter unique bit.
- **Verify with `accept_all` / `reject_all`** every time — they simulate Word, so a
  passing assertion means Word will render it the same way.
- **Placeholders convention:** author the base doc with `[[WRITE: what goes here]]`
  markers (optionally yellow-highlighted). Filling one is just
  `ed.replace_text("[[WRITE: …]]", "real text")`.

## Seeing the changes in Word
Tracked revisions are always *recorded* in the file, but whether Word *shows* them
depends on the reviewer's view: **Review → All Markup** shows every insertion and
deletion inline; **Simple Markup** shows only a change bar; **No Markup** hides them
(it renders the Accept-All view). So the guarantee is "every change is a reviewable
revision" — tell the writer to use **All Markup** for full inline visibility.

## Verifying / inspecting from the CLI
```bash
python3 scripts/docx_tracked_changes.py accept memo.docx   # Accept-All text
python3 scripts/docx_tracked_changes.py reject memo.docx   # Reject-All text
python3 scripts/docx_tracked_changes.py render memo.docx   # raw (shows both)
```

## Styling note
New inserted runs use `DEFAULT_RPR` (the major-theme heading font, which matches
Claude-exported docs). If your base document uses a different body font, set the
`rpr=` argument on `TrackedEditor` so insertions match the surrounding text.

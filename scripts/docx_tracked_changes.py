#!/usr/bin/env python3
"""docx_tracked_changes.py — create Word (.docx) files and apply real Word
*tracked changes* (<w:ins>/<w:del>) by direct OOXML surgery, plus simulate
Accept-All / Reject-All so an edit can be verified before it ships.

Why raw XML: python-docx cannot author tracked changes. A .docx is a zip whose
body is `word/document.xml`. Tracked changes are:
  * insertion: <w:ins w:id w:author w:date><w:r>…<w:t>NEW</w:t></w:r></w:ins>
  * deletion:  <w:del w:id w:author w:date><w:r>…<w:delText>OLD</w:delText></w:r></w:del>
Each carries w:author + w:date so Word can Accept/Reject "By Specific People"
(Review → Show Markup → Specific People). Group a decision by using the SAME
author string for every edit in it.

Typical loop (how these documents are edited):
    from docx_tracked_changes import TrackedEditor, accept_all, reject_all, new_docx
    new_docx(["Title", "First paragraph.", "[[WRITE: intro]]"], "memo.docx")
    ed = TrackedEditor("memo.docx", author="Claude (draft)")
    ed.replace_text("[[WRITE: intro]]", "The real introduction.")   # tracked del+ins
    ed.insert_after("First paragraph.", " A new tracked sentence.") # tracked ins
    ed.save()
    assert "[[WRITE" not in accept_all("memo.docx")   # accept view is clean
    assert "[[WRITE" in reject_all("memo.docx")        # reject restores original
Then sync memo.docx to Dropbox (see docs/setup-dropbox.md).

CLI:
    python3 docx_tracked_changes.py create source.txt out.docx  # blank-line-split paras
    python3 docx_tracked_changes.py render out.docx             # raw text
    python3 docx_tracked_changes.py accept out.docx             # Accept-All view
    python3 docx_tracked_changes.py reject out.docx             # Reject-All view

Dependencies: python-docx is needed ONLY for `new_docx`/`create`. Everything else
(editing an existing .docx, verifying) uses the standard library only.
"""
import re
import shutil
import sys
import zipfile
from xml.dom import minidom

DOC = "word/document.xml"
# Run-property block for new ins/del runs. Match your base document's body font;
# this default (Word "Heading"/major theme font) matches docs exported by Claude.
DEFAULT_RPR = '<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/></w:rPr>'


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --- read / write the docx body ------------------------------------------------
def read_xml(path):
    with zipfile.ZipFile(path) as z:
        return z.read(DOC).decode("utf-8")


def write_xml(path, xml):
    minidom.parseString(xml)  # fail fast on malformed XML before repackaging
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == DOC:
                data = xml.encode("utf-8")
            zo.writestr(it, data)
    shutil.move(tmp, path)


# --- tracked-change fragment builders -----------------------------------------
def build_ins(rid, author, date, text, rpr=DEFAULT_RPR):
    return (f'<w:ins w:id="{rid}" w:author="{author}" w:date="{date}">'
            f'<w:r>{rpr}<w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:ins>')


def build_del(rid, author, date, text, rpr=DEFAULT_RPR):
    return (f'<w:del w:id="{rid}" w:author="{author}" w:date="{date}">'
            f'<w:r>{rpr}<w:delText xml:space="preserve">{_esc(text)}</w:delText></w:r></w:del>')


class TrackedEditor:
    """Apply tracked changes to one .docx. All edits match on visible text, so you
    don't need to know the run structure. Each edit must resolve to exactly one
    location (raises AssertionError otherwise — make the anchor longer/unique)."""

    def __init__(self, path, author="Claude", date="2026-01-01T00:00:00Z", rpr=DEFAULT_RPR):
        self.path, self.author, self.date, self.rpr = path, author, date, rpr
        self.xml = read_xml(path)
        self._id = 1000

    def _nid(self):
        self._id += 1
        return self._id

    def insert_after(self, anchor, text):
        """Insert `text` as a tracked insertion right after a run whose <w:t> ENDS
        with `anchor`. Use the tail of a sentence as the anchor."""
        marker = _esc(anchor) + "</w:t></w:r>"
        n = self.xml.count(marker)
        assert n == 1, f"insert_after anchor not unique/at-run-end ({n}x): {anchor!r}"
        ins = build_ins(self._nid(), self.author, self.date, text, self.rpr)
        self.xml = self.xml.replace(marker, marker + ins)
        return self

    def replace_text(self, old, new):
        """Tracked replacement of a unique inline substring (must sit within one
        run's <w:t>): delete `old`, insert `new` in place. Also the way to fill a
        placeholder like [[WRITE: …]]."""
        esc_old = _esc(old)
        n = self.xml.count(esc_old)
        assert n == 1, f"replace_text target not unique ({n}x): {old!r}"
        i = self.xml.find(esc_old)
        rs = max(self.xml.rfind("<w:r>", 0, i), self.xml.rfind("<w:r ", 0, i))
        re_ = self.xml.find("</w:r>", i) + len("</w:r>")
        run = self.xml[rs:re_]
        m = re.search(r"(<w:rPr>.*?</w:rPr>)", run, re.S)
        rpr = m.group(1) if m else self.rpr
        tm = re.search(r"<w:t[^>]*>(.*?)</w:t>", run, re.S)
        assert tm and esc_old in tm.group(1), "target spans multiple runs; use a shorter unique anchor"
        before, after = tm.group(1).split(esc_old, 1)

        def R(t):
            return f'<w:r>{rpr}<w:t xml:space="preserve">{t}</w:t></w:r>' if t else ""

        newrun = (R(before)
                  + build_del(self._nid(), self.author, self.date, old, rpr)
                  + build_ins(self._nid(), self.author, self.date, new, rpr)
                  + R(after))
        self.xml = self.xml[:rs] + newrun + self.xml[re_:]
        return self

    # alias: filling a placeholder is just a tracked replacement
    replace_placeholder = replace_text

    def save(self):
        write_xml(self.path, self.xml)
        return self


# --- verification: simulate Word's Accept-All / Reject-All --------------------
def _apply(xml, accept):
    if accept:
        xml = re.sub(r"<w:del\b.*?</w:del>", "", xml, flags=re.S)   # drop deletions
        xml = re.sub(r"</?w:ins\b[^>]*>", "", xml)                  # keep insertions
    else:
        xml = re.sub(r"<w:ins\b.*?</w:ins>", "", xml, flags=re.S)   # drop insertions
        xml = re.sub(r"</?w:del\b[^>]*>", "", xml)                  # unwrap deletions
        xml = xml.replace("<w:delText", "<w:t").replace("</w:delText>", "</w:t>")
    return xml


def _paras(xml):
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        t = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.S))
        t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if t.strip():
            out.append(t)
    return out


def render(path):
    return "\n".join(_paras(read_xml(path)))


def accept_all(path):
    return "\n".join(_paras(_apply(read_xml(path), True)))


def reject_all(path):
    return "\n".join(_paras(_apply(read_xml(path), False)))


def new_docx(paragraphs, path):
    """Bootstrap a plain .docx from a list of paragraph strings (needs python-docx)."""
    from docx import Document
    d = Document()
    for para in paragraphs:
        d.add_paragraph(para)
    d.save(path)
    return path


def _cli():
    import argparse
    ap = argparse.ArgumentParser(description="Create/verify .docx tracked changes.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create", help="build a .docx from a blank-line-split text file")
    c.add_argument("txt")
    c.add_argument("out")
    for name in ("render", "accept", "reject"):
        sub.add_parser(name, help=f"{name} view of a .docx").add_argument("docx")
    a = ap.parse_args()
    if a.cmd == "create":
        paras = [p.strip() for p in open(a.txt, encoding="utf-8").read().split("\n\n") if p.strip()]
        new_docx(paras, a.out)
        print(f"wrote {a.out} ({len(paras)} paragraphs)")
    else:
        print({"render": render, "accept": accept_all, "reject": reject_all}[a.cmd](a.docx))


if __name__ == "__main__":
    _cli()

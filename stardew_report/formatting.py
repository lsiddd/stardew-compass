"""Render upstream report fragments with HTML5-correct table/list semantics."""

import re
import html5lib

MARK = {
    "ach_yes": "[x] ",
    "ms_yes": "[x] ",
    "ach_no": "[ ] ",
    "ms_no": "[ ] ",
    "ach_imp": "[-] ",
    "ms_imp": "[-] ",
    "result": "* ",
    "need": "! ",
    "warn": "! ",
    "explain": "  - ",
}
BLOCK = {
    "div",
    "p",
    "section",
    "fieldset",
    "legend",
    "ul",
    "ol",
    "table",
    *[f"h{i}" for i in range(1, 7)],
}
SPACE = re.compile(r"\s+")


def to_text(node):
    tag = node.tag
    if not isinstance(tag, str):
        return ""
    if tag == "br":
        return "\n"
    if tag in {"button", "script", "style"}:
        return ""
    if tag == "img":
        return f"[{node.attrib['alt']}]" if node.get("alt") else ""
    parts = [SPACE.sub(" ", node.text or "")]
    for child in node:
        parts.append(to_text(child))
        parts.append(SPACE.sub(" ", child.tail or ""))
    body = "".join(parts)
    if tag in {"td", "th"}:
        return body.strip().replace("\n", " ") + " | "
    if tag == "tr":
        return "\n" + body
    if tag == "li":
        return "\n- " + body.strip()
    mark = next((MARK[c] for c in node.get("class", "").split() if c in MARK), "")
    return "\n" + mark + body + "\n" if tag in BLOCK else mark + body


def text_of(markup):
    root = html5lib.parseFragment(
        markup, treebuilder="etree", namespaceHTMLElements=False
    )
    raw = to_text(root)
    lines = [
        re.sub(
            r"\s*\|$", "", re.sub(r"\s*\(No Details\)\s*", "", line, count=1).rstrip()
        )
        for line in raw.split("\n")
    ]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def heading(title, character="="):
    rule = character * 76
    return f"\n{rule}\n{title}\n{rule}\n"

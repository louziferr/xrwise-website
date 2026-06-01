#!/usr/bin/env python3
"""
wrap_i18n.py – Klammert allen sichtbaren Text in einer HTML-Datei mit {{ _('TEXT') }} ein.
Jinja-Blöcke ({% ... %}) und Jinja-Ausdrücke ({{ ... }}) werden NICHT angetastet.
HTML-Entities wie &amp; bleiben erhalten (BeautifulSoup kümmert sich darum).

Verwendung:
    python wrap_i18n.py input.html output.html
    python wrap_i18n.py input.html              # überschreibt die Originaldatei
"""

import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

# Tags, deren Inhalt NICHT übersetzt werden soll
SKIP_TAGS = {
    "script", "style", "code", "pre", "textarea",
    "noscript", "template", "svg", "math",
}

# Attribute, deren Wert ebenfalls übersetzt werden soll
TRANSLATABLE_ATTRS = {
    "placeholder", "title", "alt", "aria-label",
    "aria-placeholder", "data-tooltip",
}

JINJA_RE = re.compile(r'\{%-?.*?-?%\}|\{\{.*?\}\}', re.DOTALL)
PLACEHOLDER_RE = re.compile(r'\x02JINJA\d+\x02')


def contains_jinja_or_placeholder(text: str) -> bool:
    return bool(JINJA_RE.search(text) or PLACEHOLDER_RE.search(text))


def should_skip(tag) -> bool:
    return tag.name in SKIP_TAGS


def wrap_text(text: str) -> str:
    """Umschließt sichtbaren Text mit {{ _('...') }}.
    `text` ist bereits der von BS4 dekodierte String (z.B. '&' statt '&amp;').
    BS4 re-encodiert beim Serialisieren automatisch zurück zu &amp;."""
    stripped = text.strip()

    if not stripped:
        return text

    if contains_jinja_or_placeholder(stripped):
        return text

    if re.fullmatch(r"[\s\.,;:!?\-–—/\\|(){}\[\]<>\"'+*#%&@^~`]+", stripped):
        return text

    if stripped.startswith("{{ _(") and stripped.endswith(") }}"):
        return text

    # Zeilenumbrüche kollabieren → einzeilige msgid
    stripped = re.sub(r"\s*\n\s*", " ", stripped)

    leading  = text[: len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()):]
    escaped  = stripped.replace("'", "\\'")
    return f"{leading}{{{{ _('{escaped}') }}}}{trailing}"


def wrap_attr(val: str) -> str:
    stripped = val.strip()
    if not stripped:
        return val
    if contains_jinja_or_placeholder(stripped):
        return val
    if stripped.startswith("{{ _(") and stripped.endswith(") }}"):
        return val
    escaped = stripped.replace("'", "\\'")
    return f"{{{{ _('{escaped}') }}}}"


def process_node(node, stash: dict) -> None:
    if isinstance(node, Comment):
        return

    if isinstance(node, NavigableString):
        new_text = wrap_text(str(node))
        if new_text != str(node):
            node.replace_with(NavigableString(new_text))
        return

    if should_skip(node):
        return

    for attr in TRANSLATABLE_ATTRS:
        if node.get(attr):
            node[attr] = wrap_attr(node[attr])

    for child in list(node.children):
        process_node(child, stash)


def process_html(html_content: str) -> str:
    stash: dict[str, str] = {}
    counter = [0]

    def protect(m: re.Match) -> str:
        key = f"\x02JINJA{counter[0]}\x02"
        stash[key] = m.group(0)
        counter[0] += 1
        return key

    protected = JINJA_RE.sub(protect, html_content)

    soup = BeautifulSoup(protected, "html.parser")
    root = soup.body if soup.body else soup
    for child in list(root.children):
        process_node(child, stash)

    # formatter=None → BS4 serialisiert Entities so wie es sie intern speichert
    # (& wird zu &amp;), ohne weitere Transformationen
    result = soup.decode(formatter="minimal")

    for key, original in stash.items():
        result = result.replace(key, original)

    return result


def main():
    if len(sys.argv) < 2:
        print("Verwendung: python wrap_i18n.py input.html [output.html]")
        sys.exit(1)

    input_path  = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else input_path

    if not input_path.exists():
        print(f"Fehler: Datei nicht gefunden – {input_path}")
        sys.exit(1)

    html_content = input_path.read_text(encoding="utf-8")
    result       = process_html(html_content)
    output_path.write_text(result, encoding="utf-8")

    print(f"✓ Fertig! Gespeichert unter: {output_path}")


if __name__ == "__main__":
    main()
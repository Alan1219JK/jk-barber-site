"""Minimal markdown -> HTML for bloggartikler og statiske tekster.

Støtter: # overskrifter (h1 til h4), avsnitt, punktlister (-, *), nummererte lister (1.),
**fet**, *kursiv*, [lenke](url), `kode`, > sitat, --- (hr) og tabeller med | kolonner |.
Ingen rå HTML-blokker tolkes (de slippes gjennom uendret hvis linjen starter med <).
Tankestreker byttes til komma.
"""
import re

from .util import e, fix_dashes


def _inline(s: str) -> str:
    s = fix_dashes(s)
    s = e(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return s


def md_to_html(text: str, h_shift: int = 0) -> str:
    """h_shift=1 gjør '# ' til <h2> osv. (nyttig når sidemalen eier H1)."""
    lines = (text or "").replace("\r\n", "\n").split("\n")
    out, i = [], 0
    para = []

    def flush_para():
        if para:
            out.append("<p>" + _inline(" ".join(x.strip() for x in para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            flush_para()
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para()
            lvl = min(6, len(m.group(1)) + h_shift)
            out.append(f"<h{lvl}>{_inline(m.group(2).strip())}</h{lvl}>")
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", stripped):
            flush_para()
            out.append("<hr>")
            i += 1
            continue
        if stripped.startswith("<"):
            flush_para()
            out.append(line)
            i += 1
            continue
        if stripped.startswith(">"):
            flush_para()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote><p>" + _inline(" ".join(q)) + "</p></blockquote>")
            continue
        if re.match(r"^[-*]\s+", stripped):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\d+[.)]\s+", stripped):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ol>")
            continue
        if stripped.startswith("|"):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            rows = [r for r in rows if not all(re.match(r"^:?-{2,}:?$", c) for c in r)]
            if rows:
                head, body = rows[0], rows[1:]
                html = '<div class="tabell-wrap"><table><thead><tr>' + "".join(f"<th>{_inline(c)}</th>" for c in head) + "</tr></thead>"
                html += "<tbody>" + "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>"
                out.append(html)
            continue
        para.append(line)
        i += 1
    flush_para()
    return "\n".join(out)


def md_meta(text: str):
    """Leser enkel frontmatter (--- nøkkel: verdi ---) øverst i en md-fil. Returnerer (meta, brødtekst)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text or "", re.S)
    if not m:
        return {}, text or ""
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = fix_dashes(v.strip().strip('"'))
    return meta, m.group(2)

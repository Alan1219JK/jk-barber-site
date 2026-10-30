"""Ricos (Wix rich content) -> HTML for de migrerte blogginnleggene.

Kilde: cms-data/blogg-migrert.json (komprimert Ricos: PARAGRAPH, HEADING, BULLETED_LIST, ORDERED_LIST,
LIST_ITEM, IMAGE, DIVIDER, BLOCKQUOTE og TEXT med dekorasjonene BOLD, ITALIC, UNDERLINE, LINK).

    from lib.ricos import ricos_to_html, wix_image_url
    html = ricos_to_html(post["richContent"], skip_image_id=post["media"]["id"])

Regler: tankestreker byttes til komma, overskriftsnivåer flyttes så den øverste blir h2, tomme
avsnitt droppes, avsnitt som starter med "• " eller "* " samles til <ul>, bilder får wixstatic-URL
med skalering, alt-tekst og eventuell bildetekst.
"""
import re

from .util import e, fix_dashes

WIX = "https://static.wixstatic.com/media/"
BILDE_BREDDE = 1200


def wix_image_url(image_id: str, w: int = 0, h: int = 0, q: int = 80) -> str:
    """Offentlig URL for et Wix-media-id. Med w og h beskjæres (fill), med bare w skaleres (fit)."""
    if not image_id:
        return ""
    if image_id.startswith("http"):
        return image_id
    base = image_id.rsplit(".", 1)[0].replace("~mv2", "")
    if w and h:
        return f"{WIX}{image_id}/v1/fill/w_{w},h_{h},al_c,q_{q}/{base}.jpg"
    if w:
        return f"{WIX}{image_id}/v1/fit/w_{w},h_{w},q_{q}/{base}.jpg"
    return WIX + image_id


def _text(node) -> str:
    td = node.get("textData") or {}
    txt = e(fix_dashes(td.get("text", "")))
    txt = txt.replace("\n", "<br>")
    link = None
    bold = italic = under = False
    for d in td.get("decorations") or []:
        t = d.get("type")
        if t == "BOLD":
            bold = True
        elif t == "ITALIC":
            italic = True
        elif t == "UNDERLINE":
            under = True
        elif t == "LINK":
            link = ((d.get("linkData") or {}).get("link") or {})
    if bold:
        txt = f"<strong>{txt}</strong>"
    if italic:
        txt = f"<em>{txt}</em>"
    if link and link.get("url"):
        url = link["url"].strip()
        if not url.startswith(("http", "/", "mailto:", "tel:", "#")):
            url = "https://" + url
        ext = url.startswith("http") and "j-kbarber.no" not in url
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        txt = f'<a href="{e(url)}"{attrs}>{txt}</a>'
    elif under:
        txt = f"<u>{txt}</u>"
    return txt


def _inline(nodes) -> str:
    out = []
    for n in nodes or []:
        if n.get("type") == "TEXT":
            out.append(_text(n))
        else:
            out.append(_inline(n.get("nodes")))
    return "".join(out)


def _clean_para(html: str) -> str:
    """Fjerner innledende/avsluttende <br> og tomrom."""
    html = re.sub(r"^(\s|<br>)+", "", html)
    html = re.sub(r"(\s|<br>)+$", "", html)
    html = re.sub(r"(<br>\s*){3,}", "<br><br>", html)
    return html


def _plain(nodes) -> str:
    return "".join((n.get("textData") or {}).get("text", "") if n.get("type") == "TEXT" else _plain(n.get("nodes")) for n in nodes or [])


def _image(node) -> str:
    d = node.get("imageData") or {}
    im = d.get("image") or {}
    src = (im.get("src") or {})
    iid = src.get("id") or src.get("url") or ""
    w0, h0 = im.get("width") or BILDE_BREDDE, im.get("height") or int(BILDE_BREDDE * 9 / 16)
    w = min(BILDE_BREDDE, int(w0))
    h = max(1, round(h0 * w / w0))
    # Veldig høye bilder (portrett) begrenses til 4:5
    if h > w * 1.25:
        h = int(w * 1.25)
    url = wix_image_url(iid, w, h)
    alt = fix_dashes(d.get("altText") or "")
    cap = fix_dashes((d.get("caption") or "").strip())
    img = f'<img src="{e(url)}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    if cap:
        return f"<figure>{img}<figcaption class=\"muted small\">{e(cap)}</figcaption></figure>"
    return f"<figure>{img}</figure>"


def _list(node, tag) -> str:
    items = []
    for li in node.get("nodes") or []:
        parts = []
        for child in li.get("nodes") or []:
            if child.get("type") in ("PARAGRAPH", "HEADING"):
                parts.append(_clean_para(_inline(child.get("nodes"))))
            elif child.get("type") in ("BULLETED_LIST", "ORDERED_LIST"):
                parts.append(_list(child, "ul" if child["type"] == "BULLETED_LIST" else "ol"))
            else:
                parts.append(_clean_para(_inline(child.get("nodes"))))
        parts = [p for p in parts if p]
        if parts:
            items.append("<li>" + " ".join(parts) + "</li>")
    return f"<{tag}>{''.join(items)}</{tag}>" if items else ""


def _min_heading(nodes) -> int:
    lv = []
    for n in nodes or []:
        if n.get("type") == "HEADING" and _plain(n.get("nodes")).strip():
            lv.append(int((n.get("headingData") or {}).get("level") or 2))
    return min(lv) if lv else 2


def ricos_to_html(rich: dict, *, skip_image_id: str | None = None) -> str:
    nodes = (rich or {}).get("nodes") or []
    shift = 2 - _min_heading(nodes)
    out = []
    bullets = []
    skipped = False

    def flush_bullets():
        if bullets:
            out.append("<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>")
            bullets.clear()

    for n in nodes:
        t = n.get("type")
        if t == "PARAGRAPH":
            html = _clean_para(_inline(n.get("nodes")))
            if not html or html == "<br>":
                continue
            plain = _plain(n.get("nodes")).strip()
            if plain.startswith(("• ", "* ")):
                bullets.append(re.sub(r"^(•|\*)\s*", "", html))
                continue
            flush_bullets()
            # Flere avsnitt skilt med tom linje inne i ett Ricos-avsnitt
            for part in re.split(r"(?:<br>\s*){2,}", html):
                part = _clean_para(part)
                if part:
                    out.append(f"<p>{part}</p>")
        elif t == "HEADING":
            flush_bullets()
            txt = _clean_para(_inline(n.get("nodes")))
            txt = re.sub(r"</?strong>", "", txt)
            if not txt:
                continue
            lvl = min(4, max(2, int((n.get("headingData") or {}).get("level") or 2) + shift))
            out.append(f"<h{lvl}>{txt}</h{lvl}>")
        elif t in ("BULLETED_LIST", "ORDERED_LIST"):
            flush_bullets()
            out.append(_list(n, "ul" if t == "BULLETED_LIST" else "ol"))
        elif t == "IMAGE":
            flush_bullets()
            iid = (((n.get("imageData") or {}).get("image") or {}).get("src") or {}).get("id")
            if skip_image_id and iid == skip_image_id and not skipped:
                skipped = True
                continue
            out.append(_image(n))
        elif t == "DIVIDER":
            flush_bullets()
            out.append("<hr>")
        elif t == "BLOCKQUOTE":
            flush_bullets()
            out.append(f"<blockquote><p>{_clean_para(_inline(n.get('nodes')))}</p></blockquote>")
        else:
            # Ukjent node (video, tabell, HTML osv.): ta med teksten hvis det finnes noe
            txt = _clean_para(_inline(n.get("nodes")))
            if txt:
                flush_bullets()
                out.append(f"<p>{txt}</p>")
    flush_bullets()
    return "\n".join(out)


def ricos_plain(rich: dict) -> str:
    """Ren tekst (til ordtelling og utdrag)."""
    return re.sub(r"\s+", " ", _plain((rich or {}).get("nodes"))).strip()

"""Små hjelpere: escaping, slug, norsk tallformat, tekstbehandling."""
import html
import re
import unicodedata

DASHES = "–—"  # tankestrek og lang tankestrek, skal aldri ut i dist


def e(s) -> str:
    """HTML-escape for tekst i attributter og innhold."""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def slugify(s: str) -> str:
    s = str(s).strip().lower()
    s = s.replace("æ", "ae").replace("ø", "o").replace("å", "a")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def nb_num(n) -> str:
    """1029 -> '1 029' (tynt mellomrom erstattet med vanlig for enkel kopiering)."""
    try:
        n = int(round(float(n)))
    except (TypeError, ValueError):
        return str(n)
    return f"{n:,}".replace(",", " ")


def kr(n) -> str:
    return f"{nb_num(n)} kr"


def fix_dashes(s: str) -> str:
    """Bytter tankestreker til komma (regel: aldri tankestrek i output)."""
    if not s:
        return s
    s = re.sub(r"\s*[–—]\s*", ", ", s)
    return s


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def split_sentences(text: str):
    """Deler en tekst i setninger (enkelt, nok for norsk brødtekst)."""
    text = (text or "").strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÆØÅ\"(])", text)
    return [p.strip() for p in parts if p.strip()]


def chunk_even(items, n):
    """Fordeler en liste i n omtrent like store grupper (bevarer rekkefølge)."""
    items = list(items)
    if n <= 0 or not items:
        return [items]
    n = min(n, len(items))
    size, rest = divmod(len(items), n)
    out, i = [], 0
    for k in range(n):
        step = size + (1 if k < rest else 0)
        out.append(items[i:i + step])
        i += step
    return out


def tid(s: str) -> str:
    """'10:00-21:00' -> '10 til 21', '09:00-19:00' -> '9 til 19', 'Stengt' -> 'Stengt'."""
    if not s or "-" not in s:
        return s or ""
    a, b = s.split("-", 1)

    def h(t):
        t = t.strip()
        hh, _, mm = t.partition(":")
        hh = str(int(hh))
        return hh if mm in ("", "00") else f"{hh}.{mm}"

    return f"{h(a)} til {h(b)}"


def tid_schema(s: str):
    """'09:00-19:00' -> ('09:00','19:00') eller None."""
    if not s or "-" not in s:
        return None
    a, b = s.split("-", 1)
    return a.strip(), b.strip()


def truncate(s: str, n: int) -> str:
    s = (s or "").strip()
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",;:") + "."

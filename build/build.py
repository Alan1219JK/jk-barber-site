#!/usr/bin/env python3
"""Bygger hele j-kbarber.no som statiske filer i ../dist/.

    python3 build.py            bygg alt
    python3 build.py --check    bygg og kjør kontroller (gjøres alltid, men avslutter med feilkode ved feil)

Nye sidegrupper: legg en modul i pages/ som eksporterer render(ctx) -> dict[path, html].
path er ren URL med skråstrek ("/om-oss/") eller filnavn i rot ("404.html"). Modulene lastes i
alfabetisk rekkefølge, men forside.py først (andre moduler kan importere hjelpere derfra).
Sider med noindex (meta robots) holdes utenfor sitemap.xml automatisk.
"""
import html as htmlmod
import importlib
import re
import shutil
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lib import data as D  # noqa: E402

ROOT = HERE.parent
DIST = ROOT / "dist"
ASSETS_SRC = HERE / "assets"
LOGO_SRC = ROOT / "design" / "messing-800.png"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Sjekk(HTMLParser):
    """Enkel strukturkontroll: balanserte tagger og antall h1."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.feil, self.h1 = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.h1 += 1
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        if tag == "h1":
            self.h1 += 1

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.feil.append(f"uavsluttet <{self.stack.pop()}> før </{tag}>")
            self.stack.pop()
        else:
            self.feil.append(f"</{tag}> uten start")


def sjekk_html(path, html):
    problemer = []
    p = Sjekk()
    p.feed(html)
    p.close()
    if p.stack:
        problemer.append("uavsluttet: " + ", ".join(p.stack[-5:]))
    problemer += p.feil[:5]
    if p.h1 != 1:
        problemer.append(f"{p.h1} h1")
    if re.search(r"[–—]", html):
        problemer.append("tankestrek")
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m and len(htmlmod.unescape(m.group(1))) > 60:
        problemer.append(f"title {len(htmlmod.unescape(m.group(1)))} tegn")
    m = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    if m and not (120 <= len(htmlmod.unescape(m.group(1))) <= 160):
        problemer.append(f"description {len(htmlmod.unescape(m.group(1)))} tegn")
    for ord_ in ("midlertidig", "under arbeid"):
        if ord_ in html.lower():
            problemer.append(f"ordet '{ord_}'")
    return problemer


def last_moduler():
    navn = sorted(p.stem for p in (HERE / "pages").glob("*.py") if p.stem != "__init__")
    if "forside" in navn:
        navn.remove("forside")
        navn.insert(0, "forside")
    mods = []
    for n in navn:
        m = importlib.import_module(f"pages.{n}")
        if hasattr(m, "render"):
            mods.append(m)
    return mods


def skriv(path, html):
    if path.endswith(".html") or path.endswith(".xml") or path.endswith(".txt"):
        fil = DIST / path.lstrip("/")
    else:
        assert path.startswith("/") and path.endswith("/"), f"ugyldig sti: {path}"
        fil = DIST / path.strip("/") / "index.html" if path != "/" else DIST / "index.html"
    fil.parent.mkdir(parents=True, exist_ok=True)
    fil.write_text(html, encoding="utf-8")
    return fil


def main():
    ctx = D.load()
    ctx["build_date"] = date.today().isoformat()

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    for f in ASSETS_SRC.iterdir():
        if f.is_file():
            shutil.copy2(f, DIST / "assets" / f.name)
    shutil.copy2(LOGO_SRC, DIST / "assets" / "logo-messing.png")

    sider = {}
    for mod in last_moduler():
        out = mod.render(ctx)
        for path, html in out.items():
            if path in sider:
                raise SystemExit(f"Duplikat sti {path} fra {mod.__name__}")
            sider[path] = html
    ctx["sider"] = sider

    feil = 0
    sitemap = []
    for path, html in sider.items():
        skriv(path, html)
        prob = sjekk_html(path, html)
        if prob:
            feil += 1
            print(f"  ! {path}: {'; '.join(prob)}")
        if path.endswith("/") and 'name="robots" content="noindex' not in html:
            sitemap.append(path)

    base = ctx["site"]["base"]
    today = ctx["build_date"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in sorted(sitemap, key=lambda x: (x != "/", x.count("/"), x)):
        pri = "1.0" if p == "/" else ("0.9" if p.count("/") == 2 else "0.7")
        sm.append(f"  <url><loc>{base}{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    skriv("sitemap.xml", "\n".join(sm) + "\n")
    skriv("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /takk/\n\nSitemap: {base}/sitemap.xml\n")

    print(f"Skrev {len(sider)} sider + sitemap.xml + robots.txt til {DIST}")
    if feil:
        print(f"{feil} side(r) med merknader")
        if "--check" in sys.argv:
            sys.exit(1)


if __name__ == "__main__":
    main()

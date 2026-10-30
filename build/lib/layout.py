"""Base-mal: head, header, footer, sticky CTA, breadcrumbs, JSON-LD og gjenbrukbare komponenter.

Bruk fra en sidemodul:

    from lib import layout as L
    html = L.page(ctx,
        path="/avdelinger/ski/",            # ren URL med skråstrek, brukes til canonical/OG
        title="... | J&K Barber Shop",      # under 60 tegn
        description="...",                  # 140 til 155 tegn
        body=L.section(...) + ...,          # alt mellom header og footer, må inneholde nøyaktig én <h1>
        breadcrumbs=[("Avdelinger", "/avdelinger/"), ("Ski Storsenter", None)],  # Hjem legges til automatisk
        jsonld=[{...}, L.faq_jsonld(items)],  # liste med schema-dicts, BreadcrumbList legges til automatisk
        active="avdelinger",                # markerer menypunkt: avdelinger|tjenester|app|gavekort|produkter|om-oss|blogg
        bestill_url="https://fixit.no/booking/2881",  # mål for sticky "Bestill" på mobil (standard /bestill-time/)
        avdeling="ski",                     # ga4Avdeling til dataLayer (valgfritt)
        og_image=L.og("jk-barber-ski-fasade.jpg"),   # valgfritt
        noindex=False,
    )
"""
import json

from . import images as IM
from .util import e, kr

MENY = [
    ("avdelinger", "Avdelinger", "/avdelinger/"),
    ("tjenester", "Tjenester og priser", "/tjenester/"),
    ("app", "Appen", "/app/"),
    ("gavekort", "Gavekort", "/gavekort/"),
    ("produkter", "Produkter", "/produkter/"),
    ("om-oss", "Om oss", "/om-oss/"),
    ("blogg", "Blogg", "/blogg/"),
]

FONTS = "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Manrope:wght@400;500;600;700&display=swap"

DEFAULT_OG = "jk-barber-felles-hero-klipp-i-stol.jpg"


# ---------- små byggeklosser ----------

def attrs(**kw) -> str:
    out = []
    for k, v in kw.items():
        if v is None or v is False:
            continue
        k = k.rstrip("_").replace("_", "-")
        if v is True:
            out.append(k)
        else:
            out.append(f'{k}="{e(v)}"')
    return (" " + " ".join(out)) if out else ""


def btn(text, href, kind="p", *, size="", external=None, bestill=None, plassering=None, cls="", **kw) -> str:
    """Knapp. kind: p (messing), s (omriss), t (tekstlenke). bestill=avdelingsslug gir dataLayer-sporing."""
    classes = ["btn", f"btn-{kind}"]
    if size:
        classes.append(f"btn-{size}")
    if cls:
        classes.append(cls)
    if external is None:
        external = href.startswith("http")
    extra = {}
    if external:
        extra["target"] = "_blank"
        extra["rel"] = "noopener"
    if bestill is not None:
        extra["data_bestill"] = bestill or "felles"
        extra["data_plassering"] = plassering or ""
    return f'<a class="{" ".join(classes)}" href="{e(href)}"{attrs(**extra, **kw)}>{text}</a>'


def link(text, href, *, external=None, cls="", bestill=None, plassering=None, **kw) -> str:
    if external is None:
        external = href.startswith("http")
    extra = {}
    if external:
        extra["target"] = "_blank"
        extra["rel"] = "noopener"
    if bestill is not None:
        extra["data_bestill"] = bestill or "felles"
        extra["data_plassering"] = plassering or ""
    c = f' class="{e(cls)}"' if cls else ""
    return f'<a{c} href="{e(href)}"{attrs(**extra, **kw)}>{text}</a>'


def eyebrow(text, muted=False) -> str:
    return f'<div class="eyebrow{" eyebrow-m" if muted else ""}">{text}</div>'


def section(inner, *, cls="", id_="", tone="", wrap=True) -> str:
    """tone: '' (bakgrunn), 'flate' (#1B1917), 'mork' (#17150F)."""
    classes = ["sec"]
    if tone:
        classes.append(f"sec-{tone}")
    if cls:
        classes.append(cls)
    idp = f' id="{e(id_)}"' if id_ else ""
    body = f'<div class="wrap">{inner}</div>' if wrap else inner
    return f'<section class="{" ".join(classes)}"{idp}>{body}</section>'


def heading(h2, lead="", eye="", cls="", level=2) -> str:
    out = ['<div class="sec-head' + (f" {cls}" if cls else "") + '">']
    if eye:
        out.append(eyebrow(eye))
    out.append(f"<h{level}>{h2}</h{level}>")
    if lead:
        out.append(f'<p class="lead muted">{lead}</p>')
    out.append("</div>")
    return "".join(out)


def stars() -> str:
    return '<span class="stars" aria-hidden="true">★★★★★</span>'


def review_card(text, who, small=False) -> str:
    return (f'<figure class="card review{" review-s" if small else ""}">{stars()}'
            f'<blockquote><p>{e(text)}</p></blockquote><figcaption class="muted">{e(who)}</figcaption></figure>')


def cta_box(title, text, button_html, cls="") -> str:
    return (f'<div class="card cta-box{" " + cls if cls else ""}"><div><h2>{title}</h2>'
            f'<p class="muted">{text}</p></div>{button_html}</div>')


def faq_block(items, *, heading_text="Ofte stilte spørsmål", lead="", eye="Spørsmål og svar", id_="faq",
              open_first=True, side=True) -> str:
    """FAQ som <details>/<summary>. items: dicts med 'sporsmal' og 'svar' (HTML)."""
    if not items:
        return ""
    rows = []
    for i, f in enumerate(items):
        op = " open" if (open_first and i == 0) else ""
        rows.append(f'<details class="faq"{op}><summary><span>{e(f["sporsmal"])}</span>'
                    f'<span class="faq-ikon" aria-hidden="true"></span></summary>'
                    f'<div class="faq-svar">{f["svar"]}</div></details>')
    head = heading(heading_text, lead, eye)
    if side:
        return f'<div class="faq-grid" id="{e(id_)}">{head}<div class="faq-liste">{"".join(rows)}</div></div>'
    return f'<div id="{e(id_)}">{head}<div class="faq-liste">{"".join(rows)}</div></div>'


def faq_jsonld(items) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["sporsmal"],
             "acceptedAnswer": {"@type": "Answer", "text": f.get("svarTekst") or f["svar"]}}
            for f in items
        ],
    }


def pris_rad(navn, pris, varighet=None, href=None, last=False) -> str:
    n = f'<a href="{e(href)}">{e(navn)}</a>' if href else e(navn)
    v = f' <span class="muted">· {varighet} min</span>' if varighet else ""
    p = kr(pris) if isinstance(pris, (int, float)) else e(pris or "Tilbys ikke")
    return f'<div class="row{" row-last" if last else ""}"><span>{n}{v}</span><span class="pris">{p}</span></div>'


def tabell(head, rows, cls="pristabell") -> str:
    """Enkel tabell med horisontal scroll på mobil. head: liste med celler (HTML), rows: liste med lister."""
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tabell-wrap"><table class="{e(cls)}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def og(name, w=1200, h=630) -> str | None:
    return IM.url(name, w, h)


# ---------- header, footer, sticky ----------

def header(ctx, active=None) -> str:
    s = ctx["site"]
    items = "".join(
        f'<li><a class="n{" n-aktiv" if key == active else ""}" href="{href}"{" aria-current=\"page\"" if key == active else ""}>{text}</a></li>'
        for key, text, href in MENY
    )
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="J&amp;K Barber Shop, til forsiden"><img src="{IM.LOGO}" alt="" width="54" height="48"><span>J&amp;K <span class="brass">Barber Shop</span></span></a>
    <nav class="nav" id="hovedmeny" aria-label="Hovedmeny"><ul>{items}</ul>
      <div class="nav-mobil-ekstra"><a href="/kontakt/">Kontakt</a><a href="tel:{s["telefon"]}">Ring {s["telefonVisning"]}</a></div>
    </nav>
    <div class="header-cta">{btn("Bestill time", "/bestill-time/", bestill="felles", plassering="header")}
      <button class="meny-knapp" type="button" aria-expanded="false" aria-controls="hovedmeny" aria-label="Meny"><span class="meny-strek"></span></button>
    </div>
  </div>
</header>"""


def footer(ctx) -> str:
    s = ctx["site"]
    avd = "".join(
        f'<li><a href="{a["url"]}">{e(a["title"])}</a><span class="muted"> {e(a["gateadresse"])}, {e(a["postnummer"])} {e(a["poststed"])}</span></li>'
        for a in ctx["avdelinger"]
    )
    tj = "".join(f'<li><a href="{t["url"]}">{e(t["title"])}</a></li>' for t in ctx["tjenester"])
    tj += '<li><a href="/hjemmebarbering/">Hjemmebarbering</a></li><li><a href="/tjenester/">Alle priser</a></li>'
    mer = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in [
        ("Bestill time", "/bestill-time/"), ("J&amp;K-appen", "/app/"), ("Gavekort", "/gavekort/"),
        ("Produkter", "/produkter/"), ("Om oss", "/om-oss/"), ("Jobb", "/jobb/"), ("Franchise", "/franchise/"),
        ("Blogg", "/blogg/"), ("Kontakt", "/kontakt/"), ("Personvern", "/personvern/"),
    ])
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-om">
      <img src="{IM.LOGO}" alt="J&amp;K Barber Shop logo" width="122" height="110" loading="lazy">
      <div class="footer-navn">J&amp;K <span class="brass">Barber Shop</span></div>
      <p class="muted">Barbershop og herrefrisør siden 2018, for både menn og kvinner, i Follo, Bærum og Romerike.</p>
      <address class="muted">{e(s["juridisk"])}, org.nr. {e(s["orgnr"])}<br>Hovedkontor: {e(s["hovedkontor"])}<br>
      Tlf <a href="tel:{s["telefon"]}">{e(s["telefonVisning"])}</a> (felles for alle avdelinger)<br><a href="mailto:{s["epost"]}">{e(s["epost"])}</a></address>
      <div class="footer-app">
        <a class="btn btn-s btn-sm" href="{s["appStore"]}" target="_blank" rel="noopener" aria-label="Last ned J&amp;K Barber Shop-appen på App Store">App Store</a>
        <a class="btn btn-s btn-sm" href="{s["googlePlay"]}" target="_blank" rel="noopener" aria-label="Last ned J&amp;K Barber Shop-appen på Google Play">Google Play</a>
      </div>
      <div class="footer-sosial">Følg oss: <a href="{s["instagram"]}" target="_blank" rel="noopener">Instagram</a> · <a href="{s["facebook"]}" target="_blank" rel="noopener">Facebook</a></div>
    </div>
    <nav class="footer-kol" aria-label="Avdelinger"><h2>Avdelinger</h2><ul>{avd}</ul></nav>
    <nav class="footer-kol" aria-label="Tjenester"><h2>Tjenester</h2><ul>{tj}</ul></nav>
    <nav class="footer-kol" aria-label="Mer"><h2>J&amp;K</h2><ul>{mer}</ul>
      <p class="muted footer-soster">Søstersider: <a href="{s["nettbutikk"]}" target="_blank" rel="noopener">J&amp;K Shop</a> · <a href="https://www.j-kbeauty.no" target="_blank" rel="noopener">J&amp;K Beauty Salon</a></p>
    </nav>
  </div>
  <div class="wrap footer-bunn muted">© 2026 {e(s["juridisk"])}. Alle rettigheter reservert. <a href="/personvern/">Personvern</a> · <a href="/kontakt/">Kontakt</a> · <a href="/jobb/">Jobb</a> · <a href="/franchise/">Franchise</a></div>
</footer>"""


def sticky(ctx, bestill_url="/bestill-time/", avdeling="felles") -> str:
    s = ctx["site"]
    ext = ' target="_blank" rel="noopener"' if bestill_url.startswith("http") else ""
    return (f'<div class="sticky-cta" id="sticky-cta" aria-label="Hurtigvalg">'
            f'<a class="btn btn-p" href="{e(bestill_url)}"{ext} data-bestill="{e(avdeling)}" data-plassering="sticky">Bestill time</a>'
            f'<a class="btn btn-s" href="tel:{s["telefon"]}">Ring</a>'
            f'<a class="btn btn-s" href="/avdelinger/">Avdelinger</a></div>')


# ---------- breadcrumbs og schema ----------

def breadcrumbs_html(crumbs) -> str:
    """crumbs: [(navn, url|None)], uten Hjem."""
    parts = ['<a href="/">Hjem</a>']
    for navn, url in crumbs:
        parts.append(f'<a href="{e(url)}">{e(navn)}</a>' if url else f'<span aria-current="page">{e(navn)}</span>')
    return f'<nav class="wrap brod" aria-label="Du er her">{" <span aria-hidden=\"true\">·</span> ".join(parts)}</nav>'


def breadcrumb_jsonld(ctx, crumbs, path) -> dict:
    base = ctx["site"]["base"]
    items = [{"@type": "ListItem", "position": 1, "name": "J&K Barber Shop", "item": base + "/"}]
    for i, (navn, url) in enumerate(crumbs, start=2):
        items.append({"@type": "ListItem", "position": i, "name": navn, "item": base + (url or path)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def jsonld_script(obj) -> str:
    txt = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{txt}</script>'


# ---------- hele siden ----------

def page(ctx, *, path, title, description, body, breadcrumbs=None, jsonld=None, active=None,
         bestill_url="/bestill-time/", avdeling="felles", og_image=None, noindex=False, body_class="",
         og_type="website", extra_head="") -> str:
    s = ctx["site"]
    base = s["base"]
    canonical = base + path
    og_img = og_image or og(DEFAULT_OG) or (base + IM.LOGO)
    schemas = list(jsonld or [])
    if breadcrumbs:
        schemas.append(breadcrumb_jsonld(ctx, breadcrumbs, path))
    ld = "\n".join(jsonld_script(o) for o in schemas)
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    crumbs = breadcrumbs_html(breadcrumbs) if breadcrumbs else ""
    bc = f' class="{e(body_class)}"' if body_class else ""
    return f"""<!doctype html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{robots}
<link rel="canonical" href="{e(canonical)}">
<meta property="og:locale" content="nb_NO">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="J&amp;K Barber Shop">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{e(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{e(og_img)}">
<meta name="theme-color" content="#121110">
<link rel="icon" href="/assets/logo-messing.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/logo-messing.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/styles.css">
<script defer src="/assets/site.js"></script>
<!-- GTM -->
{extra_head}
{ld}
</head>
<body{bc}>
<!-- GTM -->
<a class="skip" href="#innhold">Hopp til innhold</a>
{header(ctx, active)}
{crumbs}
<main id="innhold">
{body}
</main>
{footer(ctx)}
{sticky(ctx, bestill_url, avdeling)}
</body>
</html>
"""

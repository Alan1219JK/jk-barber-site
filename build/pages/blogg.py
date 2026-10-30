"""/blogg/, /blogg/kategori/<slug>/ og /post/<slug>/ for alle 35 innlegg.

Innhold:
  - 20 nye artikler: /home/claude/jkbarber-analyse/blogg/01-*.md til 20-*.md (markdown med metablokk
    Slug, Title tag, Meta, Kategori, Hovedsøkeord, Bilde, Forfatter etter H1).
  - 15 migrerte innlegg: cms-data/blogg-migrert.json (Ricos hentet fra kladdene på den nye Wix-siten,
    konverteres med lib/ricos.py). Bygget kjører uten nett.
Design: design/Blogg.dc.html. Kategorier og ID-er: WIX-NY-SITE.md del 4.
"""
import json
import re
from datetime import date
from pathlib import Path

from lib import layout as L
from lib import images as IM
from lib.md import md_to_html
from lib.ricos import ricos_to_html, ricos_plain, wix_image_url
from lib.util import e, fix_dashes, strip_tags, truncate

ROOT = Path(__file__).resolve().parents[2]
ARTIKLER = Path("/home/claude/jkbarber-analyse/blogg")
MIGRERT_JSON = ROOT / "cms-data" / "blogg-migrert.json"

FORFATTER = "Barbererne hos J&K Barber Shop"
NY_DATO = "2026-11-03"
FREMHEVET = "hva-koster-herreklipp-og-skin-fade"
LOKALE = ["barbershop-ski", "frisor-kolbotn-barbershop", "barbershop-sandvika-storsenter",
          "barbershop-jessheim", "barbershop-strommen-storsenter", "frisor-rykkinn-senter"]
LOKAL_TAG = {"barbershop-ski": "Ski", "frisor-kolbotn-barbershop": "Kolbotn", "barbershop-sandvika-storsenter": "Sandvika",
             "barbershop-jessheim": "Jessheim", "barbershop-strommen-storsenter": "Strømmen", "frisor-rykkinn-senter": "Rykkinn"}
# Nye artikler som kan bruke et eksisterende bilde (images.py) i stedet for plassholderen fra metablokken.
BILDE_OVERRIDE = {
    "barbershop-ski": ("jk-barber-ski-fasade.jpg", "Fasaden til J&K Barber Shop på brugangen i Ski Storsenter"),
    "frisor-kolbotn-barbershop": ("jk-barber-kolbotn-interior.jpg", "Interiøret hos J&K Barber Shop på Kolbotn Torg"),
    "barbershop-sandvika-storsenter": ("jk-barber-sandvika-interior.jpg", "Interiøret hos J&K Barber Shop i Kjørbokollen, Sandvika Storsenter"),
    "frisor-rykkinn-senter": ("jk-barber-rykkinn-fasade.jpg", "J&K Barber Shop i 1. etasje på Rykkinn Senter"),
    "skin-fade-taper-fade-forskjellen": ("jk-barber-sandvika-skin-fade.jpg", "Skin fade klippet hos J&K Barber Shop"),
    "skjeggtrim-etter-ansiktsform": ("jk-barber-sandvika-skjeggtrim.jpg", "Skjeggtrim hos J&K Barber Shop"),
    "knivbarbering-slik-foregar-det": ("jk-barber-sandvika-barbering.jpg", "Knivbarbering hos J&K Barber Shop"),
    "slik-styler-du-skjegget": ("jk-barber-felles-skjegg.jpg", "Skjegg formet hos J&K Barber Shop"),
    "hvor-ofte-bor-menn-klippe-seg": ("jk-barber-felles-hero-klipp-i-stol.jpg", "Barberer hos J&K Barber Shop klipper en kunde"),
    "herrefrisor-eller-barber-forskjellen": ("jk-barber-felles-barberer-med-kunde.jpg", "Barberer hos J&K Barber Shop i samtale med kunde"),
    "drop-in-eller-bestilt-time": ("jk-barber-felles-interior-resepsjon.jpg", "Resepsjonen hos J&K Barber Shop"),
    "pomade-voks-leire-saltspray": ("jk-barber-felles-produkter-harvoks.jpg", "Hårvoks og pomade i hyllen hos J&K Barber Shop"),
}

# (slug, navn, Wix categoryId, beskrivelse, meta description)
KATEGORIER = [
    ("guider", "Guider", "44a07fa6-496b-4899-abd2-509934166426",
     "Grundige guider om klipp, fade, skjegg, barbering og priser, skrevet av barbererne våre.",
     "Guider fra barbererne hos J&K Barber Shop: skin fade, taper, herreklipp, knivbarbering, barneklipp og hva det koster i Follo, Bærum og Romerike."),
    ("skjegg", "Skjegg", "5a51bf08-3998-4727-8671-bb09a3b15a12",
     "Skjeggtrim, skjeggolje, flass i skjegget og hvordan du former skjegget etter ansiktet.",
     "Alt om skjegg fra J&K Barber Shop: skjeggtrim etter ansiktsform, skjeggolje, føning, flass i skjegget og hvordan du får et mykt og velstelt skjegg."),
    ("har-og-styling", "Hår og styling", "ca65403d-510a-4f3e-8f4f-41debc40ed22",
     "Hvor ofte du bør klippe deg, hvordan du styler håret og hva som passer hårtypen din.",
     "Hår og styling fra barbererne hos J&K Barber Shop: hvor ofte du bør klippe deg, hodebarbering, stylingteknikker og pleie for alle hårtyper."),
    ("produkter", "Produkter", "32d16a59-46f5-44d7-acba-05478852e208",
     "Pomade, voks, leire, saltspray og merkene vi bruker i salongen og selger på j-kshop.no.",
     "Produktguider fra J&K Barber Shop: pomade, voks, leire og saltspray, Reuzel, Pan Drwal og Davines. Det vi bruker i stolen, kan du ta med hjem."),
    ("barbershop-livet", "Barbershop-livet", "48b6f084-4c8c-4754-8363-7bdfafd41c29",
     "Slik finner du avdelingene våre, drop-in eller time, stempelkort, gavekort og livet i stolen.",
     "Barbershop-livet hos J&K Barber Shop: guider til avdelingene i Ski, Kolbotn, Sandvika, Jessheim, Strømmen og Rykkinn, drop-in, stempelkort og gavekort."),
]
KAT = {k[0]: k for k in KATEGORIER}
KAT_NAVN = {k[1]: k[0] for k in KATEGORIER}
KAT_ID = {k[2]: k[0] for k in KATEGORIER}

# Title tag under 60 tegn der metablokkens title er for lang (nøkkel = slug).
TITLE_FIX = {
    "frisor-kolbotn-barbershop": "Frisør i Kolbotn: herreklipp og skin fade | J&K Barber",
    "barbershop-sandvika-storsenter": "Barbershop i Sandvika Storsenter | J&K Barber Shop",
    "barbershop-jessheim": "Barbershop på Jessheim: skin fade og herreklipp | J&K",
    "frisor-rykkinn-senter": "Frisør på Rykkinn Senter: herreklipp og skjegg | J&K",
    "herreklipp-for-kvinner": "Herreklipp for kvinner: pixie og skin fade | J&K Barber",
    "skjeggtrim-etter-ansiktsform": "Skjeggtrim etter ansiktsform | J&K Barber Shop",
    "hodebarbering-guide": "Hodebarbering: hjemme eller hos barber | J&K Barber Shop",
    "hvor-ofte-bor-menn-klippe-seg": "Hvor ofte bør menn klippe seg? | J&K Barber Shop",
    "stempelkort-app-gratis-klipp": "Hver 10. klipp gratis med stempelkortet | J&K Barber",
    "gavekort-barber": "Gavekort hos barber: gaven til han som har alt | J&K",
    "skin-fade-taper-fade-forskjellen": "Skin fade vs taper fade: forskjellen | J&K Barber Shop",
    "barneklipp-forste-gang-tips": "Barneklipp første gang: 7 tips | J&K Barber Shop",
    "herrefrisor-eller-barber-forskjellen": "Herrefrisør eller barber: forskjellen | J&K Barber Shop",
    "pomade-voks-leire-saltspray": "Pomade, voks, leire eller saltspray? | J&K Barber Shop",
}

# Meta description 120 til 160 tegn der metablokkens er for lang (nøkkel = slug).
META_FIX = {
    "barneklipp-forste-gang-tips": "Skal gutten klippes for første gang? Barbererne hos J&K Barber Shop deler 7 tips som gjør første barneklipp trygg og rolig, og hva dere kan forvente.",
    "hvor-ofte-bor-menn-klippe-seg": "Hvor ofte bør du klippe deg? Det avhenger av frisyren. Barbererne hos J&K gir deg intervallene for buzz cut, skin fade, klassisk klipp og lengre hår.",
    "knivbarbering-slik-foregar-det": "Aldri prøvd knivbarbering? Hele ritualet trinn for trinn: varme håndklær, krem, kniv og etterbehandling. Hvor lang tid det tar, pris og hvem det passer for.",
    "barbershop-ski": "Leter du etter frisør i Ski? J&K Barber Shop har to avdelinger: Ski Storsenter (brugangen mot Telia) og Åsenveien 3. Skin fade, herreklipp og skjegg for alle.",
    "frisor-kolbotn-barbershop": "Leter du etter frisør i Kolbotn? J&K Barber Shop ligger på Kolbotn Torg ved Vinmonopolet. Skin fade, herreklipp, skjegg og barneklipp. 2 timer gratis parkering.",
    "barbershop-sandvika-storsenter": "Frisør i Sandvika Storsenter? J&K Barber Shop ligger i Kjørbokollen ved Cewe Japan Photo. Skin fade, herreklipp, skjegg og knivbarbering for menn og kvinner.",
    "barbershop-jessheim": "Barbershop på Jessheim? J&K Barber Shop ligger i 1. etasje på Jessheim Storsenter, mot Lindex. Skin fade, skjeggtrim, knivbarbering og herreklipp for alle.",
    "barbershop-strommen-storsenter": "Herrefrisør på Strømmen Storsenter? J&K ligger i 1. etasje i den eldste delen, mellom Fransa og Gullfunn. Skin fade, herreklipp og skjegg. Bestill time.",
    "frisor-rykkinn-senter": "Trenger du frisør på Rykkinn? J&K Barber Shop ligger i 1. etasje på Rykkinn Senter med herreklipp, skin fade, skjeggtrim og barneklipp. Gratis parkering.",
    "herrefrisor-eller-barber-forskjellen": "Herrefrisør, barber eller barbershop? Vi forklarer forskjellen i opplæring, verktøy og resultat, og hjelper deg å velge riktig for klipp, fade og skjegg.",
    "skjeggtrim-etter-ansiktsform": "Skjeggtrim handler om form, ikke bare lengde. Barbererne hos J&K forklarer hva som kler rundt, ovalt, firkantet og langt ansikt, og hvor linjene skal gå.",
    "hodebarbering-guide": "Vurderer du hodebarbering? Barberernes guide til å barbere hodet helt ned: hvem det passer for, hva som skjer hos barbereren, teknikk hjemme og pleie etterpå.",
    "pomade-voks-leire-saltspray": "Pomade eller voks? Leire eller saltspray? Barbererne hos J&K forklarer forskjellen på hold og glans, og hvilket stylingprodukt som passer håret og frisyren din.",
    "drop-in-eller-bestilt-time": "Kan du bare stikke innom barbereren, eller bør du bestille time? Barbererne hos J&K forklarer hvorfor vi anbefaler å bestille, og når drop-in fungerer.",
    "stempelkort-app-gratis-klipp": "Med J&K-appen får du stempel for hver klipp, skin fade, skjeggtrim eller kombo, og hvert 10. stempel gir gratis klipp. Slik fungerer de fire stempelkortene.",
    "gavekort-barber": "Gave til mannen som har alt? Et gavekort hos J&K Barber gir en time hos barbereren: knivbarbering, kombo eller far og sønn. Valgfritt beløp, innløses i kassen.",
}

# Migrerte innlegg: normalisert tittel (ikke versaler) og title tag.
MIGRERT_TITTEL = {
    "pan-drwal-skjegg-og-kropp": ("Pan Drwal: polsk barbershop-luksus for skjegg og kropp", "Pan Drwal: skjegg, pomade og aftershave | J&K Barber"),
    "flass-davines-harprodukter": ("Slik behandler du flass med Davines hårprodukter", "Flass? Slik behandler du det med Davines | J&K Barber"),
    "hvor-ofte-bor-jeg-besoke-frisoren-min": ("Hvor ofte bør jeg besøke frisøren min?", "Hvor ofte bør jeg besøke frisøren? | J&K Barber Shop"),
    "fordelene-med-a-ga-til-barberer": ("Hva er fordelene med å gå til en barberer?", "Fordelene med å gå til en barberer | J&K Barber Shop"),
    "ta-vare-pa-skjegget": ("Hvordan ta godt vare på skjegget", "Slik tar du godt vare på skjegget | J&K Barber Shop"),
    "pleietips-for-alle-hartyper": ("Pleietips for alle hårtyper", "Pleietips for alle hårtyper | J&K Barber Shop"),
    "flass-i-skjegget": ("Hvorfor får jeg flass i skjegget?", "Flass i skjegget: årsaker og løsning | J&K Barber Shop"),
    "reuzel-harvoks-og-pomade": ("Reuzel: hårvoks og pomade for alle frisyrer", "Reuzel hårvoks og pomade: velg riktig | J&K Barber Shop"),
    "skjeggolje-slik-bruker-du-den": ("Skjeggolje: slik bruker du den", "Skjeggolje: slik bruker du den riktig | J&K Barber Shop"),
    "slik-foner-du-skjegget": ("Slik føner du skjegget", "Slik føner du skjegget | J&K Barber Shop"),
    "slik-barberer-du-deg-hjemme": ("Slik barberer du deg lynraskt hjemme", "Slik barberer du deg lynraskt hjemme | J&K Barber Shop"),
    "mer-skjeggvekst": ("Kan jeg få mer skjeggvekst?", "Kan jeg få mer skjeggvekst? | J&K Barber Shop"),
    "harstyling-del-2-teknikker": ("Alt om hårstyling, del 2: smarte teknikker", "Hårstyling del 2: smarte teknikker | J&K Barber Shop"),
    "harstyling-del-1-grunnleggende": ("Alt om hårstyling, del 1: det grunnleggende", "Hårstyling del 1: det grunnleggende | J&K Barber Shop"),
    "mykt-skjegg-pa-1-2-3": ("Mykt skjegg på 1-2-3", "Mykt skjegg på 1-2-3: sjampo, olje, forming | J&K Barber"),
}
MIGRERT_META = {
    "pan-drwal-skjegg-og-kropp": "Pan Drwal er det polske grooming-merket vi bruker i salongen: skjeggolje, lotion, pomader, aftershave og tatoveringspleie. Guide til hele sortimentet.",
    "flass-davines-harprodukter": "Flass og irritert hodebunn? Barbererne hos J&K forklarer årsakene og hvordan du behandler flass trinn for trinn med Davines sjampo, balsam og leiremaske.",
    "hvor-ofte-bor-jeg-besoke-frisoren-min": "Hvor ofte bør du til frisøren? Barbererne hos J&K gir anbefalte intervaller for hårklipp, skin fade og skjeggtrim, og tips til pleie mellom besøkene.",
    "fordelene-med-a-ga-til-barberer": "Hvorfor gå til en barberer i stedet for en vanlig frisør? Profesjonalitet, råd tilpasset deg, enkel timebestilling og en atmosfære der du kan senke skuldrene.",
    "ta-vare-pa-skjegget": "Skjegget trenger andre produkter enn håret på hodet. Barbererne hos J&K forklarer skjeggsjampo, serum, børste og balm, og hvor ofte du bør innom til trim.",
    "pleietips-for-alle-hartyper": "Flass, fint hår, fett hår eller tørt og skadet hår? Barbererne hos J&K forklarer hvilken sjampo og pleie som passer hårtypen din, og hvordan du vasker riktig.",
    "flass-i-skjegget": "Flass i skjegget skyldes ofte stress, lite søvn, kosthold, kulde eller sopp. Her er barberernes tre steg for å bli kvitt det: peeling, skjeggsjampo og olje.",
    "reuzel-harvoks-og-pomade": "Reuzel Fiber, Clay eller rød, blå, grønn og rosa pomade? Barbererne hos J&K forklarer effekt, hold og formulering, så du finner riktig produkt til frisyren.",
    "skjeggolje-slik-bruker-du-den": "Hva skjeggolje er laget av, hvor mye du bør bruke, hvordan du påfører den og hvor ofte. Barberernes guide til et mykt, hydrert skjegg uten kløe og flass.",
    "slik-foner-du-skjegget": "Føning holder skjegget rett, fyldig og klart for trimming. Barbererne hos J&K viser hva du trenger, hvorfor det virker og fremgangsmåten steg for steg.",
    "slik-barberer-du-deg-hjemme": "Sju triks for å barbere deg raskt med tradisjonell høvel og kost: riktig krem, skum i ansiktet, korte tak, fast rekkefølge og aftershave som ansiktskrem.",
    "mer-skjeggvekst": "Kan du få mer skjeggvekst? Barbererne hos J&K forklarer hvorfor noen har mindre skjegg, om barbering gir tykkere skjegg, og hva som gir et fyldigere skjegg.",
    "harstyling-del-2-teknikker": "Smarte stylingteknikker fra barbererne: style i fuktig hår, bruk lite produkt, riktig verktøy, føner og børste, sjampo i tørt hår og kombiner produkter.",
    "harstyling-del-1-grunnleggende": "Hva er hårstyling, og hva betyr hold, shine, tyngde, tekstur, volum og definisjon? Barbererne hos J&K forklarer forskjellen på vannbasert og voksbasert.",
    "mykt-skjegg-pa-1-2-3": "Klør, flasser eller floker skjegget seg? Tre steg til et mykt skjegg: skjeggsjampo, fuktighet med olje, pomade eller lotion, og forming med børste og kam.",
}

APP_TEKST = "Last ned appen, bestill time og samle stempler. Fire stempelkort: klassisk klipp, skin fade, skjegg og kombo. Barbereren registrerer stempelet i salongen, og hvert 10. stempel gir gratis behandling."


# ---------- innlasting ----------

def _slashify(html: str) -> str:
    """Interne lenker på skråstrek-form: /tjenester/skin-fade -> /tjenester/skin-fade/."""
    def fix(m):
        url = m.group(1)
        if url == "/" or url.endswith("/") or "." in url.rsplit("/", 1)[-1] or "#" in url or "?" in url:
            return m.group(0)
        return f'href="{url}/"'
    return re.sub(r'href="(/[^"]*)"', fix, html)


def _faq_prep(md: str) -> str:
    """Linje som bare er **fet** (FAQ-spørsmål) blir eget avsnitt."""
    out = []
    for line in md.split("\n"):
        out.append(line)
        if re.match(r"^\*\*[^*]+\*\*\s*$", line.strip()):
            out.append("")
    return "\n".join(out)


def _faq_items(html: str):
    """Henter (spørsmål, svar) fra <p class="faq-q"> etterfulgt av <p>."""
    items = []
    for m in re.finditer(r'<p class="faq-q"><strong>(.+?)</strong></p>\s*<p>(.+?)</p>', html, re.S):
        items.append({"sporsmal": strip_tags(m.group(1)), "svar": m.group(2), "svarTekst": strip_tags(m.group(2))})
    return items


def last_nye():
    posts = []
    for fil in sorted(ARTIKLER.glob("[0-9][0-9]-*.md")):
        txt = fil.read_text(encoding="utf-8")
        lines = txt.split("\n")
        assert lines[0].startswith("# "), fil
        tittel = fix_dashes(lines[0][2:].strip())
        meta, i = {}, 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        while i < len(lines) and lines[i].strip():
            k, _, v = lines[i].partition(":")
            meta[k.strip()] = fix_dashes(v.strip())
            i += 1
        body = "\n".join(lines[i:]).strip()
        # Siste "## Bestill time"-avsnitt: behold teksten, fjern overskriften (CTA-boksen følger rett etter)
        body = re.sub(r"\n## Bestill time\s*\n", "\n", body)
        slug = meta["Slug"].strip("/").split("/")[-1]
        m = re.match(r"^(\S+)\s*\(alt:\s*(.+)\)\s*$", meta.get("Bilde", ""))
        bilde, alt = (m.group(1), m.group(2)) if m else (meta.get("Bilde", ""), tittel)
        if slug in BILDE_OVERRIDE and IM.has(BILDE_OVERRIDE[slug][0]):
            bilde, alt = BILDE_OVERRIDE[slug]
        html = md_to_html(_faq_prep(body), h_shift=0)
        html = re.sub(r"<p><strong>([^<]+\?)</strong></p>", r'<p class="faq-q"><strong>\1</strong></p>', html)
        html = _slashify(html)
        faq = _faq_items(html)
        ingress = strip_tags(re.search(r"<p>(.*?)</p>", html, re.S).group(1))
        posts.append({
            "slug": slug, "tittel": tittel, "kategori": KAT_NAVN[meta["Kategori"]],
            "title": TITLE_FIX.get(slug, meta["Title tag"]), "meta": META_FIX.get(slug, meta["Meta"]),
            "bilde": bilde, "alt": alt, "ny": True, "dato": NY_DATO, "endret": NY_DATO,
            "html": html, "faq": faq, "ingress": truncate(ingress, 150),
            "ord": len(strip_tags(html).split()), "sokeord": meta.get("Hovedsøkeord", ""),
        })
    return posts


def last_migrerte():
    data = json.loads(MIGRERT_JSON.read_text(encoding="utf-8"))
    posts = []
    for p in data["posts"]:
        slug = p["slug"]
        media = p.get("media") or {}
        html = ricos_to_html(p["richContent"], skip_image_id=media.get("id"))
        html = _slashify(html)
        tittel, title = MIGRERT_TITTEL.get(slug, (p["title"], p["title"] + " | J&K Barber Shop"))
        dato = (p.get("firstPublishedDate") or p.get("contentUpdated") or NY_DATO)[:10]
        kat = KAT_ID.get((p.get("categoryIds") or [None])[0], "guider")
        plain = ricos_plain(p["richContent"])
        ingress = truncate(fix_dashes((p.get("excerpt") or plain).rstrip(". ").rstrip(".")) + ".", 150)
        posts.append({
            "slug": slug, "tittel": fix_dashes(tittel), "kategori": kat,
            "title": title, "meta": MIGRERT_META[slug],
            "bilde": media.get("id"), "alt": media.get("altText") or tittel, "ny": False,
            "dato": dato, "endret": dato, "html": html, "faq": [], "ingress": ingress,
            "ord": len(plain.split()), "wixId": p["id"],
        })
    return posts


# ---------- komponenter ----------

def bilde(post, w, h, cls, lazy=True, motiv=""):
    if post["ny"]:
        return IM.picture(post["bilde"], post["alt"], w, h, cls=cls, lazy=lazy, motiv=motiv or post["alt"])
    url = wix_image_url(post["bilde"], w, h)
    attrs = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    return f'<img src="{e(url)}" alt="{e(post["alt"])}" width="{w}" height="{h}" {attrs} class="{e(cls)}">'


def bilde_url(post, w, h):
    if post["ny"]:
        return IM.url(post["bilde"], w, h)
    return wix_image_url(post["bilde"], w, h)


def kort(post, tag=None, with_ingress=True, mork=False):
    k = KAT[post["kategori"]]
    img = bilde(post, 600, 340, "kort-bilde")
    ing = f'<p class="muted small">{e(post["ingress"])}</p>' if with_ingress else ""
    cls = "card blogg-kort" + (" blogg-kort-mork" if mork else "")
    return (f'<article class="{cls}">{img}<div class="kort-innhold">'
            f'<a class="tag" href="/blogg/kategori/{k[0]}/">{e(tag or k[1])}</a>'
            f'<h3><a href="/post/{post["slug"]}/">{e(post["tittel"])}</a></h3>{ing}'
            f'<a class="kort-les" href="/post/{post["slug"]}/">Les guiden</a></div></article>')


def chips(aktiv=None):
    ch = [f'<a href="/blogg/"{" class=\"aktiv\"" if aktiv is None else ""}>Alle</a>']
    for slug, navn, *_ in KATEGORIER:
        ch.append(f'<a href="/blogg/kategori/{slug}/"{" class=\"aktiv\"" if aktiv == slug else ""}>{e(navn)}</a>')
    return f'<nav class="kategorier" aria-label="Kategorier">{"".join(ch)}</nav>'


def app_boks(ctx):
    s = ctx["site"]
    return L.section(
        f'<div class="card app-boks"><div>{L.eyebrow("J&amp;K-appen")}<h2>Hver 10. klipp gratis</h2>'
        f'<p class="muted">{APP_TEKST}</p>'
        f'<div class="knapper">{L.btn("App Store", s["appStore"])}{L.btn("Google Play", s["googlePlay"])}{L.btn("Slik fungerer det", "/app/", "s")}</div></div>'
        + IM.ph("Skjermbilde: stempelkort i appen", "jk-barber-felles-app-stempelkort-mobil.jpg", cls="app-boks-bilde") + "</div>",
        tone="mork")


def cta_bunn(plassering):
    return L.section(
        L.cta_box("Heller spørre barbereren direkte?",
                  "Bestill time i en av sju avdelinger. Konsultasjon først, så klipper vi. Avbestilling senest 24 timer før.",
                  L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering=plassering))
        + '<p class="muted small">Kategorier: ' + " · ".join(f'<a href="/blogg/kategori/{k[0]}/">{e(k[1])}</a>' for k in KATEGORIER) + "</p>")


def relaterte(post, alle):
    same = [p for p in alle if p["slug"] != post["slug"] and p["kategori"] == post["kategori"]]
    andre = [p for p in alle if p["slug"] != post["slug"] and p["kategori"] != post["kategori"]]
    # Nye artikler først, deretter migrerte; stabil rekkefølge etter liste
    same.sort(key=lambda p: (not p["ny"]))
    andre.sort(key=lambda p: (not p["ny"]))
    # Roter utvalget litt etter plassering i listen så ikke alle peker på de samme tre
    idx = [p["slug"] for p in alle].index(post["slug"])
    if len(same) > 3:
        same = same[idx % max(1, len(same) - 2):] + same[:idx % max(1, len(same) - 2)]
    return (same + andre)[:3]


def dato_nb(iso):
    mnd = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
    y, m, d = iso.split("-")
    return f"{int(d)}. {mnd[int(m) - 1]} {y}"


# ---------- sider ----------

def render_post(ctx, post, alle):
    s, base = ctx["site"], ctx["site"]["base"]
    k = KAT[post["kategori"]]
    url = f"/post/{post['slug']}/"
    lesetid = max(1, round(post["ord"] / 200))
    topp = bilde(post, 1200, 675, "artikkel-topp", lazy=False, motiv=f"Hovedbilde: {post['alt']}")
    meta = (f'<div class="artikkel-meta"><time datetime="{post["dato"]}">{dato_nb(post["dato"])}</time>'
            f'<span aria-hidden="true">·</span><a href="/blogg/kategori/{k[0]}/">{e(k[1])}</a>'
            f'<span aria-hidden="true">·</span><span>{e(FORFATTER)}</span>'
            f'<span aria-hidden="true">·</span><span>{lesetid} min lesetid</span></div>')
    hode = L.section(
        f'<div class="artikkel"><div class="artikkel-hode">{L.eyebrow(e(k[1]))}<h1>{e(post["tittel"])}</h1>{meta}</div>{topp}'
        f'<div class="prosa">{post["html"]}</div>'
        + L.cta_box("Bestill time", f"Snakk med barbereren om det du har lest. Velg avdeling, barberer og tidspunkt i onlinebookingen. {s['prisSetning']}",
                    L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering="artikkel-cta"))
        + f'<p class="muted small artikkel-deling">Skrevet av {e(FORFATTER)}. Spørsmål? Ring <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a> eller send e-post til <a href="mailto:{s["epost"]}">{s["epost"]}</a>.</p></div>',
        cls="sec-artikkel")
    rel = relaterte(post, alle)
    rel_html = L.section(
        '<div class="sec-head-rad">' + L.heading("Flere guider", "", "Les videre") + L.btn("Alle guider", "/blogg/", "s") + "</div>"
        f'<div class="grid grid-3">{"".join(kort(p) for p in rel)}</div>', tone="flate")
    body = hode + rel_html + cta_bunn("artikkel-bunn")

    img = bilde_url(post, 1200, 675) or IM.url("jk-barber-felles-hero-klipp-i-stol.jpg", 1200, 675)
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": base + url + "#post",
        "mainEntityOfPage": {"@type": "WebPage", "@id": base + url},
        "headline": post["tittel"],
        "description": post["meta"],
        "image": [img] if img else [IM.LOGO_SCHEMA],
        "datePublished": post["dato"],
        "dateModified": post["endret"],
        "author": {"@type": "Organization", "name": FORFATTER, "url": base + "/om-oss/"},
        "publisher": {"@type": "Organization", "@id": base + "/#organization", "name": "J&K Barber Shop",
                      "logo": {"@type": "ImageObject", "url": IM.LOGO_SCHEMA}},
        "articleSection": k[1],
        "inLanguage": "nb-NO",
        "wordCount": post["ord"],
        "isPartOf": {"@type": "Blog", "@id": base + "/blogg/#blog", "name": "Guider fra barbererne"},
    }
    if post.get("sokeord"):
        ld["keywords"] = post["sokeord"]
    schemas = [ld]
    if post["faq"]:
        schemas.append(L.faq_jsonld(post["faq"]))
    crumbs = [("Blogg", "/blogg/"), (k[1], f"/blogg/kategori/{k[0]}/"), (post["tittel"], None)]
    return L.page(ctx, path=url, title=post["title"], description=post["meta"], body=body, breadcrumbs=crumbs,
                  jsonld=schemas, active="blogg", og_image=img, og_type="article",
                  extra_head=f'<meta property="article:published_time" content="{post["dato"]}"><meta property="article:section" content="{e(k[1])}">')


def render_oversikt(ctx, alle):
    s, base = ctx["site"], ctx["site"]["base"]
    by = {p["slug"]: p for p in alle}
    frem = by[FREMHEVET]
    hero = L.section(
        f'<div class="sec-head sec-head-stor">{L.eyebrow("Blogg")}<h1>Guider fra barbererne</h1>'
        '<p class="lead muted">Her svarer vi på det kundene spør om i stolen: hva en skin fade egentlig er, hvilket stylingprodukt som passer håret ditt, hvor ofte du bør klippe deg, og hva det koster. Skrevet av barbererne våre, uten fagprat du ikke trenger.</p></div>'
        + chips(), cls="sec-hero")
    fk = KAT[frem["kategori"]]
    fremhevet = L.section(
        f'<article class="card fremhevet">{bilde(frem, 900, 640, "fremhevet-bilde", lazy=False, motiv="Barberer viser prislisten eller klipper skin fade")}'
        f'<div class="fremhevet-tekst"><div class="artikkel-meta"><a class="tag" href="/blogg/kategori/{fk[0]}/">{e(fk[1])}</a><span>Fremhevet · {max(1, round(frem["ord"] / 200))} min lesetid</span></div>'
        f'<h2><a href="/post/{frem["slug"]}/">{e(frem["tittel"])}</a></h2>'
        '<p class="muted">Vi går gjennom hva en klassisk herreklipp, skin fade, skjeggtrim og kombo koster hos oss og i området rundt, hvorfor prisen avhenger av barberens nivå (Lærling, Junior, Barber, Senior), og hvordan du får hver 10. klipp gratis med appen.</p>'
        f'<div class="knapper">{L.btn("Les prisguiden", f"/post/{frem['slug']}/")}{L.btn("Se alle priser", "/tjenester/", "s")}</div></div></article>')
    lok = "".join(kort(by[sl], tag=LOKAL_TAG[sl], mork=True) for sl in LOKALE)
    lokalt = L.section(
        '<div class="sec-head-rad">' + L.heading("Guider for din avdeling", "Hvor i senteret vi ligger, hvor du parkerer, og hva du kan bestille hos barbereren nær deg. Én guide per sted.", "Lokalt")
        + L.link("Se alle avdelinger", "/avdelinger/") + f'</div><div class="grid grid-3">{lok}</div>', tone="flate", id_="lokalt")
    ovrige = [p for p in alle if p["slug"] != FREMHEVET and p["slug"] not in LOKALE]
    ovrige.sort(key=lambda p: (not p["ny"], p["dato"]), reverse=False)
    ovrige = sorted(ovrige, key=lambda p: (not p["ny"]))
    rute = L.section(
        '<div class="sec-head-rad">' + L.heading("Det kundene spør om i stolen", "", "Alle guider")
        + f'<p class="muted small">{len(alle)} guider i fem kategorier</p></div>'
        f'<div class="grid grid-4">{"".join(kort(p, with_ingress=False) for p in ovrige)}</div>', id_="alle")
    body = hero + fremhevet + lokalt + rute + app_boks(ctx) + cta_bunn("blogg-cta")
    items = [{"@type": "ListItem", "position": i + 1, "url": base + f"/post/{p['slug']}/", "name": p["tittel"]} for i, p in enumerate(alle)]
    ld = [{"@context": "https://schema.org", "@type": "Blog", "@id": base + "/blogg/#blog", "name": "Guider fra barbererne",
           "url": base + "/blogg/", "inLanguage": "nb-NO", "publisher": {"@id": base + "/#organization"},
           "blogPost": [{"@type": "BlogPosting", "headline": p["tittel"], "url": base + f"/post/{p['slug']}/", "datePublished": p["dato"]} for p in alle]},
          {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items}]
    return L.page(ctx, path="/blogg/", title="Blogg: guider fra barbererne | J&K Barber Shop",
                  description="Guider fra barbererne hos J&K Barber Shop: skin fade og taper, priser på herreklipp, skjeggtrim, knivbarbering, stylingprodukter og veien til avdelingene.",
                  body=body, breadcrumbs=[("Blogg", None)], jsonld=ld, active="blogg")


def render_kategori(ctx, k, alle):
    slug, navn, _, besk, meta = k
    base = ctx["site"]["base"]
    posts = [p for p in alle if p["kategori"] == slug]
    posts = sorted(posts, key=lambda p: (not p["ny"]))
    hero = L.section(
        f'<div class="sec-head sec-head-stor">{L.eyebrow("Blogg")}<h1>{e(navn)}</h1><p class="lead muted">{e(besk)} {len(posts)} guider.</p></div>' + chips(slug),
        cls="sec-hero")
    rute = L.section(f'<div class="grid grid-3">{"".join(kort(p) for p in posts)}</div>')
    body = hero + rute + app_boks(ctx) + cta_bunn("kategori-cta")
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{navn}, guider fra J&K Barber Shop",
          "url": base + f"/blogg/kategori/{slug}/", "isPartOf": {"@id": base + "/blogg/#blog"}, "inLanguage": "nb-NO",
          "mainEntity": {"@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": base + f"/post/{p['slug']}/", "name": p["tittel"]} for i, p in enumerate(posts)]}}
    return L.page(ctx, path=f"/blogg/kategori/{slug}/", title=f"{navn}: guider fra barbererne | J&K Barber Shop",
                  description=meta, body=body, breadcrumbs=[("Blogg", "/blogg/"), (navn, None)], jsonld=[ld], active="blogg")


def render(ctx):
    alle = last_nye() + last_migrerte()
    assert len(alle) == 35, len(alle)
    assert len({p["slug"] for p in alle}) == 35
    ctx["blogg"] = alle
    out = {"/blogg/": render_oversikt(ctx, alle)}
    for k in KATEGORIER:
        out[f"/blogg/kategori/{k[0]}/"] = render_kategori(ctx, k, alle)
    for p in alle:
        out[f"/post/{p['slug']}/"] = render_post(ctx, p, alle)
    return out

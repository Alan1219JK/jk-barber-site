"""Laster kildedata (cms-data/data.json) og faste fakta, og gir en ctx-dict til sidemodulene.

ctx-nøkler:
  site        faste fakta (telefon, e-post, org.nr., lenker, merker, nivåer)
  avdelinger  liste med 7 avdelinger (dict, sortert på rekkefolge), alle felt fra CMS pluss
              'url', 'nabo' (liste med slugs), 'rating', 'antall', 'reviewsUrl', 'bloggSlug', 'bloggTittel'
  avd         dict slug -> avdeling
  tjenester   liste med 6 tjenester (dict), pluss 'url', 'bloggSlug', 'bloggTittel', 'hovedBehandling'
  tj          dict slug -> tjeneste
  priser      liste med alle prisrader (dict)
  faq         liste med alle FAQ (dict med 'sporsmal', 'svar' (HTML), 'svarTekst')
  fn          hjelpefunksjoner: hovedpriser(slug), pris(tjeneste_slug, avd_slug), priser_tjeneste(slug),
              priser_kategori(), faq_for(sted, slug=None), nabo_avdelinger(slug)
"""
import json
from pathlib import Path

from .util import strip_tags, fix_dashes

ROOT = Path(__file__).resolve().parents[2]
DATA_JSON = ROOT / "cms-data" / "data.json"

SITE = {
    "navn": "J&K Barber Shop",
    "juridisk": "JK Barber Drift AS",
    "base": "https://www.j-kbarber.no",
    "telefon": "+4790800086",
    "telefonVisning": "90 80 00 86",
    "epost": "post@j-kbarber.no",
    "orgnr": "932 372 614",
    "hovedkontor": "Åsenveien 3, 1400 Ski",
    "instagram": "https://www.instagram.com/jkbarbershopnorge",
    "facebook": "https://www.facebook.com/jkbarbershopnorge",
    "appStore": "https://apps.apple.com/no/app/id6463275107",
    "googlePlay": "https://play.google.com/store/apps/details?id=appfirm.jkbarbershop",
    "gavekort": "https://fixit.no/gavekort/1634",
    "nettbutikk": "https://www.j-kshop.no",
    "anmeldelser": "Over 1 100 Google-anmeldelser",
    "snitt": "4,8",
    "prisSetning": "Prisen avhenger av barberens nivå (Lærling, Junior, Barber, Senior). Endelig pris ser du i onlinebookingen.",
    "regel0": "Alle behandlingene på menyen er for både menn og kvinner. Vil du ha kort hår, skin fade eller en skikkelig herreklipp, er du velkommen uansett kjønn.",
    "gtm": "GTM-TH8SNQ7",
    "wixClientId": "dbd18313-acf6-4a35-b6e3-11b05b4d0914",
    "forms": {
        "kontakt": "46d9f072-fc1c-4aa0-8e3e-ef43548f3c1d",
        "jobb": "4db6b92d-98f9-4964-bdf8-c3a7ec589c15",
        "franchise": "af4ebbfe-481d-4a49-bbeb-c86c9fd70e6d",
        "hjemmebarbering": "28632583-0742-4e13-9a61-37a609717a9a",
    },
    "nivaer": [
        ("Lærling", "Under opplæring hos oss, alltid med en erfaren barberer i nærheten. Laveste pris."),
        ("Junior", "Ferdig utdannet og trygg på de vanligste klippene."),
        ("Barber", "Erfaren, selvstendig og rask i hendene. Her ligger de fleste av oss."),
        ("Senior", "Våre mest erfarne, spesialister på skin fade, skjegg og kniv. Høyeste pris."),
    ],
}

UTM = "?utm_source=j-kbarber&utm_medium=referral&utm_campaign=produkter"
MERKER = [
    ("Davines", "https://j-kshop.no/collections/davines" + UTM),
    ("in:on", "https://j-kshop.no/collections/in-on" + UTM),
    ("Uppercut Deluxe", "https://j-kshop.no/collections/uppercut-deluxe" + UTM),
    ("Reuzel", "https://j-kshop.no/collections/reuzel" + UTM),
    ("Taylor of Old Bond Street", "https://j-kshop.no/collections/taylor-of-old-bond-street" + UTM),
    ("Pan Drwal", "https://j-kshop.no/collections/pan-drwal" + UTM),
    ("Slickhaven", "https://j-kshop.no/collections/slickhaven" + UTM),
    ("Jobski Cosmetics", "https://j-kshop.no/collections/jobski-cosmetics" + UTM),
    ("Gråbein", "https://j-kshop.no/collections/graabein" + UTM),
    ("Proraso", "https://j-kshop.no/collections/proraso" + UTM),
    ("HUFS", "https://j-kshop.no/collections/hufs" + UTM),
]

# Google-tall per profil (fakta-priser-anmeldelser.md, 23.10.2026). reviewsUrl er søk-lenke til Google Maps
# inntil gbpUrl/reviewsUrl er fylt i CMS (Avdelinger-samlingen).
GOOGLE = {
    "sandvika": ("4,9", 381),
    "ski": ("4,7", 409),
    "asenveien": ("4,9", 70),
    "kolbotn": ("4,9", 172),
    "jessheim": ("4,6", 48),
    "strommen": ("5,0", 54),
    "rykkinn": ("5,0", 28),
}

# Lokal bloggartikkel per avdeling (/post/<slug>/). Åsenveien deler Ski-artikkelen.
BLOGG_AVD = {
    "sandvika": ("barbershop-sandvika-storsenter", "Barbershop i Sandvika Storsenter: slik finner du J&K i Kjørbokollen",
                 "Inngang, parkering og hva du kan bestille hos barbereren ved siden av Cewe Japan Photo."),
    "ski": ("barbershop-ski", "Barbershop i Ski: herreklipp og skin fade på Ski Storsenter og i Åsenveien",
            "To avdelinger i Ski, to minutter fra stasjonen. Slik velger du, og hva du kan bestille."),
    "asenveien": ("barbershop-ski", "Barbershop i Ski: herreklipp og skin fade på Ski Storsenter og i Åsenveien",
                  "Der det startet i 2018. Slik finner du oss i Åsenveien 3, og forskjellen på de to Ski-avdelingene."),
    "kolbotn": ("frisor-kolbotn-barbershop", "Frisør i Kolbotn? Slik er herreklipp og skin fade hos barbereren på Kolbotn Torg",
                "Ved Vinmonopolet, kort vei fra stasjonen. Hva du kan bestille, og hvordan du parkerer gratis."),
    "jessheim": ("barbershop-jessheim", "Barbershop på Jessheim: skin fade, skjegg og herreklipp på Jessheim Storsenter",
                 "1. etasje mot Lindex, midt i Jessheim sentrum. Slik finner du oss, og hva du kan bestille."),
    "strommen": ("barbershop-strommen-storsenter", "Herrefrisør på Strømmen Storsenter",
                 "Mellom Fransa og Gullfunn i den eldste delen av senteret. Fem minutter fra Lillestrøm."),
    "rykkinn": ("frisor-rykkinn-senter", "Frisør på Rykkinn Senter: herreklipp og skjegg uten å dra til Sandvika",
                "Bærum vests egen barbershop. Slik finner du oss, og hva du kan bestille."),
}

SEO_BESKRIVELSE_KORT = {
    "asenveien": "J&K Barber Shop i Åsenveien 3, Ski sentrum: der det startet i 2018, den roligste salongen vår, med gratis parkering utenfor. Herreklipp, skin fade og skjegg.",
}

# Guideartikkel per tjeneste (/post/<slug>/).
BLOGG_TJ = {
    "herreklipp": ("hvor-ofte-bor-menn-klippe-seg", "Hvor ofte bør menn klippe seg?",
                   "Hvor ofte du bør i stolen for kort, mellomlangt og lengre hår, og hvordan du holder klippen mellom besøkene."),
    "skin-fade": ("skin-fade-taper-fade-forskjellen", "Skin fade, taper fade, low, mid og high: forskjellen forklart",
                  "Hva som skiller de ulike fadene, hvilken som passer hodeformen og håret ditt, og hva du skal si i stolen."),
    "skjeggtrim": ("skjeggtrim-etter-ansiktsform", "Skjeggtrim: slik former du skjegget etter ansiktsformen",
                   "Kinnlinje, halslinje og lengde: slik får skjegget form som kler ansiktet ditt."),
    "barbering": ("knivbarbering-slik-foregar-det", "Knivbarbering: hva skjer, hvor lang tid tar det?",
                  "Varme håndklær, krem, kniv og etterbehandling, steg for steg."),
    "barneklipp": ("barneklipp-forste-gang-tips", "Barneklipp første gang: 7 tips fra barbereren",
                   "Slik forbereder du barnet, velger tidspunkt og gjør første klipp til en god opplevelse."),
    "kombo": ("hva-koster-herreklipp-og-skin-fade", "Hva koster herreklipp og skin fade i 2026? Prisguide for Follo, Bærum og Romerike",
              "Hva som er vanlig pris, hvorfor nivået på barbereren påvirker den, og hva som inngår."),
}

# Hovedbehandlingen (Fixit-navn i Priser-samlingen) som viser "prisen" for tjenesten per avdeling.
HOVED_BEHANDLING = {
    "herreklipp": "Klassisk herreklipp",
    "skin-fade": "Skin fade",
    "skjeggtrim": "Skjeggtrim",
    "barbering": "Barbering av skjegget med kniv",
    "barneklipp": "Barneklipp klassisk (under 12 år)",
    "kombo": "Kombo I: klassisk herreklipp og skjeggtrim eller knivbarbering",
}

KATEGORI_REKKEFOLGE = ["Hårklipp", "Re-fresh", "Kombo", "Skjegg", "Barbering", "Deluxe", "Voksing"]


def _clean(obj):
    """Fjerner tankestreker rekursivt i alle strenger."""
    if isinstance(obj, str):
        return fix_dashes(obj)
    if isinstance(obj, list):
        return [_clean(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    return obj


def load() -> dict:
    raw = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    raw = _clean(raw)

    avdelinger = sorted((a["data"] for a in raw["avdelinger"]), key=lambda x: x["rekkefolge"])
    for a in avdelinger:
        s = a["slug"]
        a["url"] = f"/avdelinger/{s}/"
        a["nabo"] = raw["naboer"].get(s, [])
        a["rating"], a["antall"] = GOOGLE.get(s, (SITE["snitt"], 0))
        a["reviewsUrl"] = a.get("reviewsUrl") or (
            "https://www.google.com/maps/search/?api=1&query=" +
            ("J%26K+Barber+Shop+" + a["title"].replace(" ", "+").replace("&", "%26").replace("Å", "%C3%85").replace("ø", "%C3%B8").replace("å", "%C3%A5"))
        )
        a["bloggSlug"], a["bloggTittel"], a["bloggIngress"] = BLOGG_AVD[s]
        if len(a["seoTittel"]) > 60:
            a["seoTittel"] = a["seoTittel"].replace(" | J&K Barber Shop", " | J&K")
        if len(a["seoBeskrivelse"]) > 160:
            a["seoBeskrivelse"] = SEO_BESKRIVELSE_KORT.get(s, a["seoBeskrivelse"])
        a["apningstider"] = [
            ("Mandag", a.get("apentMan", "")), ("Tirsdag", a.get("apentTir", "")), ("Onsdag", a.get("apentOns", "")),
            ("Torsdag", a.get("apentTor", "")), ("Fredag", a.get("apentFre", "")), ("Lørdag", a.get("apentLor", "")),
            ("Søndag", a.get("apentSon", "Stengt")),
        ]
    avd = {a["slug"]: a for a in avdelinger}

    tjenester = sorted((t["data"] for t in raw["tjenester"]), key=lambda x: x["rekkefolge"])
    for t in tjenester:
        s = t["slug"]
        t["url"] = f"/tjenester/{s}/"
        t["bloggSlug"], t["bloggTittel"], t["bloggIngress"] = BLOGG_TJ[s]
        t["hovedBehandling"] = HOVED_BEHANDLING[s]
        t["relaterte"] = [x for x in (t.get("relaterteSlugs") or "").split(",") if x]
    tj = {t["slug"]: t for t in tjenester}

    priser = [p["data"] for p in raw["priser"]]
    priser.sort(key=lambda p: (p.get("rekkefolge", 0), p.get("niva", "")))

    faq = []
    for f in raw["faq"]:
        d = f["data"]
        d["sporsmal"] = d["title"]
        d["svarTekst"] = strip_tags(d["svar"])
        faq.append(d)
    faq.sort(key=lambda f: f.get("rekkefolge", 0))

    avd_order = [a["slug"] for a in avdelinger]

    def hovedpriser(slug, niva="Barber"):
        return [p for p in priser if p["avdelingSlug"] == slug and p.get("hovedpris") and p["niva"] == niva]

    def pris(tjeneste_slug, avd_slug, behandling=None, niva="Barber"):
        navn = behandling or HOVED_BEHANDLING[tjeneste_slug]
        for p in priser:
            if p["avdelingSlug"] == avd_slug and p["niva"] == niva and p["behandling"] == navn:
                return p
        return None

    def priser_tjeneste(tjeneste_slug, niva="Barber"):
        """Rader for en tjeneste: [(behandling, varighet, {avd_slug: pris|None})], hovedbehandling først."""
        rows, seen = [], {}
        for p in priser:
            if p.get("tjenesteSlug") != tjeneste_slug or p["niva"] != niva:
                continue
            key = p["behandling"]
            if key not in seen:
                seen[key] = {"behandling": key, "varighet": p.get("varighetMin"), "kategori": p.get("kategori"),
                             "rekkefolge": p.get("rekkefolge", 0), "priser": {}}
                rows.append(seen[key])
            seen[key]["priser"][p["avdelingSlug"]] = p["pris"]
        hoved = HOVED_BEHANDLING[tjeneste_slug]
        rows.sort(key=lambda r: (0 if r["behandling"] == hoved else 1, r["rekkefolge"]))
        return rows

    def priser_kategori(niva="Barber"):
        """Alle behandlinger gruppert: [(kategori, [rad, ...])] i fast rekkefølge."""
        grupper = {}
        for p in priser:
            if p["niva"] != niva:
                continue
            g = grupper.setdefault(p["kategori"], {})
            r = g.setdefault(p["behandling"], {"behandling": p["behandling"], "varighet": p.get("varighetMin"),
                                               "tjenesteSlug": p.get("tjenesteSlug"), "rekkefolge": p.get("rekkefolge", 0),
                                               "priser": {}})
            r["priser"][p["avdelingSlug"]] = p["pris"]
        out = []
        for k in KATEGORI_REKKEFOLGE:
            if k in grupper:
                out.append((k, sorted(grupper[k].values(), key=lambda r: r["rekkefolge"])))
        return out

    def faq_for(sted, slug=None):
        """sted: 'forside' | 'avdeling' | 'tjeneste' | 'app' | 'gavekort'.
        Med slug: generelle (uten avdeling/tjeneste) + spesifikke for slug. 'Klipper dere bare menn?' først."""
        gen, spes = [], []
        for f in faq:
            if sted not in (f.get("visPa") or []):
                continue
            key = f.get("avdelingSlug") or f.get("tjenesteSlug")
            if key is None:
                gen.append(f)
            elif slug and key == slug:
                spes.append(f)
        items = spes + gen if slug else gen
        items.sort(key=lambda f: 0 if f["sporsmal"].startswith("Klipper dere bare menn") else 1)
        return items

    def nabo_avdelinger(slug):
        return [avd[s] for s in avd[slug]["nabo"] if s in avd]

    return {
        "site": SITE,
        "merker": MERKER,
        "avdelinger": avdelinger,
        "avd": avd,
        "avd_order": avd_order,
        "tjenester": tjenester,
        "tj": tj,
        "priser": priser,
        "faq": faq,
        "fn": {
            "hovedpriser": hovedpriser,
            "pris": pris,
            "priser_tjeneste": priser_tjeneste,
            "priser_kategori": priser_kategori,
            "faq_for": faq_for,
            "nabo_avdelinger": nabo_avdelinger,
        },
    }

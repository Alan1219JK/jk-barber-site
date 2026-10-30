"""/avdelinger/ (oversikt) og de sju avdelingssidene /avdelinger/<slug>/.

Innhold: data.json (Avdelinger, Priser, Faq), designskisse Avdeling.dc.html, innholdsplan del 4,
anmeldelser fra lib/anmeldelser.py.
"""
from lib import layout as L
from lib import images as IM
from lib.anmeldelser import for_avdeling
from lib.util import e, tid, tid_schema, kr, nb_num
from pages.forside import avd_kort

DAGER_EN = {"Mandag": "Monday", "Tirsdag": "Tuesday", "Onsdag": "Wednesday", "Torsdag": "Thursday",
            "Fredag": "Friday", "Lørdag": "Saturday", "Søndag": "Sunday"}

# Reisetid til naboavdelinger (innholdsplan del 4, "Andre avdelinger i nærheten").
NABO_NOTAT = {
    ("sandvika", "rykkinn"): "12 minutter med bil",
    ("ski", "asenveien"): "5 minutters gange",
    ("ski", "kolbotn"): "10 minutter med tog",
    ("asenveien", "ski"): "5 minutters gange",
    ("kolbotn", "ski"): "10 minutter med tog",
    ("jessheim", "strommen"): "25 minutter med bil eller tog",
    ("strommen", "jessheim"): "25 minutter",
    ("rykkinn", "sandvika"): "12 minutter med bil",
}

CTA = {
    "sandvika": ("Klar for en klipp som sitter?", "Bestill time i Sandvika Storsenter på under ett minutt. Du velger barberer, tidspunkt og behandling selv."),
    "ski": ("Time i Ski Storsenter?", "Velg barberer og tidspunkt, og bestill på under ett minutt."),
    "asenveien": ("Vil du ha ro i stolen?", "Bestill time i Åsenveien 3 og parker gratis rett utenfor."),
    "kolbotn": ("Klar for en klipp på Kolbotn?", "Bestill time, velg barberer og parker gratis i 2 timer."),
    "jessheim": ("Jessheims barbershop.", "Bestill time, velg barberer, og få klippen du har sett etter."),
    "strommen": ("Barbershop midt i Strømmen Storsenter.", "Bestill time, velg barberer og kombiner med handleturen."),
    "rykkinn": ("Bærum vests egen barbershop.", "Bestill time på Rykkinn Senter."),
}

# Galleri per avdeling: (avtalt filnavn, motiv). Filnavn fra innholdsplan del 4 / 10.2.
GALLERI = {
    "sandvika": [("jk-barber-sandvika-fasade.jpg", "Inngangen til salongen i Sandvika Storsenter"),
                 ("jk-barber-sandvika-interior.jpg", "Interiør, Sandvika"),
                 ("jk-barber-sandvika-skin-fade.jpg", "Skin fade, resultat"),
                 ("jk-barber-sandvika-skjeggtrim.jpg", "Skjeggtrim"),
                 ("jk-barber-sandvika-herreklipp-slickback.jpg", "Klassisk herreklipp, slickback"),
                 ("jk-barber-sandvika-barneklipp.jpg", "Barneklipp")],
    "ski": [("jk-barber-ski-fasade.jpg", "Fasaden på brugangen i Ski Storsenter"),
            ("jk-barber-ski-interior.jpg", "Interiør, Ski Storsenter"),
            ("jk-barber-ski-skin-fade.jpg", "Skin fade, resultat"),
            ("jk-barber-ski-skjeggtrim.jpg", "Skjeggtrim"),
            ("jk-barber-ski-herreklipp.jpg", "Klassisk herreklipp"),
            ("jk-barber-ski-brua.jpg", "Brugangen mot Telia")],
    "asenveien": [("jk-barber-asenveien-fasade.jpg", "Fasaden i Åsenveien 3"),
                  ("jk-barber-asenveien-interior.jpg", "Interiør, Åsenveien 3"),
                  ("jk-barber-asenveien-knivbarbering.jpg", "Knivbarbering"),
                  ("jk-barber-asenveien-skin-fade.jpg", "Skin fade, resultat"),
                  ("jk-barber-asenveien-parkering.jpg", "Parkering rett utenfor døren")],
    "kolbotn": [("jk-barber-kolbotn-fasade.jpg", "Fasaden ved Vinmonopolet, Kolbotn Torg"),
                ("jk-barber-kolbotn-interior.jpg", "Interiør, Kolbotn Torg"),
                ("jk-barber-kolbotn-skin-fade.jpg", "Skin fade, resultat"),
                ("jk-barber-kolbotn-barneklipp.jpg", "Barneklipp"),
                ("jk-barber-kolbotn-skjeggtrim.jpg", "Skjeggtrim"),
                ("jk-barber-kolbotn-stasjon.jpg", "Kolbotn stasjon, to minutter unna")],
    "jessheim": [("jk-barber-jessheim-fasade.jpg", "Fasaden mot Lindex, Jessheim Storsenter"),
                 ("jk-barber-jessheim-interior-neon.jpg", "Interiør, Jessheim"),
                 ("jk-barber-jessheim-skin-fade.jpg", "Skin fade, resultat"),
                 ("jk-barber-jessheim-skjeggtrim.jpg", "Skjeggtrim"),
                 ("jk-barber-jessheim-herreklipp.jpg", "Klassisk herreklipp")],
    "strommen": [("jk-barber-strommen-fasade.jpg", "Fasaden mellom Fransa og Gullfunn, Strømmen Storsenter"),
                 ("jk-barber-strommen-interior.jpg", "Interiør, Strømmen"),
                 ("jk-barber-strommen-skin-fade.jpg", "Skin fade, resultat"),
                 ("jk-barber-strommen-knivbarbering.jpg", "Knivbarbering"),
                 ("jk-barber-strommen-herreklipp.jpg", "Klassisk herreklipp")],
    "rykkinn": [("jk-barber-rykkinn-fasade.jpg", "Fasaden på Rykkinn Senter"),
                ("jk-barber-rykkinn-interior.jpg", "Interiør, Rykkinn"),
                ("jk-barber-rykkinn-barneklipp.jpg", "Barneklipp"),
                ("jk-barber-rykkinn-skin-fade.jpg", "Skin fade, resultat")],
}

HERO_BILDE = {
    "sandvika": ("jk-barber-sandvika-interior.jpg", "Interiøret i J&K Barber Shop Sandvika Storsenter"),
    "ski": ("jk-barber-ski-fasade.jpg", "Fasaden til J&K Barber Shop på brugangen i Ski Storsenter"),
    "asenveien": ("jk-barber-asenveien-fasade.jpg", "J&K Barber Shop i Åsenveien 3, Ski"),
    "kolbotn": ("jk-barber-kolbotn-interior.jpg", "Interiøret i J&K Barber Shop Kolbotn Torg"),
    "jessheim": ("jk-barber-jessheim-fasade.jpg", "Inngangen til J&K Barber Shop i Jessheim Storsenter"),
    "strommen": ("jk-barber-strommen-fasade.jpg", "Inngangen til J&K Barber Shop i Strømmen Storsenter"),
    "rykkinn": ("jk-barber-rykkinn-fasade.jpg", "J&K Barber Shop på Rykkinn Senter"),
}

SENIOR_PASLAG = {"Hårklipp": 50, "Skjegg": 70, "Barbering": 50, "Kombo": 100, "Deluxe": 100, "Re-fresh": 50, "Voksing": 0}


def sted(a):
    """'i Sandvika Storsenter' / 'på Kolbotn Torg' (fra H1)."""
    return a["h1"].split("herrefrisør ", 1)[1] if "herrefrisør " in a["h1"] else "i " + a["title"]


def grupper_tider(a):
    """[('Mandag til fredag', '10 til 21'), ('Lørdag', '9 til 19'), ('Søndag', 'Stengt')]."""
    out = []
    for dag, t in a["apningstider"]:
        if out and out[-1][2] == t:
            out[-1][1] = dag
        else:
            out.append([dag, dag, t])
    res = []
    for start, slutt, t in out:
        navn = start if start == slutt else f"{start} til {slutt.lower()}"
        res.append((navn, tid(t) if t != "Stengt" else "Stengt"))
    return res


def hours_jsonld(a):
    spec, grupper = [], {}
    for dag, t in a["apningstider"]:
        tt = tid_schema(t)
        if not tt:
            continue
        grupper.setdefault(tt, []).append(DAGER_EN[dag])
    for (o, c), dager in grupper.items():
        spec.append({"@type": "OpeningHoursSpecification", "dayOfWeek": dager if len(dager) > 1 else dager[0],
                     "opens": o, "closes": c})
    return spec


def barbershop_jsonld(ctx, a, hovedpriser):
    s, base = ctx["site"], ctx["site"]["base"]
    fn = ctx["fn"]
    offers = []
    for p in hovedpriser:
        senior = fn["pris"](p.get("tjenesteSlug") or "herreklipp", a["slug"], behandling=p["behandling"], niva="Senior")
        maxp = senior["pris"] if senior else p["pris"] + SENIOR_PASLAG.get(p["kategori"], 50)
        url = base + (ctx["tj"][p["tjenesteSlug"]]["url"] if p.get("tjenesteSlug") in ctx["tj"] else "/tjenester/")
        offers.append({
            "@type": "Offer",
            "itemOffered": {"@type": "Service", "name": p["behandling"], "url": url},
            "priceSpecification": {"@type": "PriceSpecification", "minPrice": str(p["pris"]), "maxPrice": str(maxp),
                                   "priceCurrency": "NOK",
                                   "description": f"{p['pris']} kr for nivå Barber, {maxp} kr for nivå Senior"},
        })
    bilder = [IM.url(n, 1200, 800) for n, _ in GALLERI[a["slug"]] if IM.has(n)]
    plass = a["plassering"].split(".")[0]
    d = {
        "@context": "https://schema.org",
        "@type": "BarberShop",
        "@id": base + a["url"] + "#barbershop",
        "name": f"J&K Barber Shop {a['title']}",
        "description": a["seoBeskrivelse"],
        "url": base + a["url"],
        "image": bilder or [IM.LOGO_SCHEMA],
        "logo": IM.LOGO_SCHEMA,
        "telephone": s["telefon"],
        "email": s["epost"],
        "priceRange": "kr 300-1800",
        "currenciesAccepted": "NOK",
        "paymentAccepted": "Kort, Vipps",
        "address": {"@type": "PostalAddress",
                    "streetAddress": f"{a['gateadresse']}" + (f", {a['senter']}, {plass}" if a.get("senter") else ""),
                    "postalCode": a["postnummer"], "addressLocality": a["poststed"],
                    "addressRegion": "Akershus", "addressCountry": "NO"},
        "hasMap": a["mapsUrl"],
        "openingHoursSpecification": hours_jsonld(a),
        "sameAs": [a["fixitUrl"], s["instagram"], s["facebook"]],
        "parentOrganization": {"@id": base + "/#organization"},
        "foundingDate": str(a.get("apnet", "")),
        "knowsLanguage": ["nb", "en"],
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": "Parkering", "value": True},
            {"@type": "LocationFeatureSpecification", "name": "Barnevennlig", "value": True},
        ],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": f"Tjenester hos J&K Barber Shop {a['title']}", "itemListElement": offers},
        "potentialAction": {"@type": "ReserveAction",
                            "target": {"@type": "EntryPoint", "urlTemplate": a["fixitUrl"], "inLanguage": "nb-NO",
                                       "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]},
                            "result": {"@type": "Reservation", "name": f"Time hos J&K Barber Shop {a['title']}"}},
    }
    if a.get("lat") and a.get("lng"):
        d["geo"] = {"@type": "GeoCoordinates", "latitude": a["lat"], "longitude": a["lng"]}
    return d


def render_avdeling(ctx, a):
    s, fn = ctx["site"], ctx["fn"]
    slug = a["slug"]
    hoved = fn["hovedpriser"](slug)
    # Rekkefølge som i innholdsplanen: klipp, skin fade, skjegg, barbering, barneklipp x2, kombo x2, pensjonist
    onsket = ["Klassisk herreklipp", "Skin fade", "Skjeggtrim", "Barbering av skjegget med kniv",
              "Barneklipp klassisk (under 12 år)", "Barneklipp skin fade (under 12 år)",
              "Kombo I: klassisk herreklipp og skjeggtrim eller knivbarbering",
              "Kombo II: skin fade og skjeggtrim eller knivbarbering", "Pensjonistklipp"]
    hoved.sort(key=lambda p: onsket.index(p["behandling"]) if p["behandling"] in onsket else 99)

    hero_navn, hero_alt = HERO_BILDE[slug]
    hero_img = IM.picture(hero_navn, hero_alt, 900, 700, cls="hero-bilde", lazy=False, motiv=hero_alt)
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow(e(a["title"]) + ", " + e(a["kommune"]))}'
        f'<h1>{e(a["h1"])}</h1><p class="hero-ingress">{e(a["ingress"])} {s["regel0"].split(". ")[0]}.</p>'
        f'<div class="knapper">{L.btn(e(a["bestillKnapp"]), a["fixitUrl"], bestill=a["ga4Avdeling"], plassering="hero")}'
        f'{L.btn("Ring " + s["telefonVisning"], "tel:" + s["telefon"], "s", external=False)}'
        f'{L.btn("Veibeskrivelse", a["mapsUrl"], "s")}</div>'
        f'<p class="muted small">{L.stars()} {a["rating"]} av 5 på Google, {a["antall"]} anmeldelser</p></div>{hero_img}</div>',
        cls="sec-hero")

    tider = "".join(f'<div class="row"><span>{e(d)}</span><span{" class=\"muted\"" if t == "Stengt" else ""}>{e(t)}</span></div>' for d, t in grupper_tider(a))
    adresse_navn = f"J&amp;K Barber Shop {e(a['title'])}"
    nap = L.section(
        '<div class="grid grid-3 nap">'
        f'<div class="card kort-stor">{L.eyebrow("Her finner du oss")}<h2>Adresse</h2><p>{adresse_navn}<br>{e(a["gateadresse"])}, {e(a["postnummer"])} {e(a["poststed"])}<br>{e(a["plassering"])}</p>'
        f'<p>{e(a["parkering"])} {e(a["kollektiv"])}</p>'
        f'<p>Tlf <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a> (felles for alle avdelinger)<br><a href="mailto:{s["epost"]}">{s["epost"]}</a></p></div>'
        f'<div class="card kort-stor">{L.eyebrow("Åpningstider")}<h2>Vi har åpent</h2><div class="rows">{tider}</div>'
        f'<p class="muted small">Åpningstidene følger senteret. Avvikende tider i høytider vises i bookingen og på Google.</p></div>'
        f'<div class="kart"><div class="ph kart-ph" role="img" aria-label="Kart til {e(a["gateadresse"])}, {e(a["poststed"])}"><span>Google Maps-kart med markør: {e(a["gateadresse"])}, {e(a["postnummer"])} {e(a["poststed"])}</span></div>'
        f'<a class="btn btn-s btn-sm" href="{e(a["mapsUrl"])}" target="_blank" rel="noopener">Åpne i Google Maps</a></div>'
        '</div>', tone="flate", id_="her")

    rader = []
    for i, p in enumerate(hoved):
        href = ctx["tj"][p["tjenesteSlug"]]["url"] if p.get("tjenesteSlug") in ctx["tj"] else "/tjenester/"
        rader.append(L.pris_rad(p["behandling"], p["pris"], p.get("varighetMin"), href))
    rader.append('<div class="row row-last"><span class="muted">Re-fresh, deluxe, voksing og student: se hele listen</span><a href="/tjenester/">Alle priser</a></div>')
    priser = L.section(
        f'<div class="split split-start split-14"><div class="sec-head">{L.eyebrow("Tjenester og priser")}<h2>Priser {e(sted(a))}</h2>'
        f'<p class="lead muted">Prisene viser nivået Barber. {s["prisSetning"]} Hårvask inngår i klipp, du velger selv om du vil ha den. {s["regel0"].split(". ")[0]}.</p>'
        f'<a href="/tjenester/#nivaer">Slik fungerer nivåene Lærling, Junior, Barber og Senior</a></div>'
        f'<div class="card pristabell-kort">{"".join(rader)}</div></div>', id_="priser")

    velg = L.section(
        f'<div class="rad-mellom"><div class="sec-head">{L.eyebrow("Barbererne")}<h2>Velg barberer selv</h2>'
        f'<p class="lead muted">Barbererne {e(sted(a))} er synlige i onlinebookingen. Der ser du nivået deres (Lærling, Junior, Barber, Senior), prisen og ledige tider. Velg den du vil ha, eller første ledige. Avbestilling senest 24 timer før.</p></div>'
        f'{L.btn("Se barbererne og bestill", a["fixitUrl"], bestill=a["ga4Avdeling"], plassering="velg-barberer")}</div>',
        tone="mork")

    bilder = "".join(IM.picture(n, m, 600, 600, cls="galleri-bilde", motiv=m) for n, m in GALLERI[slug])
    anm = "".join(L.review_card(t, f"{n}, {m}") for t, n, m in for_avdeling(slug))
    galleri = L.section(
        f'<h2>Fra stolen {e(sted(a))}</h2><div class="galleri">{bilder}</div>'
        f'<div class="sec-head-rad"><h2>Det kundene {e(sted(a))} sier</h2><a href="{e(a["reviewsUrl"])}" target="_blank" rel="noopener">Les alle {a["antall"]} anmeldelser på Google</a></div>'
        f'<div class="grid grid-3">{anm}</div>', id_="galleri")

    faq_items, sett = [], set()
    for f in fn["faq_for"]("avdeling", slug):
        if f["sporsmal"] in sett:
            continue
        sett.add(f["sporsmal"])
        faq_items.append(f)
    om = L.section(
        f'<div class="split split-start"><div class="prosa"><h2>Om J&amp;K Barber Shop {e(sted(a))}</h2>{a["beskrivelse"]}</div>'
        + L.faq_block(faq_items, heading_text=f"Spørsmål om {e(a['kortnavn'])}", eye="", side=False, id_="faq") + "</div>",
        tone="flate", id_="om")

    cta_t, cta_x = CTA[slug]
    blogg_img = IM.picture(f"jk-barber-{slug}-blogg.jpg", a["bloggTittel"], 500, 360, cls="blogg-bilde",
                           motiv=f"Bilde til guiden om {a['title']}")
    andre = []
    for n in fn["nabo_avdelinger"](slug):
        note = NABO_NOTAT.get((slug, n["slug"]))
        andre.append(f'<a href="{n["url"]}">{e(n["title"])}</a>' + (f" ({note})" if note else ""))
    for x in ctx["avdelinger"]:
        if x["slug"] != slug and x["slug"] not in a["nabo"]:
            andre.append(f'<a href="{x["url"]}">{e(x["title"])}</a>')
    andre.append('<a href="/avdelinger/">Alle avdelinger</a>')
    bunn = L.section(
        L.cta_box(e(cta_t), e(cta_x), L.btn(e(a["bestillKnapp"]), a["fixitUrl"], bestill=a["ga4Avdeling"], plassering="cta-bunn"))
        + f'<article class="card blogg-bred">{blogg_img}<div class="kort-innhold">{L.eyebrow("Guide", muted=True)}<h2><a href="/post/{a["bloggSlug"]}/">{e(a["bloggTittel"])}</a></h2>'
        f'<p class="muted">{e(a["bloggIngress"])}</p><a href="/post/{a["bloggSlug"]}/">Les guiden</a></div></article>'
        f'<p class="muted small andre-avd">Våre andre avdelinger: {" · ".join(andre)}</p>'
        f'<p class="muted small">Tjenester {e(sted(a))}: ' + " · ".join(f'<a href="{t["url"]}">{e(t["title"])}</a>' for t in ctx["tjenester"]) + "</p>",
        id_="bestill")

    body = hero + nap + priser + velg + galleri + om + bunn
    crumbs = [("Avdelinger", "/avdelinger/"), (a["title"], None)]
    og_img = IM.url(hero_navn, 1200, 630)
    return L.page(ctx, path=a["url"], title=a["seoTittel"], description=a["seoBeskrivelse"], body=body,
                  breadcrumbs=crumbs, jsonld=[barbershop_jsonld(ctx, a, hoved), L.faq_jsonld(faq_items)],
                  active="avdelinger", bestill_url=a["fixitUrl"], avdeling=a["ga4Avdeling"], og_image=og_img)


def render_oversikt(ctx):
    s = ctx["site"]
    kort = "".join(avd_kort(ctx, a, extra=f'<p class="small">{e(a["oversiktTekst"])}</p>') for a in ctx["avdelinger"])
    hero = L.section(
        f'<div class="sec-head sec-head-stor">{L.eyebrow("Sju avdelinger")}<h1>Finn din barbershop</h1>'
        '<p class="lead muted">Sju avdelinger i Follo, Bærum og Romerike, alle med samme standard og samme stempelkort. Prisene varierer litt mellom avdelingene, du ser dem på hver avdelingsside. Velg den som ligger nærmest, se åpningstider og bestill time direkte.</p></div>'
        '<div class="ph kart-alle" role="img" aria-label="Kart med alle sju avdelinger"><span>Google Maps med alle sju avdelinger (Sandvika, Ski Storsenter, Åsenveien 3, Kolbotn, Jessheim, Strømmen, Rykkinn)</span></div>',
        cls="sec-hero")
    liste = L.section(f'<div class="grid grid-3">{kort}</div>'
                      f'<p class="muted small">Felles telefon for alle avdelinger: <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a>. Åpningstider følger senteret.</p>')
    samme = L.section(
        L.heading("Samme kvalitet overalt",
                  "Uansett hvilken avdeling du velger, får du barberere med tydelig nivå, konsultasjon før klippen, de samme produktene i hyllene og stempelkort som gjelder på tvers. Har du en favorittbarberer, finner du vedkommende i bookingen for den avdelingen han eller hun jobber i.")
        + f'<p class="muted">{s["regel0"]}</p>'
        + L.cta_box("Bestill time", "Velg avdeling, barberer og tidspunkt. Det tar under ett minutt.",
                    L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering="avdelinger-cta")),
        tone="flate")
    body = hero + liste + samme
    items = [{"@type": "ListItem", "position": i + 1, "name": f"J&K Barber Shop {a['title']}", "url": s["base"] + a["url"]}
             for i, a in enumerate(ctx["avdelinger"])]
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Avdelinger, J&K Barber Shop", "itemListElement": items}
    return L.page(ctx, path="/avdelinger/", title="Våre avdelinger: Sandvika, Ski, Kolbotn | J&K",
                  description="Finn din nærmeste J&K Barber Shop. Adresser, åpningstider, parkering og direkte timebestilling for alle sju avdelinger i Follo, Bærum og Romerike.",
                  body=body, breadcrumbs=[("Avdelinger", None)], jsonld=[ld], active="avdelinger")


def render(ctx):
    out = {"/avdelinger/": render_oversikt(ctx)}
    for a in ctx["avdelinger"]:
        out[a["url"]] = render_avdeling(ctx, a)
    return out

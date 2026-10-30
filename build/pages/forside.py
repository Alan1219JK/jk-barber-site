"""Forsiden (/). Tekster fra design/Main.dc.html og ForsideMobil.dc.html (godkjent 29. okt 2026)."""
from lib import layout as L
from lib import images as IM
from lib.anmeldelser import GENERELLE
from lib.util import e, tid, nb_num

TITLE = "Barbershop og herrefrisør i Akershus | J&K Barber Shop"
DESC = ("Barbershop og herrefrisør med 7 avdelinger i Sandvika, Ski, Kolbotn, Jessheim og Strømmen. "
        "Herreklipp, skin fade, skjeggtrim og barbering. Bestill time.")

HVORFOR = [
    ("For både menn og kvinner", "Alle behandlingene på menyen er for både menn og kvinner. Vil du ha kort hår, skin fade eller en skikkelig herreklipp, er du velkommen uansett kjønn."),
    ("Barberere, ikke tilfeldige hender", "Vi rekrutterer folk som kan faget og trener dem videre på skin fade, skjegg og kniv. Du ser nivået til hver barberer før du bestiller."),
    ("Konsultasjon først, alltid", "Ingen klipp starter før vi har snakket om hva du vil ha. Har du bilde, vis det. Har du ikke, hjelper vi deg."),
    ("J&amp;K-familien siden 2018", "Første avdeling åpnet i Åsenveien 3 i Ski i 2018. Navnet kommer fra eierens barn, Jan og Kevin, og barbershopene er det tredje barnet. I dag er vi rundt 15 barberere på sju steder."),
    ("Et fristed uten hastverk", "Mørkt interiør, messing, god kaffe og tid nok. Du skal ut av stolen med senkede skuldre."),
    ("Enkelt å komme tilbake", "Sju avdelinger, booking på nett og i appen, stempelkort som gir deg hver 10. behandling gratis."),
]

GUIDER = [
    ("barbershop-sandvika-storsenter", "Guider", "Barbershop i Sandvika Storsenter: slik finner du J&amp;K i Kjørbokollen",
     "Inngang, parkering og hva du kan bestille hos barbereren ved Cewe Japan Photo.",
     "jk-barber-sandvika-blogg-kjorbokollen.jpg", "J&K i Kjørbokollen, Sandvika Storsenter"),
    ("hva-koster-herreklipp-og-skin-fade", "Guider", "Hva koster herreklipp og skin fade i 2026? Prisguide for Follo, Bærum og Romerike",
     "Hva som er vanlig pris, hvorfor nivået på barbereren påvirker den, og hva som inngår.",
     "jk-barber-felles-blogg-prisguide.jpg", "Prisliste og saks på benken"),
    ("herreklipp-for-kvinner", "Hår og styling", "Herreklipp for kvinner: kort hår, pixie og skin fade hos barberer",
     "Alle behandlingene på menyen er for både menn og kvinner. Slik bestiller du, og hva du kan forvente.",
     "jk-barber-felles-blogg-herreklipp-for-kvinner.jpg", "Kvinne med kort pixie-klipp i stolen"),
]

AVD_BILDE = {
    "sandvika": "jk-barber-sandvika-interior.jpg",
    "ski": "jk-barber-ski-fasade.jpg",
    "asenveien": "jk-barber-asenveien-fasade.jpg",
    "kolbotn": "jk-barber-kolbotn-interior.jpg",
    "jessheim": "jk-barber-jessheim-fasade.jpg",
    "strommen": "jk-barber-strommen-fasade.jpg",
    "rykkinn": "jk-barber-rykkinn-fasade.jpg",
}

TJ_BILDE = {
    "herreklipp": ("jk-barber-sandvika-herreklipp-teksturert.jpg", "Klassisk herreklipp, resultat"),
    "skin-fade": ("jk-barber-sandvika-skin-fade.jpg", "Skin fade, resultat"),
    "skjeggtrim": ("jk-barber-sandvika-skjeggtrim.jpg", "Skjeggtrim med kniv"),
    "barbering": ("jk-barber-sandvika-barbering.jpg", "Knivbarbering, varmt håndkle"),
    "barneklipp": ("jk-barber-felles-barneklipp.jpg", "Barneklipp"),
    "kombo": ("jk-barber-felles-barberer-med-kunde.jpg", "Kombo: klipp og skjegg"),
}


def apningstider_kort(a):
    """Kort åpningstidslinje som i designet: 'Man til fre 10 til 21, lør 9 til 19'."""
    man, fre, lor = a["apentMan"], a["apentFre"], a["apentLor"]
    if man == fre:
        s = f"Man til fre {tid(man)}"
    else:
        s = f"Man til tor {tid(man)}, fre {tid(fre)}"
    return f"{s}, lør {tid(lor)}"


def avd_kort(ctx, a, with_img=True, extra=""):
    img = ""
    if with_img:
        img = IM.picture(AVD_BILDE[a["slug"]], f"J&K Barber Shop {a['title']}", 600, 340, cls="kort-bilde",
                         motiv=f"Fasade {a['title']}")
    plass = a["plassering"].split(". Følg")[0].rstrip(".")
    tekst = f"{e(a['gateadresse'])}, {e(a['postnummer'])} {e(a['poststed'])}. {e(plass)}. {e(a['parkering'].split('. ')[-1] if 'gratis' in a['parkering'] else a['parkering'])}"
    return (f'<article class="card avd-kort">{img}<div class="kort-innhold">'
            f'<h3>{e(a["title"] if a["slug"] != "asenveien" else "Åsenveien 3, Ski sentrum")}</h3>'
            f'<p class="muted small">{tekst}<br>{apningstider_kort(a)}</p>{extra}'
            f'<div class="kort-handling">{L.btn("Bestill time", a["fixitUrl"], size="sm", bestill=a["ga4Avdeling"], plassering="forside-kort")}'
            f'<a href="{a["url"]}">Om avdelingen</a></div></div></article>')


def render(ctx):
    s = ctx["site"]
    fn = ctx["fn"]

    hero_img = IM.url("jk-barber-felles-hero-klipp-i-stol.jpg", 1800, 1000)
    hero_style = f' style="background-image:url({hero_img})"' if hero_img else ""
    hero = f"""<section class="hero hero-forside"{hero_style}>
  <div class="hero-overlay"></div>
  <div class="wrap hero-inner">
    {L.eyebrow("Barbershop og herrefrisør siden 2018")}
    <h1>Barbershop og herrefrisør i Follo, Bærum og Romerike</h1>
    <p class="hero-ingress">Sju avdelinger og rundt 15 barberere som kan skin fade, skjegg og klassisk klipp. {s["regel0"]}</p>
    <div class="knapper">{L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering="hero")}{L.btn("Finn din barbershop", "/avdelinger/", "s")}</div>
    <div class="tillit muted"><span>{L.stars()} {s["anmeldelser"]}</span><span>Snitt {s["snitt"]} av 5</span><span>Timebestilling på nett og i appen</span></div>
  </div>
</section>"""

    avd = L.section(
        L.heading("Finn din barbershop",
                  "Alle avdelingene våre ligger der du likevel er: i senteret, ved stasjonen, med parkering. Velg din, se åpningstider og bestill time direkte.",
                  "Sju avdelinger")
        + '<div class="grid grid-3">' + "".join(avd_kort(ctx, a) for a in ctx["avdelinger"]) + "</div>"
        + f'<p class="muted small">Felles telefon for alle avdelinger: <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a>. Åpningstider følger senteret. <a href="/avdelinger/">Se alle avdelinger med kart</a></p>',
        id_="avdelinger")

    tj_kort = []
    for t in ctx["tjenester"]:
        navn, motiv = TJ_BILDE[t["slug"]]
        img = IM.picture(navn, t["title"], 600, 300, cls="kort-bilde", motiv=motiv)
        tj_kort.append(f'<article class="card tj-kort">{img}<div class="kort-innhold"><h3><a href="{t["url"]}">{e(t["title"])}</a></h3>'
                       f'<p class="muted">{e(t["ingress"])}</p><div class="kort-bunn"><span class="pris">{nb_num(t["fraPris"])} til {nb_num(t["tilPris"])} kr</span>'
                       f'<a href="{t["url"]}">Les mer om {e(t["title"].split(":")[0].lower())}</a></div></div></article>')
    tjenester = L.section(
        '<div class="sec-head-rad">' + L.heading("Det vi gjør best",
                  "Alt starter med en kort prat i stolen: hva du vil ha, hva som passer hodeformen og håret ditt, og hvordan du vil ha det om tre uker. Så gjør vi jobben.",
                  "Tjenester") + L.btn("Alle priser", "/tjenester/", "s") + "</div>"
        + '<div class="grid grid-3">' + "".join(tj_kort) + "</div>"
        + f'<p class="muted small">Prisene viser nivået Barber. {s["prisSetning"]} Hårvask inngår i klipp, du velger selv om du vil ha den.</p>',
        tone="flate", id_="tjenester")

    niva_kort = "".join(
        f'<div class="card niva-kort{" niva-senior" if i == 3 else ""}">{L.eyebrow(f"Nivå {i + 1}", muted=(i != 3))}<h3>{n}</h3><p class="muted">{t}</p></div>'
        for i, (n, t) in enumerate(s["nivaer"]))
    priser = L.section(
        '<div class="split split-start"><div class="sec-head">' + L.eyebrow("Slik fungerer prisene") +
        '<h2>Du velger barberer. Prisen følger nivået.</h2>'
        f'<p class="lead muted">Prisene på siden gjelder nivået Barber. {s["prisSetning"]} Når du bestiller, velger du selv barberer og ser prisen før du bekrefter. Hårvask inngår i klipp, du velger selv om du vil ha den. Alle jobber etter samme standard, med samme produkter og samme konsultasjon først.</p>'
        + L.btn("Se alle priser og nivåer", "/tjenester/", "s") + '</div><div class="grid grid-2">' + niva_kort + "</div></div>",
        id_="priser")

    hvorfor = L.section(
        '<h2 class="h2-bred">Derfor velger folk i Follo, Bærum og Romerike oss</h2><div class="grid grid-3 grunner">'
        + "".join(f'<div class="grunn"><h3>{h}</h3><p class="muted">{t}</p></div>' for h, t in HVORFOR) + "</div>",
        tone="mork")

    anm = L.section(
        '<div class="sec-head-rad">' + L.heading("Det kundene sier", "", "Google-anmeldelser")
        + f'<a href="/avdelinger/">Les anmeldelser per avdeling på Google</a></div>'
        + '<div class="grid grid-3">' + "".join(L.review_card(t, f"{n}, {m}") for t, n, m in GENERELLE) + "</div>"
        + f'<p class="muted small">{s["anmeldelser"]} med snitt {s["snitt"]} av 5 (summen av de sju Google-profilene).</p>',
        id_="anmeldelser")

    app_img = IM.picture("jk-barber-felles-app-stempelkort-mobil.jpg", "Mobil med stempelkortet i J&K-appen", 800, 700,
                         cls="app-bilde", motiv="Mobil med stempelkortet i J&K-appen")
    app = L.section(
        f'<div class="split split-center">{app_img}<div class="sec-head">' + L.eyebrow("J&amp;K-appen")
        + '<h2>Last ned appen og få hver 10. behandling gratis</h2>'
        '<p class="lead muted">Appen har fire stempelkort: klassisk klipp, skin fade, skjegg og kombo. Hvert 10. stempel gir deg behandlingen gratis. Barbereren registrerer stempelet i salongen etter hver behandling, så du trenger ikke gjøre noe annet enn å vise appen.</p>'
        '<div class="grid grid-4 stempel">' + "".join(f'<div class="card stempel-kort">{x}</div>' for x in ["Klassisk klipp", "Skin fade", "Skjegg", "Kombo"]) + "</div>"
        f'<div class="knapper">{L.btn("App Store", s["appStore"], "s", aria_label="Last ned J&K Barber Shop-appen på App Store")}{L.btn("Google Play", s["googlePlay"], "s", aria_label="Last ned J&K Barber Shop-appen på Google Play")}</div>'
        '<a href="/app/">Slik fungerer stempelkortet</a></div></div>',
        tone="flate", id_="app")

    merker = "".join(f'<a class="merke" href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in ctx["merker"])
    merker += f'<a class="merke merke-alle" href="{s["nettbutikk"]}" target="_blank" rel="noopener">Se alle på j-kshop.no</a>'
    produkter = L.section(
        L.heading("Produktene vi bruker og selger",
                  "Det vi bruker i stolen, kan du ta med hjem. Elleve merker står i hyllene i salongene, og barbereren viser deg gjerne hvordan du bruker dem. Hele utvalget finner du i nettbutikken vår, j-kshop.no.",
                  "Produkter")
        + f'<div class="merker">{merker}</div>'
        + f'<div class="knapper">{L.btn("Handle på j-kshop.no", s["nettbutikk"])}{L.btn("Se merkene vi fører", "/produkter/", "s")}</div>',
        id_="produkter")

    guide_kort = []
    for slug, kat, tittel, ing, bilde, motiv in GUIDER:
        img = IM.picture(bilde, motiv, 600, 340, cls="kort-bilde", motiv=motiv)
        guide_kort.append(f'<article class="card blogg-kort">{img}<div class="kort-innhold">{L.eyebrow(kat, muted=True)}'
                          f'<h3><a href="/post/{slug}/">{tittel}</a></h3><p class="muted">{ing}</p><a href="/post/{slug}/">Les guiden</a></div></article>')
    guider = L.section(
        '<div class="sec-head-rad">' + L.heading("Guider fra barbererne", "Det vi forklarer i stolen hver dag, skrevet ned. Priser, forskjellen på fadene, og hvordan du finner oss.", "Blogg")
        + L.btn("Se alle guider", "/blogg/", "s") + '</div><div class="grid grid-3">' + "".join(guide_kort) + "</div>",
        tone="flate", id_="guider")

    jobb = L.section(
        '<div class="grid grid-2">'
        '<div class="card kort-stor"><h2>Bli barberer hos J&amp;K Barber Shop</h2><p class="muted">Fast ansatt eller selvstendig med egen stol. Etablert kundegrunnlag, booking, app og kolleger som kan faget.</p><a href="/jobb/">Les om jobb hos oss</a></div>'
        '<div class="card kort-stor"><h2>Åpne din egen J&amp;K Barber Shop</h2><p class="muted">Vi vokser med franchise. Du får konseptet, innkjøpsavtalene, appen, bookingen og markedsføringen.</p><a href="/franchise/">Les om franchise</a></div>'
        '</div>', tone="mork")

    faq_items = fn["faq_for"]("forside")
    faq = L.section(L.faq_block(faq_items), id_="sporsmal")

    body = hero + avd + tjenester + priser + hvorfor + anm + app + produkter + guider + jobb + faq

    base = s["base"]
    org = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": base + "/#organization",
                "name": "J&K Barber Shop",
                "legalName": s["juridisk"],
                "url": base + "/",
                "logo": {"@type": "ImageObject", "url": IM.LOGO_SCHEMA, "width": 2270, "height": 2041},
                "image": hero_img or base + IM.LOGO,
                "description": "Barbershop og herrefrisør med sju avdelinger i Follo, Bærum og Romerike. Herreklipp, skin fade, skjeggtrim og knivbarbering siden 2018, for både menn og kvinner.",
                "foundingDate": "2018",
                "telephone": s["telefon"],
                "email": s["epost"],
                "vatID": "NO932372614MVA",
                "address": {"@type": "PostalAddress", "streetAddress": "Åsenveien 3", "postalCode": "1400",
                            "addressLocality": "Ski", "addressRegion": "Akershus", "addressCountry": "NO"},
                "areaServed": ["Bærum", "Nordre Follo", "Ullensaker", "Lillestrøm", "Akershus"],
                "sameAs": [s["instagram"], s["facebook"], s["appStore"], s["googlePlay"]],
                "contactPoint": {"@type": "ContactPoint", "telephone": s["telefon"], "contactType": "customer service",
                                 "availableLanguage": ["Norwegian", "English"]},
            },
            {
                "@type": "WebSite",
                "@id": base + "/#website",
                "url": base + "/",
                "name": "J&K Barber Shop",
                "inLanguage": "nb-NO",
                "publisher": {"@id": base + "/#organization"},
            },
        ],
    }
    html = L.page(ctx, path="/", title=TITLE, description=DESC, body=body,
                  jsonld=[org, L.faq_jsonld(faq_items)], active=None, body_class="forside")
    return {"/": html}

"""/tjenester/ (oversikt med pristabell per avdeling og nivåforklaring) og de seks tjenestesidene.

Innhold: data.json (Tjenester, Priser, Faq), designskisse Tjeneste.dc.html, innholdsplan del 5 og 6.1.
"""
import re

from lib import layout as L
from lib import images as IM
from lib.util import e, kr, nb_num, split_sentences, chunk_even

TJ_BILDE = {
    "herreklipp": ("jk-barber-sandvika-herreklipp-teksturert.jpg", "Klassisk herreklipp med teksturert topp"),
    "skin-fade": ("jk-barber-sandvika-skin-fade.jpg", "Skin fade, nærbilde av overgangen"),
    "skjeggtrim": ("jk-barber-sandvika-skjeggtrim.jpg", "Skjeggtrim med presisjon"),
    "barbering": ("jk-barber-sandvika-barbering.jpg", "Tradisjonell knivbarbering med varmt håndkle"),
    "barneklipp": ("jk-barber-felles-barneklipp.jpg", "Barneklipp i stolen"),
    "kombo": ("jk-barber-felles-barberer-med-kunde.jpg", "Klipp og skjegg hos samme barberer"),
}

FOR_ETTER = {
    "herreklipp": ["Før og etter 1", "Før og etter 2", "Side part med lengde", "Teksturert topp"],
    "skin-fade": ["Før og etter 1", "Før og etter 2", "Low fade", "High fade med tekstur"],
    "skjeggtrim": ["Før og etter 1", "Før og etter 2", "Kort stubb med linjer", "Fullskjegg med form"],
    "barbering": ["Varmt håndkle", "Krem og kost", "Kniv", "Resultat"],
    "barneklipp": ["Første klipp", "Barneklipp skin fade", "Far og sønn", "Resultat"],
    "kombo": ["Før og etter 1", "Før og etter 2", "Skin fade og skjegg", "Klipp og knivbarbering"],
}

# Produkttips per tjeneste: (overskrift, tekst, plassholder-motiv). Merker fra merkelisten (11).
PRODUKTER = {
    "herreklipp": ("Hold klippen hjemme", [
        ("Pomade eller leire til toppen", "Reuzel og Uppercut Deluxe for hold og glans eller matt finish. Barbereren viser deg mengde og teknikk.", "Pomade og leire (Reuzel, Uppercut Deluxe)"),
        ("Lett styling og tekstur", "Slickhaven og HUFS for naturlig hold uten glans.", "Styling (Slickhaven, HUFS)"),
        ("Sjampo og pleie", "Davines og in:on til hår og hodebunn mellom besøkene.", "Sjampo og pleie (Davines, in:on)"),
    ]),
    "skin-fade": ("Hold faden skarp hjemme", [
        ("Pomade eller leire til toppen", "Reuzel og Uppercut Deluxe for hold og tekstur. Barbereren viser deg mengde og teknikk.", "Pomade og leire (Reuzel, Uppercut Deluxe)"),
        ("Lett styling og tekstur", "Jobski Cosmetics og Slickhaven for dem som vil ha naturlig hold uten glans.", "Saltspray og styling (Jobski Cosmetics, Slickhaven)"),
        ("Ro i huden etter faden", "Proraso og Davines til hud og skalp der maskinen har gått helt ned.", "Hud og skalp (Proraso, Davines)"),
    ]),
    "skjeggtrim": ("Hold skjegget i form hjemme", [
        ("Skjeggolje daglig", "Pan Drwal og Gråbein holder huden under skjegget myk og hindrer flass.", "Skjeggolje (Pan Drwal, Gråbein)"),
        ("Balm og voks til form", "Proraso og Pan Drwal for hold i et lengre skjegg.", "Skjeggbalm (Proraso, Pan Drwal)"),
        ("Børste og kam", "Børst skjegget nedover om morgenen. Barbereren viser deg hvordan.", "Skjeggbørste og kam"),
    ]),
    "barbering": ("Barbering hjemme mellom besøkene", [
        ("Barberkrem og kost", "Proraso og Taylor of Old Bond Street, de samme vi bruker i stolen.", "Barberkrem (Proraso, Taylor of Old Bond Street)"),
        ("Etterbehandling uten alkohol", "Proraso aftershave-balm som roer huden.", "Aftershave-balm (Proraso)"),
        ("Pre-shave-olje", "Pan Drwal mykgjør stubbene før kniven eller høvelen.", "Pre-shave-olje (Pan Drwal)"),
    ]),
    "barneklipp": ("Enkel styling for de minste", [
        ("Mild sjampo", "Davines og in:on til sart hodebunn.", "Mild sjampo (Davines, in:on)"),
        ("Lett voks eller leire", "HUFS og Slickhaven for en topp som holder seg til skoledagen er over.", "Lett voks (HUFS, Slickhaven)"),
        ("Kam og børste", "Så frisyren fra stolen holder seg til neste gang.", "Kam og børste"),
    ]),
    "kombo": ("Hold både hår og skjegg hjemme", [
        ("Styling til toppen", "Reuzel, Uppercut Deluxe eller Slickhaven, avhengig av hold og finish.", "Pomade og leire (Reuzel, Uppercut Deluxe)"),
        ("Skjeggolje og balm", "Pan Drwal og Gråbein til skjegget, hver dag.", "Skjeggolje (Pan Drwal, Gråbein)"),
        ("Hud og skalp", "Proraso og Davines der maskinen og kniven har vært.", "Hud og skalp (Proraso, Davines)"),
    ]),
}

STEMPEL = {
    "herreklipp": ("Hver 10. klassiske klipp gratis", "J&K-appen har eget stempelkort for klassisk klipp. Barbereren registrerer stempelet i salongen etter hver behandling, og det 10. stempelet gir deg klippen gratis."),
    "skin-fade": ("Hver 10. skin fade gratis", "J&K-appen har eget stempelkort for skin fade. Barbereren registrerer stempelet i salongen etter hver behandling, og det 10. stempelet gir deg skin fade gratis."),
    "skjeggtrim": ("Hver 10. skjeggtrim gratis", "J&K-appen har eget stempelkort for skjegg. Barbereren registrerer stempelet i salongen etter hver behandling, og det 10. stempelet gir deg skjeggtrimmen gratis."),
    "barbering": ("Stempelkort i appen", "Appen har fire stempelkort: klassisk klipp, skin fade, skjegg og kombo. Hvert 10. stempel gir deg behandlingen gratis. Barbereren registrerer stempelet i salongen."),
    "barneklipp": ("Stempel for din egen klipp", "Barneklipp gir ikke stempel i appen, men tar du klipp samtidig, får du stempel for din egen klipp. Hvert 10. stempel gir deg behandlingen gratis."),
    "kombo": ("Hver 10. kombo gratis", "Kombo har sitt eget stempelkort i appen: hver kombo gir ett stempel på kombokortet, og den tiende komboen er gratis. Barbereren registrerer stempelet i salongen."),
}


def split_beskrivelse(html):
    """Deler beskrivelse-HTML i {'intro': ..., 'Hva du får': ..., 'Slik foregår det': ..., ...} på <h2>."""
    parts = re.split(r"<h2>(.*?)</h2>", html)
    out = {"intro": parts[0]}
    for i in range(1, len(parts) - 1, 2):
        out[parts[i].strip()] = parts[i + 1]
    return out


def steg_html(tekst_html):
    """Gjør avsnittet 'Slik foregår det' om til nummererte steg (2 til 4), første setning som leder."""
    setn = split_sentences(re.sub(r"<[^>]+>", " ", tekst_html))
    grupper = chunk_even(setn, 4) if len(setn) >= 4 else [[x] for x in setn]
    out = []
    for i, g in enumerate(grupper, 1):
        lead, rest = g[0], " ".join(g[1:])
        out.append(f'<div class="steg"><div class="steg-num" aria-hidden="true">{i}</div><div><div class="steg-tittel">{e(lead)}</div>'
                   + (f'<p class="muted">{e(rest)}</p>' if rest else "") + "</div></div>")
    return "".join(out)


def inkludert_html(html):
    """'Hva du får': lister med hake-ikon, mellomtitler beholdes."""
    html = html.replace("<ul>", '<ul class="hake">')
    return html


def render_tjeneste(ctx, t):
    s, fn = ctx["site"], ctx["fn"]
    slug = t["slug"]
    deler = split_beskrivelse(t["beskrivelse"])
    intro = re.sub(r"^<p>|</p>$", "", deler["intro"].strip())
    intro = intro.replace(" Behandlingen er for både menn og kvinner.", "")
    navn_kort = t["title"].split(":")[0]

    bilde_navn, bilde_alt = TJ_BILDE[slug]
    hero_img = IM.picture(bilde_navn, bilde_alt, 900, 760, cls="hero-bilde", lazy=False, motiv=bilde_alt)
    regel = (f"{navn_kort} er for både menn og kvinner, som alle behandlingene på menyen vår. "
             "Vil du ha kort hår, skin fade eller en skikkelig herreklipp, er du velkommen uansett kjønn. "
             "Bestill på vanlig måte og velg behandlingen du vil ha.")
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("Tjeneste · " + str(t["varighetMin"]) + " minutter")}'
        f'<h1>{e(t["h1"])}</h1><p class="hero-ingress">{intro}</p><p class="regel0">{regel}</p>'
        f'<div class="pris-stor"><span class="pris-tall">{nb_num(t["fraPris"])} til {nb_num(t["tilPris"])} kr</span><span class="muted small">Nivå Barber, varierer per avdeling</span></div>'
        f'<div class="knapper">{L.btn(e(t["knappetekst"]), "/bestill-time/", bestill="felles", plassering="tjeneste-hero")}{L.btn("Se før og etter", "#for-etter", "s", external=False)}</div>'
        f'</div>{hero_img}</div>', cls="sec-hero")

    inkl = L.section(
        f'<div class="split split-start"><div class="sec-head">{L.eyebrow("Hva du får")}<h2>Dette er inkludert</h2><div class="inkludert">{inkludert_html(deler.get("Hva du får", ""))}</div></div>'
        f'<div class="sec-head">{L.eyebrow("Slik foregår det")}<h2>Slik foregår det i stolen</h2><div class="steg-liste">{steg_html(deler.get("Slik foregår det", ""))}</div>'
        f'<p class="muted small">{e(t["varighetTekst"])}</p></div></div>', tone="flate")

    kort = []
    for a in ctx["avdelinger"]:
        p = fn["pris"](slug, a["slug"])
        pris = kr(p["pris"]) if p else "Se booking"
        kort.append(f'<div class="card pris-kort"><div class="pris-kort-navn">{e(a["title"])}</div><div class="pris-kort-tall">{pris}</div>'
                    f'{L.link(e(a["bestillKnapp"]), a["fixitUrl"], bestill=a["ga4Avdeling"], plassering="tjeneste-pris")}</div>')
    rader = fn["priser_tjeneste"](slug)
    tab_rows = []
    for r in rader:
        celler = [e(r["behandling"]), f'{r["varighet"]} min' if r["varighet"] else ""]
        for a in ctx["avdelinger"]:
            v = r["priser"].get(a["slug"])
            celler.append(nb_num(v) if v is not None else '<span class="muted">Tilbys ikke</span>')
        tab_rows.append(celler)
    tabell = L.tabell(["Behandling", "Varighet"] + [e(a["kortnavn"]) for a in ctx["avdelinger"]], tab_rows)
    stempel_t, stempel_x = STEMPEL[slug]
    priser = L.section(
        L.heading(f"{e(navn_kort)}: pris per avdeling",
                  f"Prisene viser nivået Barber. {s['prisSetning']} Hårvask inngår i klipp, du velger selv om du vil ha den.", "Priser")
        + f'<div class="grid grid-4">{"".join(kort)}</div>'
        + f'<h3 class="h3-tabell">Alle varianter av {e(navn_kort.lower())}, priser i kroner for nivå Barber</h3>{tabell}'
        + f'<div class="prosa prisnivaer">{t["prisnivaer"]}</div>'
        + '<div class="grid grid-3">'
        f'<div class="card info-kort">{L.eyebrow("Booking", muted=True)}<div class="info-tittel">Velg barberer selv</div><p class="muted">I onlinebookingen velger du selv barberer og ser nivå og pris før du bekrefter. Alle jobber etter samme standard, med samme konsultasjon først.</p></div>'
        f'<div class="card info-kort">{L.eyebrow("Avbestilling", muted=True)}<div class="info-tittel">Senest 24 timer før</div><p class="muted">Avbestill eller flytt timen senest 24 timer før i bookingen eller appen. Betaling i salongen med kort eller Vipps.</p></div>'
        f'<div class="card info-kort info-messing">{L.eyebrow("Stempelkort i appen")}<div class="info-tittel">{e(stempel_t)}</div><p class="muted">{e(stempel_x)}</p><a href="/app/">Les om appen og stempelkortet</a></div>'
        '</div>', id_="priser")

    fe = "".join(IM.ph(m, f"jk-barber-felles-{slug}-{i + 1}.jpg", cls="galleri-bilde") for i, m in enumerate(FOR_ETTER[slug]))
    hvem = deler.get("Hvem passer det for", "")
    for_etter_tekst = deler.get("Før og etter", "")
    foretter = L.section(
        f'<h2>Før og etter</h2><div class="galleri">{fe}</div>'
        f'<div class="split split-start prosa-grid"><div class="prosa"><h3>Hvem passer det for</h3>{hvem}</div><div class="prosa"><h3>Før og etter timen</h3>{for_etter_tekst}</div></div>',
        tone="mork", id_="for-etter")

    ptit, pliste = PRODUKTER[slug]
    pk = "".join(f'<div class="card produkt-kort">{IM.ph(m, cls="produkt-ph")}<div class="info-tittel">{e(h)}</div><p class="muted">{e(x)}</p></div>' for h, x, m in pliste)
    produkter = L.section(
        f'<div class="split split-start split-16"><div class="sec-head">{L.eyebrow("Produkter")}<h2>{e(ptit)}</h2>'
        f'<p class="lead muted">Det barbereren bruker i stolen, kan du ta med hjem. Alle produktene finner du i nettbutikken vår, j-kshop.no.</p>'
        f'{L.btn("Handle på j-kshop.no", s["nettbutikk"], "s")} <a class="lenke-under" href="/produkter/">Merkene vi fører</a></div>'
        f'<div class="grid grid-3">{pk}</div></div>')

    faq_items, sett = [], set()
    for f in fn["faq_for"]("tjeneste", slug):
        if f["sporsmal"] in sett:
            continue
        sett.add(f["sporsmal"])
        faq_items.append(f)
    faq = L.section(L.faq_block(faq_items, heading_text=f"Om {e(navn_kort.lower())}",
                                lead="Svarene står også som strukturerte data, så de kan vises direkte i Google."))

    avd_lenker = " · ".join(L.link(e(a["kortnavn"]), a["fixitUrl"], bestill=a["ga4Avdeling"], plassering="tjeneste-cta") for a in ctx["avdelinger"])
    rel = " · ".join(f'<a href="{ctx["tj"][r]["url"]}">{e(ctx["tj"][r]["title"])}</a>' for r in t["relaterte"] if r in ctx["tj"])
    cta = L.section(
        L.cta_box(f"Bestill {e(navn_kort.lower())} hos nærmeste avdeling", avd_lenker,
                  L.btn("Velg avdeling og bestill", "/bestill-time/", bestill="felles", plassering="tjeneste-cta"))
        + f'<div class="card guide-boks">{L.eyebrow("Guide fra barbererne", muted=True)}<h2><a href="/post/{t["bloggSlug"]}/">{e(t["bloggTittel"])}</a></h2>'
        f'<p class="muted">{e(t["bloggIngress"])}</p>{L.btn("Les guiden", "/post/" + t["bloggSlug"] + "/", "s", external=False)}</div>'
        + (f'<p class="muted small">Relaterte tjenester: {rel}. Se også <a href="/avdelinger/">alle avdelinger</a>.</p>' if rel else ""),
        id_="bestill")

    body = hero + inkl + priser + foretter + produkter + faq + cta

    base = s["base"]
    pris_per_avd = ", ".join(f"{kr(fn['pris'](slug, a['slug'])['pris'])} {a['title']}" for a in ctx["avdelinger"] if fn["pris"](slug, a["slug"]))
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": base + t["url"] + "#service",
        "name": t["title"],
        "serviceType": t["h1"],
        "description": t["seoBeskrivelse"],
        "url": base + t["url"],
        "image": IM.url(bilde_navn, 1200, 800) or IM.LOGO_SCHEMA,
        "provider": {"@id": base + "/#organization"},
        "brand": {"@id": base + "/#organization"},
        "areaServed": [{"@type": "City", "name": a["poststed"]} for a in ctx["avdelinger"]],
        "availableChannel": [
            {"@type": "ServiceChannel", "name": a["title"], "serviceUrl": a["fixitUrl"],
             "serviceLocation": {"@id": base + a["url"] + "#barbershop"}} for a in ctx["avdelinger"]
        ],
        "offers": {
            "@type": "Offer", "priceCurrency": "NOK",
            "priceSpecification": {"@type": "PriceSpecification", "minPrice": str(t["fraPris"]), "maxPrice": str(t["tilPris"]),
                                   "priceCurrency": "NOK",
                                   "description": f"Pris for nivå Barber, varierer per avdeling: {pris_per_avd}. Endelig pris vises i onlinebookingen."},
            "availability": "https://schema.org/InStock",
            "url": base + "/bestill-time/",
        },
        "termsOfService": base + "/bestill-time/",
    }
    crumbs = [("Tjenester og priser", "/tjenester/"), (t["title"], None)]
    return L.page(ctx, path=t["url"], title=t["seoTittel"], description=t["seoBeskrivelse"], body=body, breadcrumbs=crumbs,
                  jsonld=[service, L.faq_jsonld(faq_items)], active="tjenester", og_image=IM.url(bilde_navn, 1200, 630))


NIVAER_LANG = [
    ("Lærling", "Under opplæring hos oss, alltid med en erfaren barberer i rommet. Gjør klassisk klipp, skjeggtrim og enklere fade, og blir bedre for hver uke. Litt under Barber-prisen, og en god måte å bli kjent med oss på."),
    ("Junior", "Ferdig utdannet og selvstendig på de vanligste behandlingene. Trygg på klassisk klipp, skjegg og fade, og gjør knivbarbering. Litt under Barber-prisen."),
    ("Barber", "Erfaren og rask i hendene, mestrer hele programmet inkludert skarpe skin fades og kniv. De fleste barbererne våre er på dette nivået, og det er denne prisen du ser i tabellen."),
    ("Senior", "Våre mest erfarne barberere, med flere års fartstid og spesialkompetanse på skin fade, skjeggdesign og knivbarbering. De lærer opp de andre. Senior koster litt mer enn Barber: typisk 50 kr mer på klipp, 70 kr mer på skjeggtrim og 50 til 100 kr mer på kombo og deluxe. Voksing og bart koster det samme uansett nivå."),
]

KATEGORI_TITTEL = {
    "Hårklipp": ("Hårklipp", ""),
    "Re-fresh": ("Re-fresh", "Vedlikehold innen 15 dager etter forrige besøk hos oss, ellers ordinær pris."),
    "Kombo": ("Kombo", ""),
    "Skjegg": ("Skjegg", ""),
    "Barbering": ("Barbering", ""),
    "Deluxe": ("Deluxe-behandlinger", ""),
    "Voksing": ("Voksing og napping", "Samme pris uansett barberens nivå."),
}


def render_oversikt(ctx):
    s, fn = ctx["site"], ctx["fn"]
    hero = L.section(
        f'<div class="sec-head sec-head-stor">{L.eyebrow("Tjenester og priser")}<h1>Tjenester og priser</h1>'
        '<p class="lead muted">Her er alt vi gjør, med pris per avdeling for nivå Barber. Prisen du betaler avhenger av hvilken barberer du velger, og det velger du selv i bookingen. Les hvordan nivåene fungerer under tabellen.</p>'
        f'<p class="regel0">{s["regel0"]}</p></div>'
        '<div class="grid grid-3">' + "".join(
            f'<article class="card tj-kort tj-kort-liten"><div class="kort-innhold"><h2><a href="{t["url"]}">{e(t["title"])}</a></h2><p class="muted">{e(t["ingress"])}</p>'
            f'<div class="kort-bunn"><span class="pris">{nb_num(t["fraPris"])} til {nb_num(t["tilPris"])} kr</span><span class="muted small">{t["varighetMin"]} min</span></div></div></article>'
            for t in ctx["tjenester"]) + "</div>", cls="sec-hero")

    head = ["Behandling", "Varighet"] + [f'<a href="{a["url"]}">{e(a["kortnavn"])}</a>' for a in ctx["avdelinger"]] + ["Mer"]
    blokker = []
    for kat, rader in fn["priser_kategori"]():
        tittel, note = KATEGORI_TITTEL.get(kat, (kat, ""))
        rows = []
        for r in rader:
            celler = [e(r["behandling"]), f'{r["varighet"]} min' if r["varighet"] else ""]
            for a in ctx["avdelinger"]:
                v = r["priser"].get(a["slug"])
                celler.append(nb_num(v) if v is not None else '<span class="muted">Tilbys ikke</span>')
            tslug = r.get("tjenesteSlug")
            celler.append(f'<a href="{ctx["tj"][tslug]["url"]}">Les mer</a>' if tslug in ctx["tj"] else "")
            rows.append(celler)
        blokker.append(f'<h3>{e(tittel)}</h3>' + (f'<p class="muted small">{e(note)}</p>' if note else "") + L.tabell(head, rows))
    tabell = L.section(
        L.heading("Priser for nivå Barber",
                  "Behandlingsnavnene er de samme som i bookingen, så du finner dem igjen når du bestiller. Kolonnene er avdelingene; trykk på en avdeling for å se mer om den. Tabellen kan rulles sideveis på mobil.")
        + "".join(blokker)
        + f'<p class="muted small">Priser for nivå Barber. {s["prisSetning"]} Alle priser er i norske kroner inkludert mva. Varighetene er tiden som settes av i bookingen. Hårvask inngår i klipp på alle nivåer, du velger selv om du vil ha vask. Hjemmebarbering har egen prisliste, se <a href="/hjemmebarbering/">hjemmebarbering</a>.</p>',
        tone="flate", id_="priser")

    niva_kort = "".join(
        f'<div class="card niva-kort{" niva-senior" if i == 3 else ""}">{L.eyebrow(f"Nivå {i + 1}", muted=(i != 3))}<h3>{n}</h3><p class="muted">{t}</p></div>'
        for i, (n, t) in enumerate(NIVAER_LANG))
    nivaer = L.section(
        L.heading("Slik fungerer prisnivåene", "Prisene i tabellen er for nivå Barber, som er standardnivået hos oss. Barbererne våre er delt inn i fire nivåer, og prisen følger nivået:")
        + f'<div class="grid grid-2">{niva_kort}</div>'
        '<p class="muted">Ikke alle avdelinger har alle nivåer. Finnes det ikke Lærling eller Junior der du bestiller, er Barber-prisen den laveste prisen i den avdelingen. Alle nivåer bruker samme produkter, følger samme rutine med konsultasjon først, og står for samme kvalitetsløfte: er du ikke fornøyd, retter vi det.</p>'
        f'<p>{s["regel0"]} Prisene er de samme uavhengig av kjønn: pris følger behandling og barberens nivå.</p>',
        id_="nivaer")

    steg = [("Trykk Bestill time og velg avdeling.", ""), ("Velg behandling.", "Du ser varigheten med en gang."),
            ("Velg barberer.", "Ved navnet står nivået og prisen for akkurat den behandlingen."),
            ("Velg tidspunkt og bekreft.", "Du får bekreftelse på SMS og e-post.")]
    steg_html_ = "".join(f'<div class="steg"><div class="steg-num" aria-hidden="true">{i}</div><div><div class="steg-tittel">{a}</div>' + (f'<p class="muted">{b}</p>' if b else "") + "</div></div>" for i, (a, b) in enumerate(steg, 1))
    velg = L.section(
        f'<div class="split split-start"><div class="sec-head">{L.eyebrow("Booking")}<h2>Slik velger du barberer</h2><div class="steg-liste">{steg_html_}</div>'
        '<p class="muted">Vet du ikke hvem du skal velge? Start med nivå Barber, eller velg den barbereren som har ledig tid når det passer deg. Du velger alltid barberer selv i bookingen.</p></div>'
        f'<div class="sec-head">{L.eyebrow("Betaling og gavekort")}<h2>Betaling og gavekort</h2>'
        f'<p class="muted">Du betaler i salongen etter behandlingen, med kort eller Vipps i kassen, i alle avdelinger. Gavekort kjøpes på <a href="{s["gavekort"]}" target="_blank" rel="noopener">fixit.no</a>, gjelder i alle avdelinger og brukes som betalingsmiddel i kassen (ikke i onlinebookingen). Stempelkortene i appen gir deg den tiende behandlingen gratis på Klassisk klipp, Skin fade, Skjeggtrim og Kombo.</p>'
        f'<div class="knapper">{L.btn("Gavekort", "/gavekort/", "s")}{L.btn("Appen og stempelkort", "/app/", "s")}</div></div></div>',
        tone="mork")

    faq_items = fn["faq_for"]("tjeneste")
    faq = L.section(L.faq_block(faq_items))
    cta = L.section(L.cta_box("Bestill time", "Velg avdeling, barberer og tidspunkt. Det tar under ett minutt.",
                              L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering="tjenester-cta"))
                    + '<p class="muted small">Avdelinger: ' + " · ".join(f'<a href="{a["url"]}">{e(a["title"])}</a>' for a in ctx["avdelinger"]) + "</p>")
    body = hero + tabell + nivaer + velg + faq + cta
    return L.page(ctx, path="/tjenester/", title="Tjenester og priser: klipp, skin fade, skjegg | J&K",
                  description="Alle behandlinger hos J&K Barber Shop med pris per avdeling: herreklipp, skin fade, skjeggtrim, knivbarbering, barneklipp og kombo. Slik fungerer nivåene.",
                  body=body, breadcrumbs=[("Tjenester og priser", None)], jsonld=[L.faq_jsonld(faq_items)], active="tjenester")


def render(ctx):
    out = {"/tjenester/": render_oversikt(ctx)}
    for t in ctx["tjenester"]:
        out[t["url"]] = render_tjeneste(ctx, t)
    return out

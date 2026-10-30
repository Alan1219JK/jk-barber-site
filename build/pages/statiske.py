"""Statiske sider: /om-oss/, /app/, /gavekort/, /produkter/, /jobb/, /franchise/, /kontakt/,
/hjemmebarbering/, /bestill-time/, /personvern/, /tilbakemelding/, /takk/ og 404.html.

Tekster: innholdsplan del 2 (title/meta/H1), 6.2 til 6.13, designskisse OmOss.dc.html.
Skjemafelt: WIX-NY-SITE.md del 5 (name = feltets target i Wix Forms).
Punkter merket [SJEKK] i planen er utelatt eller skrevet uten løfte.
"""
import math

from lib import layout as L
from lib import images as IM
from lib.util import e, kr
from pages.forside import apningstider_kort

MAILTO = "mailto:post@j-kbarber.no"


# ---------- skjemahjelpere ----------

def felt(name, label, *, type_="text", required=False, hint="", placeholder="", autocomplete="", extra=""):
    req = " required" if required else ""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    ph = f' placeholder="{e(placeholder)}"' if placeholder else ""
    h = f'<span class="hint">{hint}</span>' if hint else ""
    stj = ' <span class="brass" aria-hidden="true">*</span>' if required else ""
    return (f'<div class="felt"><label for="f-{name}">{label}{stj}</label>'
            f'<input type="{type_}" id="f-{name}" name="{name}"{req}{ac}{ph}{extra}>{h}</div>')


def tekstfelt(name, label, *, required=False, hint="", rows=5):
    req = " required" if required else ""
    h = f'<span class="hint">{hint}</span>' if hint else ""
    stj = ' <span class="brass" aria-hidden="true">*</span>' if required else ""
    return (f'<div class="felt"><label for="f-{name}">{label}{stj}</label>'
            f'<textarea id="f-{name}" name="{name}" rows="{rows}"{req}></textarea>{h}</div>')


def nedtrekk(name, label, options, *, required=False, hint="", avd_velger=False, tom="Velg"):
    """options: liste med str eller (verdi, data-slug)."""
    req = " required" if required else ""
    dv = " data-avd-velger" if avd_velger else ""
    opts = [f'<option value="">{e(tom)}</option>']
    for o in options:
        if isinstance(o, tuple):
            v, slug = o
            opts.append(f'<option value="{e(v)}" data-slug="{e(slug)}">{e(v)}</option>')
        else:
            opts.append(f'<option value="{e(o)}">{e(o)}</option>')
    h = f'<span class="hint">{hint}</span>' if hint else ""
    stj = ' <span class="brass" aria-hidden="true">*</span>' if required else ""
    return (f'<div class="felt"><label for="f-{name}">{label}{stj}</label>'
            f'<select id="f-{name}" name="{name}"{req}{dv}>{"".join(opts)}</select>{h}</div>')


def valg(name, label, options, *, type_="checkbox", required=False, hint=""):
    """Avkrysningsgruppe (flere med samme name sendes som liste) eller radioknapper."""
    rows = []
    for i, o in enumerate(options):
        # required på radio: alle i gruppen; på checkbox-gruppe lar vi JS/Wix avgjøre (minst én krysses normalt av)
        req = " required" if (required and type_ == "radio") else ""
        rows.append(f'<label><input type="{type_}" name="{name}" value="{e(o)}"{req}> <span>{e(o)}</span></label>')
    h = f'<span class="hint">{hint}</span>' if hint else ""
    stj = ' <span class="brass" aria-hidden="true">*</span>' if required else ""
    return (f'<fieldset class="felt felt-gruppe"><legend>{label}{stj}</legend>'
            f'<div class="valg">{"".join(rows)}</div>{h}</fieldset>')


def samtykke(name, tekst=None):
    tekst = tekst or ('Jeg samtykker til at J&amp;K Barber Shop lagrer opplysningene jeg sender inn for å svare på henvendelsen. '
                      'Les <a href="/personvern/">personvernerklæringen</a>.')
    return f'<label class="samtykke"><input type="checkbox" name="{name}" value="true" required> <span>{tekst}</span></label>'


def skjema(form_id, navn, felter_html, knapp, takk_tittel, takk_tekst, *, takk_id="takk"):
    return (f'<form class="skjema" data-wix-form="{form_id}" data-skjema="{navn}" data-takk="#{takk_id}" method="post" action="#{takk_id}">'
            f'{felter_html}<p class="muted small">Felt merket med <span class="brass">*</span> må fylles ut.</p>'
            f'<button class="btn btn-p" type="submit">{knapp}</button>'
            f'<p class="skjema-status" aria-live="polite"></p></form>'
            f'<div class="skjema-takk card" id="{takk_id}" role="status"><h3>{takk_tittel}</h3><p class="muted">{takk_tekst}</p></div>')


def avd_navn(a):
    return "Åsenveien 3, Ski sentrum" if a["slug"] == "asenveien" else a["title"]


def avd_option(a):
    """Verdi i Wix-nedtrekk: avdelingens tittel (Åsenveien 3 for asenveien)."""
    return ("Åsenveien 3" if a["slug"] == "asenveien" else a["title"], a["slug"])


def plass_kort(a):
    return a["plassering"].split(". Følg")[0].rstrip(".")


# ---------- /om-oss/ ----------

TIDSLINJE = [
    ("2018", "Åsenveien 3 i Ski", "Første avdeling, med samme inngang som Unilabs. Her startet J&amp;K Barber Shop, og avdelingen er fortsatt åpen i dag. Logoen bærer fortsatt ESTD 2018."),
    ("2019", "Ski Storsenter", "Andre avdeling i Ski, på brugangen mot Telia. Kort vei fra Ski stasjon, og raskt den avdelingen med flest barberere og lengst åpningstid."),
    ("2020", "Sandvika Storsenter og Kolbotn Torg", "Vi gikk ut av Ski for første gang, til Kjørbokollen i Sandvika og til Kolbotn Torg ved Vinmonopolet. Midt i et år der det meste stengte, åpnet vi to salonger, fordi kundene ba om det."),
    ("2021 til 2024", "Appen og nettbutikken", "Appen med digitalt stempelkort kommer, og nettbutikken vår, J&amp;K Shop, vokser til en av Norges største på barber- og herrepleieprodukter."),
    ("2025", "Strømmen Storsenter, Jessheim Storsenter og Rykkinn Senter", "Tre nye avdelinger på ett år. Romerike fikk to, og Bærum fikk sin andre på Rykkinn. Kjeden gikk fra fire til sju avdelinger."),
    ("I dag", "Sju avdelinger, én familie", "Samme telefonnummer, samme app og samme stempelkort uansett hvor du klipper deg. Og samme løfte som i 2018."),
]

KVALITET = [
    ("Konsultasjon før hver behandling.", "Ingen klipp uten at vi har snakket sammen først."),
    ("Tydelige nivåer og priser.", "Du ser nivået og prisen til barbereren før du bestiller. Ingen overraskelser i kassen."),
    ("Rett opp om noe er feil.", "Er du ikke fornøyd, si fra i stolen, så justerer vi. Oppdager du det hjemme, ta kontakt så snart du kan, så finner vi en løsning."),
    ("Samme standard i alle avdelinger.", "Samme produkter, samme rutiner, samme stempelkort, uansett hvor du er."),
    ("Rene verktøy, nye blad.", "Engangsblad byttes for hver kunde. Verktøy desinfiseres mellom hver kunde."),
]


def render_om_oss(ctx):
    s = ctx["site"]
    hero_img = IM.picture("jk-barber-asenveien-historisk-2018.jpg", "Den første J&K Barber Shop i Åsenveien 3 i Ski, 2018", 900, 700,
                          cls="hero-bilde", lazy=False, motiv="Den første salongen i Åsenveien 3, Ski, gjerne et eldre bilde fra 2018")
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("J&amp;K-familien siden 2018")}'
        '<h1>Om J&amp;K Barber Shop</h1>'
        '<p class="hero-ingress">J&amp;K Barber Shop startet med én salong i Åsenveien 3 i Ski i 2018 og en enkel idé: folk i Follo fortjente en barbershop der håndverket, roen og tiden var på plass. I dag er vi sju avdelinger i Follo, Bærum og Romerike, rundt 15 barberere på fire nivåer, over 12 000 kunder og over 1 100 anmeldelser på Google. Vi er fortsatt en familiebedrift, og ideen er den samme.</p>'
        f'<p class="regel0">{s["regel0"]}</p>'
        f'<div class="knapper">{L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering="om-oss-hero")}{L.btn("Finn din avdeling", "/avdelinger/", "s")}</div>'
        f'<p class="muted small">{L.stars()} {s["snitt"]} av 5 på Google, over 1 100 anmeldelser</p></div>{hero_img}</div>',
        cls="sec-hero")

    tl = "".join(f'<div class="tl"><div class="yr">{y}</div><div><h3>{t}</h3><p class="muted">{x}</p></div></div>' for y, t, x in TIDSLINJE)
    arbeid = IM.picture("jk-barber-felles-barberer-med-kunde.jpg", "Barberere i arbeid hos J&K Barber Shop", 800, 520, cls="bilde-rund",
                        motiv="Barberere i arbeid i en av salongene, ingen portretter")
    historien = L.section(
        f'<div class="split split-start split-14"><div class="sec-head">{L.eyebrow("Historien")}<h2>Fra én stol i Ski til sju avdelinger</h2>'
        '<p class="lead muted">Vi åpnet den første avdelingen i Åsenveien 3 i Ski i 2018, med samme inngang som Unilabs. Kundene kom tilbake, tok med seg venner og familie, og året etter flyttet vi også inn på Ski Storsenter. Siden har vi vokst ett senter om gangen, alltid i områder der vi selv bor og handler.</p>'
        '<p class="lead muted">Hver nye avdeling har blitt åpnet av barberere som allerede har jobbet hos oss. Det er slik vi holder på samme håndverk og samme måte å møte kundene på, enten du sitter i Ski, Sandvika eller på Jessheim.</p>'
        f'{arbeid}</div><div class="card tidslinje">{tl}</div></div>',
        tone="flate", id_="historien")

    hk = IM.picture("jk-barber-asenveien-fasade.jpg", "J&K Barber Shop i Åsenveien 3, hovedkontor", 800, 520, cls="bilde-rund")
    detalj = IM.picture("jk-barber-felles-handverk-detalj.jpg", "Barberer i arbeid, nærbilde av hendene", 800, 420, cls="bilde-rund",
                        motiv="Detalj fra salongen: stol, saks og speil")
    navnet = L.section(
        f'<div class="split split-center"><div class="card kort-navn">{L.eyebrow("Navnet")}<h2>J for Jan, K for Kevin</h2>'
        '<p class="lead">J&amp;K er oppkalt etter barna i familien, Jan og Kevin. Da den første salongen åpnet, var det naturlig å gi den navnet deres. Barbershopene har siden blitt omtalt som det tredje barnet i familien: noe vi har bygget opp sakte, tatt vare på og vært stolte av.</p>'
        f'<p class="muted">Det er fortsatt J&amp;K-familien som eier og driver J&amp;K Barber Shop, gjennom {e(s["juridisk"])} med hovedkontor i Åsenveien 3 i Ski. Det merker du på at vi er til stede i salongene, kjenner barbererne våre og svarer selv når du ringer eller skriver til oss. Avdelingene ledes av erfarne barberere, og du ser hvem som jobber i hver avdeling, og nivået deres, når du bestiller time.</p></div>'
        f'<div class="bilde-stabel">{hk}{detalj}</div></div>',
        id_="navnet")

    niva = "".join(
        f'<div class="card niva-kort{" niva-senior" if i == 3 else ""}">{L.eyebrow(f"Nivå {i + 1}", muted=(i != 3))}<h3>{n}</h3><p class="muted">{t}</p></div>'
        for i, (n, t) in enumerate(s["nivaer"]))
    kval = "".join(f'<li><strong>{t}</strong> {x}</li>' for t, x in KVALITET)
    jobber = L.section(
        f'<div class="split split-start split-14"><div class="sec-head">{L.eyebrow("Slik jobber vi")}<h2>Konsultasjon først, så saks og maskin</h2>'
        '<p class="lead muted">Rundt 15 barberere jobber hos oss, fordelt på sju avdelinger. Alle starter med en kort konsultasjon i stolen: hva vil du ha, hva hadde du sist, hvordan ligger håret, og hvordan vil du at det skal se ut om tre uker. Det tar to minutter og sparer deg for tre uker med en klipp du ikke liker. Så klipper vi.</p>'
        '<p class="lead muted">En barberer hos J&amp;K Barber Shop er valgt for faget sitt, ikke for å fylle en stol. Vi trener kontinuerlig på det som skiller en grei klipp fra en god: skin fade uten synlige overganger, skjegglinjer som følger ansiktet, knivbarbering som er glatt uten å irritere. Nye barberere går ved siden av erfarne barberere til de er klare, og vi forteller deg ærlig hvilket nivå hver barberer er på, så du kan velge selv.</p>'
        f'<p class="lead muted">{s["regel0"]}</p></div>'
        f'<div><p class="muted small">Barbererne våre jobber på fire nivåer. {s["prisSetning"]}</p><div class="grid grid-2 niva-grid">{niva}</div></div></div>'
        f'<div class="card laere"><div><h3>Vi jobber mot å bli godkjent lærebedrift</h3><p class="muted">Vi har lært opp barberere internt siden starten. Nå jobber vi mot å bli godkjent lærebedrift, slik at lærlingene våre kan ta fagbrev hos oss. Er du interessert i læreplass, ta gjerne kontakt.</p></div>{L.btn("Les om jobb hos oss", "/jobb/", "s")}</div>'
        f'<div class="split split-start"><div class="sec-head">{L.eyebrow("Kvalitetsløftet vårt")}<h2>Fem ting du kan regne med</h2></div><ol class="kvalitet">{kval}</ol></div>',
        tone="flate", id_="slik-jobber-vi")

    tall = [("7", "avdelinger", "I Follo, Bærum og Romerike, alle med parkering."),
            ("12 000+", "kunder", "Som har sittet i stolen hos oss siden 2018."),
            ("1 100+", "Google-anmeldelser", "Skrevet av kunder i alle sju avdelingene."),
            (s["snitt"], "i snitt på Google", "Av 5 mulige. Vi leser alle anmeldelsene."),
            ("2018", "siden starten i Ski", "Fortsatt familieeid og familiedrevet.")]
    tall_html = "".join(f'<div class="card tall-kort"><div class="tall-num">{n}</div><div class="tall-navn">{t}</div><p class="muted small">{x}</p></div>' for n, t, x in tall)
    tall_sec = L.section(L.heading("J&amp;K i tall", "", "Tall") + f'<div class="tall-grid">{tall_html}</div>', id_="tall")

    familien = L.section(
        L.heading("Resten av J&amp;K-familien",
                  f'J&amp;K Barber Shop er en del av J&amp;K-gruppen, sammen med <a href="{s["nettbutikk"]}" target="_blank" rel="noopener">J&amp;K Shop</a> (nettbutikk for hår-, skjegg- og hudpleie, j-kshop.no) og <a href="https://www.j-kbeauty.no" target="_blank" rel="noopener">J&amp;K Beauty Salon</a> (frisør- og skjønnhetssalong i Ski, j-kbeauty.no). Det gir oss innkjøpsavtaler og produkttilgang få barbershops har, og det gir deg produktene vi bruker i stolen, rett hjem i posten.',
                  "Søstersider")
        + f'<div class="knapper">{L.btn("Produktene vi bruker", "/produkter/", "s")}{L.btn("Handle på j-kshop.no", s["nettbutikk"], "s")}</div>',
        id_="familien")

    bli = L.section(
        L.heading("Jobb hos oss eller åpne din egen J&amp;K",
                  "Vi vokser med folk som allerede kjenner oss. Enten du vil stå i stolen hos oss eller drive din egen avdeling, begynner det med en samtale.",
                  "Bli en del av J&amp;K")
        + '<div class="grid grid-2">'
        f'<div class="card kort-stor">{L.eyebrow("Jobb hos oss", muted=True)}<h3>Ansettelse eller stolleie</h3>'
        '<p class="muted">Vi tar imot barberere på alle nivåer, fra lærling til senior. Du kan være ansatt hos oss eller leie stol og drive for deg selv i en av avdelingene våre, med bookingsystem, produkter og kunder på plass fra første dag. Send oss noen linjer om deg selv og gjerne bilder av arbeidet ditt.</p>'
        f'<div class="knapper">{L.btn("Send søknad", "/jobb/")}{L.btn(s["epost"], MAILTO + "?subject=Barberer", "s", external=False)}</div></div>'
        f'<div class="card kort-stor">{L.eyebrow("Franchise", muted=True)}<h3>Åpne J&amp;K i ditt nærområde</h3>'
        '<p class="muted">Kjenner du et sted i nærområdet ditt som mangler en skikkelig barbershop? Vi ser etter barberere som vil drive sin egen J&amp;K-avdeling. Forutsetningen er at du først jobber hos oss, slik at du kjenner måten vi jobber på, før du åpner din egen avdeling med vårt navn, vår app og våre systemer.</p>'
        f'<div class="knapper">{L.btn("Fortell oss om stedet ditt", "/franchise/")}{L.btn("Ring " + s["telefonVisning"], "tel:" + s["telefon"], "s", external=False)}</div></div>'
        '</div>', tone="mork", id_="bli-med")

    avd = " · ".join(f'<a href="{a["url"]}">{e(avd_navn(a))}</a>' for a in ctx["avdelinger"])
    bunn = L.section(
        L.cta_box("Klar for å besøke J&amp;K-familien?", "Velg avdeling, barberer og tidspunkt, det tar under ett minutt. Avbestilling senest 24 timer før.",
                  L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering="om-oss-cta"))
        + f'<p class="muted small andre-avd">Våre avdelinger: {avd}</p>')

    body = hero + historien + navnet + jobber + tall_sec + familien + bli + bunn
    base = s["base"]
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "@id": base + "/om-oss/#aboutpage",
          "url": base + "/om-oss/", "name": "Om J&K Barber Shop", "inLanguage": "nb-NO",
          "about": {"@id": base + "/#organization"}, "mainEntity": {"@id": base + "/#organization"},
          "description": "Historien om J&K Barber Shop: fra én salong i Åsenveien 3 i Ski i 2018 til sju avdelinger i Follo, Bærum og Romerike."}
    return L.page(ctx, path="/om-oss/", title="Om oss: barbershopkjede siden 2018 | J&K Barber Shop",
                  description="Historien om J&K Barber Shop: fra én salong i Åsenveien 3 i Ski i 2018 til sju avdelinger i Follo, Bærum og Romerike. Håndverket, familien og kvalitetsløftet.",
                  body=body, breadcrumbs=[("Om oss", None)], jsonld=[ld], active="om-oss",
                  og_image=IM.url("jk-barber-asenveien-fasade.jpg", 1200, 630))


# ---------- /app/ ----------

APP_FAQ = [
    ("Koster appen noe?", "Nei, den er gratis på iPhone og Android."),
    ("Får jeg stempel for barneklipp eller knivbarbering?", "Stempel gis for Klassisk klipp, Skin fade, Skjeggtrim og Kombo, på hvert sitt stempelkort. Andre behandlinger gir ikke stempel."),
    ("Hvordan får jeg stempelet?", "Vis appen i salongen etter behandlingen, så registrerer barbereren stempelet."),
    ("Gjelder stemplene i alle avdelingene?", "Ja. Stemplene gjelder på tvers av alle avdelingene våre. Tre stempler i Ski og seks i Sandvika på samme kort er ni stempler."),
    ("Hva skjer med stemplene mine om jeg bytter telefon?", "Logg inn med samme mobilnummer på den nye telefonen, så følger stemplene med."),
    ("Hvordan bruker jeg en kupong?", "Kuponger du har fått, ligger i appen. Vis kupongen i kassen når du betaler, så trekkes den fra."),
]


def app_knapper(s, plassering):
    return (f'<div class="knapper">{L.btn("Last ned i App Store", s["appStore"], aria_label="Last ned J&K Barber Shop-appen på App Store")}'
            f'{L.btn("Last ned på Google Play", s["googlePlay"], "s", aria_label="Last ned J&K Barber Shop-appen på Google Play")}</div>')


def render_app(ctx):
    s, fn = ctx["site"], ctx["fn"]
    img = IM.picture("jk-barber-felles-app-skjermbilder.jpg", "Skjermbilder fra J&K Barber Shop-appen: stempelkort, booking og kupong", 900, 700,
                     cls="hero-bilde", lazy=False, motiv="Tre skjermbilder fra appen: stempelkort, booking, kupong")
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("J&amp;K-appen")}<h1>J&amp;K-appen og stempelkortet</h1>'
        '<p class="hero-ingress">Appen er den enkleste måten å være kunde hos oss på. Bestill time, samle stempler, bruk kuponger og hold oversikt over besøkene dine, i alle sju avdelinger. Hvert 10. stempel gir deg behandlingen gratis.</p>'
        f'{app_knapper(s, "hero")}<p class="muted small">Gratis på iPhone og Android.</p></div>{img}</div>',
        cls="sec-hero")

    steg = [
        ("Last ned appen", "Registrer deg med mobilnummeret ditt. Det tar under ett minutt."),
        ("Samle stempler", "Hver gang du tar Klassisk klipp, Skin fade, Skjeggtrim eller Kombo hos oss, får du ett stempel på kortet for den behandlingen. Vis appen i salongen etter behandlingen, så registrerer barbereren stempelet."),
        ("Hvert 10. gratis", "Når du har ni stempler på et kort, er den tiende behandlingen gratis. Gratisbehandlingen er samme type som kortet: ni klassiske klipp gir gratis klassisk klipp, ni skin fades gir gratis skin fade, og det samme for skjegg og kombo."),
        ("Stemplene varer", "Hvert stempel er gyldig i ett år fra den dagen du fikk det. Går et stempel ut, forsvinner bare det ene, ikke hele kortet."),
        ("I alle avdelinger", "Stemplene gjelder på tvers av alle avdelingene våre. Tre stempler i Ski og seks i Sandvika på samme kort er ni stempler."),
    ]
    steg_html = "".join(f'<div class="steg"><div class="steg-num">{i + 1}</div><div><div class="steg-tittel">{t}</div><p class="muted">{x}</p></div></div>' for i, (t, x) in enumerate(steg))
    kort = "".join(f'<div class="card stempel-kort">{x}</div>' for x in ["Klassisk klipp", "Skin fade", "Skjegg", "Kombo"])
    stempel = L.section(
        f'<div class="split split-start"><div class="sec-head">{L.eyebrow("Stempelkortet")}<h2>Slik fungerer stempelkortet</h2>'
        '<p class="lead muted">Det er fire stempelkort i appen: ett for klassisk klipp, ett for skin fade, ett for skjegg og ett for kombo. Du trenger ikke gjøre noe annet enn å vise appen i salongen.</p>'
        f'<div class="grid grid-4 stempel">{kort}</div></div><div class="steg-liste">{steg_html}</div></div>',
        tone="flate", id_="stempelkort")

    faar = ["Timebestilling i alle avdelinger, med favorittbarberer lagret.",
            "Digitalt stempelkort som ikke kan mistes i vaskemaskinen.",
            "Kuponger og tilbud vi bare sender i appen.",
            "Historikk over besøkene dine, så du husker hva du hadde sist."]
    kasse = IM.picture("jk-barber-felles-app-kasse.jpg", "Kunde viser appen i kassen hos J&K Barber Shop", 800, 520, cls="bilde-rund",
                       motiv="Kunde viser appen i kassen")
    kuponger = L.section(
        f'<div class="split split-center"><div class="sec-head">{L.eyebrow("Kuponger og fordeler")}<h2>Dette får du i appen</h2>'
        '<p class="lead muted">Fra tid til annen legger vi kuponger og tilbud i appen, bare for dem som har den. Kupongen ligger i appen og vises i kassen når du betaler. Hvilke kuponger som gjelder akkurat nå, ser du i appen.</p>'
        '<ul class="hake-liste">' + "".join(f"<li>{x}</li>" for x in faar) + '</ul></div>' + kasse + '</div>',
        id_="fordeler")

    faq_items = [{"sporsmal": q, "svar": f"<p>{a}</p>", "svarTekst": a} for q, a in APP_FAQ]
    for f in fn["faq_for"]("app"):
        if f["sporsmal"] not in {q for q, _ in APP_FAQ}:
            faq_items.insert(0, f)
    faq = L.section(L.faq_block(faq_items, heading_text="Spørsmål om appen"), tone="flate", id_="faq")
    bunn = L.section(L.cta_box("Last ned appen", "Stempelkort, booking og kuponger samlet på ett sted. Gratis på iPhone og Android.",
                               app_knapper(s, "cta-bunn"))
                     + '<p class="muted small">Heller bestille uten app? <a href="/bestill-time/">Bestill time på nett</a>. Les også <a href="/gavekort/">om gavekort</a>.</p>')
    body = hero + stempel + kuponger + faq + bunn
    base = s["base"]
    app_ld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": "J&K Barber Shop-appen",
              "operatingSystem": "iOS, Android", "applicationCategory": "LifestyleApplication",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NOK"},
              "installUrl": [s["appStore"], s["googlePlay"]], "publisher": {"@id": base + "/#organization"},
              "description": "Timebestilling, digitalt stempelkort (hvert 10. stempel gir behandlingen gratis) og kuponger hos J&K Barber Shop."}
    return L.page(ctx, path="/app/", title="J&K-appen: stempelkort og fordeler | J&K Barber Shop",
                  description="Last ned J&K Barber Shop-appen: digitalt stempelkort der hvert 10. stempel gir behandlingen gratis, kuponger og timebestilling i alle avdelinger. iOS, Android.",
                  body=body, breadcrumbs=[("Appen", None)], jsonld=[app_ld, L.faq_jsonld(faq_items)], active="app")


# ---------- /gavekort/ ----------

def rund_opp(n, til=50):
    return int(math.ceil(n / til) * til)


def render_gavekort(ctx):
    s, fn = ctx["site"], ctx["fn"]
    gk = s["gavekort"]
    img = IM.picture("jk-barber-felles-gavekort.jpg", "Gavekort fra J&K Barber Shop", 900, 700, cls="hero-bilde", lazy=False,
                     motiv="Gavekort fra J&K Barber Shop, gjerne med messinglogo")
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("Gi bort en time")}<h1>Gavekort</h1>'
        '<p class="hero-ingress">Gi bort en time hos barbereren. Et gavekort fra J&amp;K Barber Shop har valgfritt beløp, gjelder i alle avdelingene våre og til alle behandlinger, fra klassisk herreklipp til knivbarbering med varme håndklær.</p>'
        f'<div class="knapper">{L.btn("Kjøp gavekort", gk, bestill="felles", plassering="gavekort-hero")}{L.btn("Se behandlingene", "/tjenester/", "s")}</div>'
        '<p class="muted small">Kjøpes på fixit.no og sendes på e-post. Innløses i kassen i salongen.</p></div>' + img + '</div>',
        cls="sec-hero")

    steg = [("Velg beløp", "Velg beløpet selv på gavekortsiden. Gavekortet har valgfri verdi, så mottakeren kan bruke det på akkurat den behandlingen han eller hun vil."),
            ("Betal på fixit.no", f'Betalingen går gjennom bookingsystemet vårt, Fixit. <a href="{gk}" target="_blank" rel="noopener">Kjøp gavekort</a>.'),
            ("Gavekortet sendes på e-post", "Til deg eller rett til mottakeren, med en hilsen fra deg. Skriv det ut eller send det videre."),
            ("Mottakeren bruker det i kassen", "Mottakeren bestiller time på nett eller i appen og bruker gavekortet som betaling i kassen i salongen. Gavekortet legges ikke inn i onlinebookingen.")]
    steg_html = "".join(f'<div class="steg"><div class="steg-num">{i + 1}</div><div><div class="steg-tittel">{t}</div><p class="muted">{x}</p></div></div>' for i, (t, x) in enumerate(steg))

    # Forslag til beløp: rundet opp fra høyeste Senior-pris i kjeden, så beløpet dekker alle nivåer i alle avdelinger.
    forslag = []
    for navn, beh in [("Klassisk herreklipp", "Klassisk herreklipp"), ("Skin fade", "Skin fade"),
                      ("Kombo, klipp og skjegg", "Kombo II: skin fade og skjeggtrim eller knivbarbering"),
                      ("Knivbarbering", "Barbering av skjegget med kniv")]:
        maks = max([p["pris"] for p in ctx["priser"] if p["behandling"] == beh] or [0])
        if maks:
            forslag.append((navn, rund_opp(maks + 1, 50), f"Dekker {navn.split(',')[0].lower()} hos alle nivåer i alle avdelingene våre."))
    forslag.append(("Fri verdi", None, "Velg beløpet selv, mottakeren bruker det på det han eller hun vil."))
    f_html = "".join(f'<div class="card pris-kort"><div class="pris-kort-navn">{e(n)}</div><div class="pris-kort-tall">{kr(b) if b else "Valgfritt"}</div><p class="muted small">{x}</p></div>' for n, b, x in forslag)
    slik = L.section(
        f'<div class="split split-start"><div class="sec-head">{L.eyebrow("Slik fungerer det")}<h2>Fire steg, så er gaven klar</h2><div class="steg-liste">{steg_html}</div></div>'
        f'<div class="sec-head">{L.eyebrow("Forslag til beløp")}<h2>Hva koster en time?</h2><p class="lead muted">Prisene våre avhenger av barberens nivå. Beløpene under dekker behandlingen hos alle nivåer, i alle avdelinger. Blir det penger til overs, står restbeløpet på kortet til neste gang.</p><div class="grid grid-2">{f_html}</div></div></div>',
        tone="flate", id_="slik")

    godt = [f"Gjelder i alle J&amp;K Barber Shop-avdelinger: {', '.join(e(avd_navn(a)) for a in ctx['avdelinger'][:-1])} og {e(avd_navn(ctx['avdelinger'][-1]))}.",
            "Restbeløp blir stående på kortet til neste gang.",
            "Gavekortet brukes som betalingsmiddel i kassen, ikke i onlinebookingen.",
            "Vil mottakeren ha en dyrere behandling enn gavekortet dekker, betales mellomlegget i salongen.",
            "Gavekort kan også kjøpes i salongen."]
    faq_items = list(fn["faq_for"]("gavekort"))
    faq_items.append({"sporsmal": "Hva om mottakeren vil ha en dyrere behandling enn gavekortet dekker?",
                      "svar": "<p>Mellomlegget betales i salongen, med kort eller Vipps.</p>", "svarTekst": "Mellomlegget betales i salongen, med kort eller Vipps."})
    faq_items.append({"sporsmal": "Kan jeg kjøpe gavekort i salongen?",
                      "svar": "<p>Ja. Si fra i kassen i hvilken som helst avdeling, så ordner vi det. På nett kjøper du det på fixit.no.</p>",
                      "svarTekst": "Ja. Si fra i kassen i hvilken som helst avdeling, så ordner vi det. På nett kjøper du det på fixit.no."})
    info = L.section(
        f'<div class="split split-start"><div><div class="sec-head">{L.eyebrow("Godt å vite")}<h2>Før du kjøper</h2></div><ul class="hake-liste">' + "".join(f"<li>{x}</li>" for x in godt) + '</ul></div>'
        + L.faq_block(faq_items, heading_text="Spørsmål om gavekort", side=False, id_="faq") + '</div>', id_="godt-a-vite")
    bunn = L.section(L.cta_box("Kjøp gavekort", "Valgfritt beløp, sendes på e-post, gjelder i alle avdelinger.",
                               L.btn("Kjøp gavekort på fixit.no", gk, bestill="felles", plassering="gavekort-cta"))
                     + '<p class="muted small">Leter du etter en gave til? Produktene vi bruker i stolen finner du på <a href="/produkter/">produktsiden</a> og i nettbutikken j-kshop.no.</p>')
    body = hero + slik + info + bunn
    return L.page(ctx, path="/gavekort/", title="Gavekort til barbershop | J&K Barber Shop",
                  description="Gi bort en time hos barbereren. Gavekort fra J&K Barber Shop har valgfritt beløp, gjelder i alle avdelinger, kjøpes på nett og sendes til mottakeren på e-post.",
                  body=body, breadcrumbs=[("Gavekort", None)], jsonld=[L.faq_jsonld(faq_items)], active="gavekort", bestill_url=gk)


# ---------- /produkter/ ----------

PRODUKTER = [
    ("Styling", [
        ("Reuzel", "reuzel", "Reuzel kommer fra Schorem Barbershop i Rotterdam, en av verdens mest kjente barbershops, og er laget av barberere for barberere. Pomadene finnes i vannbasert (lett å vaske ut) og fettbasert (holder hele dagen), i ulike grader av glans og hold. Vi bruker Reuzel Fiber og Clay Matte til teksturerte klipp og Reuzel Blue til slickback. Grooming Tonic er favoritten vår til føning. Skjeggbalm og skjeggolje fra Reuzel brukes etter skjeggtrim.",
         "Start med en mengde på størrelse med en ert, varm den i hendene og jobb den inn bakfra og frem."),
        ("Uppercut Deluxe", "uppercut-deluxe", "Uppercut Deluxe er australsk pomade og styling, startet av barberere og laget for klassiske herreklipp med hold som varer hele dagen. Vi bruker Deluxe Pomade til slickback og side part, og Matt Clay og Featherweight til teksturerte klipp med naturlig finish.",
         "Pomaden er vannbasert, så den vaskes ut med vanlig sjampo og kan jobbes om i løpet av dagen med litt vann."),
        ("Slickhaven", "slickhaven", "Slickhaven er norsk pomade og styling, laget for nordisk hår og nordisk vær. Vi bruker Slickhaven til klassiske klipp som skal holde formen fra morgen til kveld, både med glans og matt.",
         "Fordel produktet i tørt hår for mest hold, i lett fuktig hår for en mykere finish."),
        ("HUFS", "hufs", "HUFS er norsk hårstyling laget for folk som vil ha enkle produkter som fungerer. Vi bruker HUFS til hverdagsstyling med lett til medium hold, særlig på kortere klipp og teksturerte topper.",
         "Litt er nok. Varm produktet mellom hendene og legg det i håret bakfra, så unngår du klumper i panneluggen."),
    ]),
    ("Skjegg og barbering", [
        ("Proraso", "proraso", "Proraso har laget barberprodukter i Firenze siden 1948, og den grønne barberkremen med eukalyptus og mentol er en klassiker på alle barbershops. Vi bruker Proraso pre-shave og barberkrem i knivbarberingen og anbefaler den til alle som barberer seg hjemme med kniv eller høvel. Skjeggvasken og skjeggoljen fra Proraso er milde og godt egnet til daglig bruk.",
         "Den hvite serien er for sensitiv hud, den røde for grovt skjegg, den grønne for alle andre."),
        ("Taylor of Old Bond Street", "taylor-of-old-bond-street", "Taylor of Old Bond Street er britisk barberkrem og etterbarbering, laget i London siden 1854. Vi bruker barberkremene i knivbarberingen og anbefaler sandeltre-serien til deg som vil ha en klassisk, varm duft etter barberingen.",
         "Pisk kremen med kost i en skål med litt varmt vann til den blir tykk og blank, så ligger den bedre på huden."),
        ("Pan Drwal", "pan-drwal", "Pan Drwal er et polsk barbershopmerke med røtter i tømmerhoggertradisjonen, kjent for skjeggoljer, balm og voks med tydelige, maskuline dufter. Serien laget i samarbeid med Bulleit Bourbon er den mest etterspurte hos oss. Vi bruker Pan Drwal til skjeggpleie etter trim og anbefaler skjeggbørsten og kammen til alle med fullskjegg.",
         "Balm om kvelden, olje om morgenen. Da holder skjegget formen og huden under slipper å klø."),
        ("Gråbein", "graabein", "Gråbein er norske skjegg- og barberprodukter, laget for norsk klima og norske skjegg. Vi bruker Gråbein skjeggolje og balm etter skjeggtrim, og anbefaler merket til deg som vil ha skjeggpleie uten sterke dufter.",
         "To til tre dråper olje i håndflaten, gni inn mot huden under skjegget først, deretter utover i hårene."),
        ("Jobski Cosmetics", "jobski-cosmetics", "Jobski Cosmetics er skjegg- og hudpleie for menn. Vi bruker Jobski Cosmetics til pleie etter skjeggtrim og barbering, og anbefaler det til deg som vil ha enkle produkter til både skjegg og hud.",
         "Bruk skjeggproduktet på rent, tørt skjegg, og hudpleien etter barbering når huden fortsatt er lett fuktig."),
    ]),
    ("Hårpleie", [
        ("Davines", "davines", "Davines er italiensk profesjonell hårpleie med fokus på bærekraft, og merket vi bruker til vask og hodebunnspleie. Vi anbefaler Davines til deg som sliter med flass, tørr hodebunn eller fett hår, fordi serien har egne produkter for hvert problem. Stylingproduktene fra Davines (This is a-serien) er lette og egner seg godt til lengre hår og naturlig fall.",
         "Har du flass, spør om Davines Purifying-serien. Vi har sett den fungere på mange kunder."),
        ("in:on", "in-on", "in:on er hårpleie og styling til daglig bruk, med sjampo, balsam og stylingprodukter som fungerer sammen. Vi bruker in:on til vask før klipp og til lett styling, og anbefaler det til deg som vil ha én serie til hele rutinen.",
         "Bytt sjampo etter årstid: mildere om vinteren når hodebunnen er tørr, dypere rens om sommeren."),
    ]),
]

PRODUKT_BILDE_ALIAS = {"davines": "jk-barber-felles-produkter-davines.jpg"}


def render_produkter(ctx):
    s = ctx["site"]
    merke_url = dict(ctx["merker"])
    hylle = IM.picture("jk-barber-felles-produkter-harvoks.jpg", "Produkthyllen hos J&K Barber Shop", 900, 700, cls="hero-bilde", lazy=False,
                       motiv="Produkthyllen i en av salongene")
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("Produkter")}<h1>Produktene vi bruker og selger</h1>'
        f'<p class="hero-ingress">Vi bruker ikke produkter vi ikke selv vil ha i håret. De elleve merkene under står i hyllene i alle avdelingene våre, barbererne bruker dem i stolen hver dag, og du kan kjøpe dem hos oss eller i nettbutikken vår, j-kshop.no. Spør barbereren hva som passer håret og skjegget ditt.</p>'
        f'<div class="knapper">{L.btn("Handle på j-kshop.no", s["nettbutikk"])}{L.btn("Hopp til merkene", "#merker", "s")}</div>'
        '<p class="muted small">Denne siden selger ikke selv. Kjøp skjer i salongen eller på j-kshop.no.</p></div>' + hylle + '</div>',
        cls="sec-hero")

    alle = [m for _, ms in PRODUKTER for m in ms]
    hopp = '<nav class="kategorier" aria-label="Merker">' + "".join(f'<a href="#{h}">{e(n)}</a>' for n, h, _, _ in alle) + '</nav>'
    blokker = []
    for gruppe, merker in PRODUKTER:
        kort = []
        for navn, handle, tekst, tips in merker:
            url = merke_url.get(navn) or (s["nettbutikk"])
            bilde = IM.picture(PRODUKT_BILDE_ALIAS.get(handle, f"jk-barber-felles-produkt-{handle}.jpg"), f"{navn} i hyllen hos J&K Barber Shop", 600, 400,
                               cls="kort-bilde", motiv=f"{navn} i hyllen")
            kort.append(f'<article class="card produkt-merke" id="{handle}">{bilde}<div class="kort-innhold"><h3>{e(navn)}</h3><p class="muted">{tekst}</p>'
                        f'<p class="tips"><strong>Barberens tips:</strong> {tips}</p>'
                        f'<div class="kort-handling">{L.btn(f"Kjøp {e(navn)} på j-kshop.no", url, "s", size="sm")}</div></div></article>')
        blokker.append(f'<h2 class="h2-gruppe">{gruppe}</h2><div class="grid grid-2">{"".join(kort)}</div>')
    merker_sec = L.section(
        L.heading("Elleve merker, valgt av barbererne", "Rekkefølgen følger bruksområde: styling, skjegg og barbering, hårpleie.", "Merkene") + hopp + "".join(blokker),
        tone="flate", id_="merker")

    bunn = L.section(
        L.cta_box("Kjøp i salongen eller på nett", "Alt du ser her, står i hyllene i avdelingene våre. Vil du heller handle hjemmefra, finner du hele sortimentet og mer til i nettbutikken vår, j-kshop.no, med levering i hele Norge.",
                  L.btn("Gå til j-kshop.no", s["nettbutikk"]))
        + f'<p class="muted small">Vil du vite hvordan produktene brukes? Les guidene på <a href="/blogg/">bloggen</a>, eller spør barbereren neste gang du <a href="/bestill-time/">bestiller time</a>.</p>')
    body = hero + merker_sec + bunn
    base = s["base"]
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Merker hos J&K Barber Shop",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Brand", "name": n, "url": base + "/produkter/#" + h}}
                              for i, (n, h, _, _) in enumerate(alle)]}
    return L.page(ctx, path="/produkter/", title="Produktene vi bruker og selger | J&K Barber Shop",
                  description="Reuzel, Uppercut Deluxe, Proraso, Pan Drwal, Davines og flere: produktene barbererne våre bruker i stolen. Kjøp dem i salongen eller i nettbutikken j-kshop.no.",
                  body=body, breadcrumbs=[("Produkter", None)], jsonld=[ld], active="produkter")


# ---------- /jobb/ ----------

def render_jobb(ctx):
    s = ctx["site"]
    img = IM.picture("jk-barber-felles-jobb-hero.jpg", "Barberere i arbeid hos J&K Barber Shop", 900, 700, cls="hero-bilde", lazy=False,
                     motiv="Barberere som jobber side om side")
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("Jobb")}<h1>Bli barberer hos J&amp;K Barber Shop</h1>'
        '<p class="hero-ingress">Vi er en barbershopkjede med sju avdelinger i Follo, Bærum og Romerike, og vi vokser. Er du barberer eller herrefrisør som vil jobbe med faget på et sted der håndverket betyr noe, vil vi høre fra deg. Du velger selv om du vil være fast ansatt eller selvstendig med egen stol (stolleie). Og vil du en dag drive din egen J&amp;K Barber Shop, er det her veien starter: alle franchisetakere har først jobbet hos oss.</p>'
        f'<div class="knapper">{L.btn("Søk her", "#sok")}{L.btn("Send e-post", MAILTO + "?subject=Barberer", "s", external=False)}</div></div>{img}</div>',
        cls="sec-hero")

    faar = [("Kunder fra dag én.", "Avdelingene våre har fulle bøker og over tusen anmeldelser på Google. Du starter ikke med tom kalender."),
            ("Booking, app og markedsføring.", "Fixit-booking, J&amp;K-appen med stempelkort, Google-profiler og annonsering er på plass. Du klipper, vi fyller stolen."),
            ("Produkter til innkjøpspris.", "Gjennom J&amp;K Shop får du tilgang til Reuzel, Uppercut Deluxe, Proraso, Pan Drwal, Davines og flere til priser få andre har."),
            ("Faglig utvikling.", "Interne kurs i skin fade, skjeggdesign og knivbarbering, og et nivåsystem (Lærling, Junior, Barber, Senior) der du rykker opp i pris når du rykker opp i nivå."),
            ("Kolleger som kan faget.", "Du jobber med barberere som bryr seg om resultatet, og som deler teknikker."),
            ("Fleksibilitet.", "Sju avdelinger betyr muligheter for å bytte avdeling, jobbe ekstra et annet sted eller flytte nærmere der du bor.")]
    faar_html = "".join(f'<div class="grunn"><h3>{t}</h3><p class="muted">{x}</p></div>' for t, x in faar)
    dette = L.section('<h2 class="h2-bred">Dette får du hos oss</h2><div class="grid grid-3 grunner">' + faar_html + "</div>", tone="flate", id_="dette-far-du")

    spor = L.section(
        L.heading("To spor: ansatt eller selvstendig", "Usikker på hva som passer deg? Skriv det i søknaden, så tar vi en prat. Vilkårene går vi gjennom i samtalen, vi publiserer ikke tall på nettsiden.", "Tilknytning")
        + '<div class="grid grid-2">'
        f'<div class="card kort-stor"><h3>Fast ansatt</h3><p class="muted">Du er ansatt i {e(s["juridisk"])} med lønn, feriepenger, pensjon og forsikring. Vi tar oss av regnskap, markedsføring og vaktplan. Du tar deg av kundene. Passer deg som vil ha forutsigbarhet og et team rundt deg.</p></div>'
        '<div class="card kort-stor"><h3>Selvstendig med egen stol (stolleie)</h3><p class="muted">Du leier stol hos oss og driver som selvstendig næringsdrivende. Du får booking, app, kunder, produkter og markedsføring gjennom J&amp;K, men driver eget firma og bestemmer selv over tid og timeplan. Passer deg som allerede har eget enkeltpersonforetak eller AS, eller som vil ha det.</p></div>'
        '</div>', id_="to-spor")

    ser = ["Svennebrev som frisør eller dokumentert erfaring som barberer.",
           "Solid på herreklipp. Skin fade, skjegg og kniv er en fordel, og vi lærer deg resten.",
           "Du liker folk, holder avtaler og tar faget på alvor.",
           "Norsk eller engelsk muntlig. Flere språk er en fordel i avdelingene våre.",
           "Under utdanning? Vi er ikke godkjent lærebedrift ennå, men vi jobber mot å bli det. Ta gjerne kontakt likevel, så forteller vi hva vi kan tilby i dag."]
    opplaering = IM.picture("jk-barber-felles-jobb-opplaering.jpg", "Seniorbarberer lærer opp lærling hos J&K Barber Shop", 800, 520, cls="bilde-rund",
                            motiv="Seniorbarberer lærer opp lærling")
    krav = L.section(
        f'<div class="split split-center"><div><div class="sec-head">{L.eyebrow("Dette ser vi etter")}<h2>Hvem vi leter etter</h2></div><ul class="hake-liste">' + "".join(f"<li>{x}</li>" for x in ser) + '</ul>'
        f'<p class="muted"><strong>Ledige stillinger:</strong> Vi tar imot åpne søknader til alle avdelinger, både til ansettelse og stolleie. Skriv hvilken avdeling du helst vil jobbe i.</p>'
        f'<p class="muted">{s["regel0"]}</p></div>{opplaering}</div>',
        tone="mork", id_="krav")

    avd_opts = [avd_option(a)[0] for a in ctx["avdelinger"]]
    felter = (
        felt("navn_7pb7rx", "Fullt navn", required=True, autocomplete="name")
        + '<div class="felt-rad">' + felt("telefon_tzs0xj", "Telefon", type_="tel", required=True, autocomplete="tel")
        + felt("e_post_7w4sea", "E-post", type_="email", required=True, autocomplete="email") + "</div>"
        + valg("onsket_avdeling_h1rtid", "Hvilken avdeling ønsker du å jobbe i?", avd_opts, hint="Kryss av én eller flere.")
        + nedtrekk("erfaring_som_barberer_eller_frisor_pjh5wz", "Erfaring som barberer eller frisør", ["Under 1 år", "1 til 3 år", "3 til 5 år", "Over 5 år"], required=True)
        + valg("har_du_fagbrev_mpbucg", "Har du fagbrev?", ["Ja", "Nei", "Under utdanning"], type_="radio", required=True)
        + tekstfelt("fortell_kort_om_deg_selv_82l8ni", "Fortell kort om deg selv", required=True,
                    hint="Hva er du best på, ønsket tilknytning (fast ansatt eller egen stol), og hvorfor du vil jobbe hos J&amp;K.")
        + felt("lenke_til_cv_eller_portefolje_valgfritt_hy5u1q", "Lenke til CV eller portefølje (valgfritt)", type_="url", placeholder="https://",
               hint="Lenke til CV (for eksempel i OneDrive, Google Drive eller Dropbox), Instagram eller en portefølje med bilder av arbeidet ditt.")
        + samtykke("jeg_samtykker_til_at_j_k_barber_shop_lag_uj9xfs",
                   'Jeg samtykker til at J&amp;K Barber Shop lagrer opplysningene i søknaden i forbindelse med rekruttering. Søknader slettes senest seks måneder etter at prosessen er avsluttet. Les <a href="/personvern/">personvernerklæringen</a>.')
    )
    sok = L.section(
        f'<div class="split split-start split-16"><div class="sec-head">{L.eyebrow("Søk her")}<h2>Send søknad</h2>'
        '<p class="lead muted">Vi leser alle søknader og tar kontakt med dem vi vil snakke mer med. Du hører fra oss uansett.</p>'
        f'<p class="muted small">Vil du heller sende e-post? Send CV og noen ord til <a href="{MAILTO}?subject=Barberer">{s["epost"]}</a> med emne "Barberer".</p></div>'
        + skjema(s["forms"]["jobb"], "jobb", felter, "Send søknad", "Takk for søknaden.", "Vi leser alle søknader og tar kontakt. Hilsen J&amp;K Barber Shop.")
        + "</div>", tone="flate", id_="sok")

    bunn = L.section(L.cta_box("Vil du drive din egen J&amp;K Barber Shop?", "Alle franchisetakere har først jobbet hos oss. Les hvordan veien ser ut.", L.btn("Les om franchise", "/franchise/", "s")))
    body = hero + dette + spor + krav + sok + bunn
    return L.page(ctx, path="/jobb/", title="Bli barberer hos oss | J&K Barber Shop",
                  description="Vil du jobbe i en etablert barbershopkjede? J&K Barber Shop søker barberere til sju avdelinger, som fast ansatt eller selvstendig med egen stol. Søk her.",
                  body=body, breadcrumbs=[("Jobb", None)], active=None)


# ---------- /franchise/ ----------

def render_franchise(ctx):
    s = ctx["site"]
    img = IM.picture("jk-barber-felles-interior-2025.jpg", "Interiørkonseptet til J&K Barber Shop med mørkt tre og messing", 900, 700, cls="hero-bilde", lazy=False)
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("Franchise")}<h1>Franchise med J&amp;K Barber Shop</h1>'
        '<p class="hero-ingress">Vil du drive din egen barbershop uten å starte fra null? J&amp;K Barber Shop tilbyr franchise til barberere som vil bygge noe eget under et navn kundene allerede kjenner. Du får konseptet, systemene, innkjøpsavtalene og markedsføringen. Du driver avdelingen. Veien dit starter alltid med at du jobber hos oss først.</p>'
        f'<div class="knapper">{L.btn("Ta kontakt", "#skjema")}{L.btn("Ring " + s["telefonVisning"], "tel:" + s["telefon"], "s", external=False)}</div></div>{img}</div>',
        cls="sec-hero")

    konsept = L.section(
        L.heading("Konseptet", "J&amp;K Barber Shop er en premium barbershop etablert i 2018, med sju avdelinger i Follo, Bærum og Romerike. Konseptet er gjennomprøvd: mørkt interiør med messing, barberere på fire tydelige nivåer, konsultasjon før hver behandling, digitalt stempelkort i egen app, og en produktportefølje gjennom J&amp;K Shop. Flere av avdelingene våre drives i dag som franchise av barberere som startet hos oss. " + s["regel0"], "Dette er J&amp;K")
        + f'<div class="knapper">{L.btn("Les om oss", "/om-oss/", "s")}{L.btn("Se avdelingene", "/avdelinger/", "s")}</div>',
        tone="flate", id_="konseptet")

    faar = [("Merkevare og konsept.", "Navn, logo, interiørkonsept, tjenestemeny, prisstruktur og nivåsystem."),
            ("Booking og app.", "Fixit-booking med egen avdelings-ID, J&amp;K-appen med stempelkort som gjelder på tvers av kjeden, Google-profil satt opp etter vår standard."),
            ("Innkjøp.", "Tilgang til J&amp;K Shops innkjøpsavtaler på Reuzel, Uppercut Deluxe, Proraso, Pan Drwal, Davines og flere, både til bruk i salong og videresalg."),
            ("Markedsføring.", "Felles nettside med egen avdelingsside, Google Ads og sosiale medier, kampanjer og senteraktiviteter."),
            ("Opplæring.", "Oppstartsprogram for deg og teamet ditt, fagkurs, driftsrutiner (åpning, stenging, hygiene, kundehåndtering) og tilgang til erfarne avdelingsledere."),
            ("Rekrutteringshjelp.", "Vi hjelper deg å finne barberere gjennom kanalene våre."),
            ("Lokaler.", "Hjelp til å vurdere og forhandle leiekontrakt, med erfaring fra Thon-sentre og andre kjøpesentre.")]
    faar_html = "".join(f'<div class="grunn"><h3>{t}</h3><p class="muted">{x}</p></div>' for t, x in faar)
    dette = L.section('<h2 class="h2-bred">Dette får du som franchisetaker</h2><div class="grid grid-3 grunner">' + faar_html + "</div>", id_="dette-far-du")

    forventer = [("Seks måneder hos oss først.", "Alle som vil bli franchisetaker, jobber minst seks måneder som barberer i en av avdelingene våre før vi tar stilling til videre godkjenning. Da lærer du konseptet innenfra, kundene og teamet blir kjent med deg, og begge parter vet hva de går til. Dette gjelder uansett hvor mye erfaring du har fra før."),
                 ("Erfaring som barberer,", "og solid på herreklipp, skin fade og skjegg."),
                 ("Vilje til å følge konseptet:", "standard på tjenester, priser, produkter og kundeopplevelse."),
                 ("Et lokale eller en idé om sted.", "Vi ser først og fremst etter partnere i nærområdet vårt: Follo, Asker og Bærum og Romerike. Har du et godt sted og en god plan et annet sted, er vi åpne for det også."),
                 ("Eget selskap", "som inngår franchiseavtale med oss.")]
    forv_html = "".join(f'<li><strong>{t}</strong> {x}</li>' for t, x in forventer)
    steg = ["Fyll ut skjemaet under, eller søk jobb hos oss via jobbsiden og skriv at du vil bli franchisetaker på sikt.",
            "Vi ringer deg innen en uke for en første prat.",
            "Møte hos oss i Ski eller i en av avdelingene, der du ser konseptet i drift.",
            "Du jobber hos J&amp;K i minst seks måneder, som ansatt eller med egen stol.",
            "Videre godkjenning: gjennomgang av økonomi, lokale og avtale.",
            "Signering, oppstartsprogram og åpning."]
    steg_html = "".join(f'<div class="steg"><div class="steg-num">{i + 1}</div><div><p>{x}</p></div></div>' for i, x in enumerate(steg))
    krav = L.section(
        f'<div class="split split-start"><div><div class="sec-head">{L.eyebrow("Dette forventer vi av deg")}<h2>Forutsetningene</h2></div><ol class="kvalitet">{forv_html}</ol>'
        f'<div class="card info-kort info-messing"><div class="info-tittel">Økonomi</div><p>Hva avtalen koster, hva som er inkludert, og hvordan økonomien i en avdeling henger sammen, går vi gjennom i et møte når du har jobbet hos oss en stund. Vi publiserer ikke tall på nettsiden.</p></div></div>'
        f'<div><div class="sec-head">{L.eyebrow("Slik går du frem")}<h2>Seks steg til egen avdeling</h2></div><div class="steg-liste">{steg_html}</div></div></div>',
        tone="mork", id_="forventninger")

    felter = (
        felt("navn_24rehu", "Fullt navn", required=True, autocomplete="name")
        + felt("firma_6y29cs", "Firma (valgfritt)", autocomplete="organization", hint="Har du eget selskap i dag, skriv navnet her.")
        + '<div class="felt-rad">' + felt("telefon_o5lnov", "Telefon", type_="tel", required=True, autocomplete="tel")
        + felt("e_post_q52elm", "E-post", type_="email", required=True, autocomplete="email") + "</div>"
        + felt("onsket_omrade_4o5eqs", "Hvor ønsker du å åpne?", required=True, placeholder="By eller sted", hint="Skriv gjerne om du har lokale, eller bare en idé om sted.")
        + tekstfelt("erfaring_fra_bransjen_27ejxk", "Erfaring fra bransjen", required=True,
                    hint="Bakgrunn (barberer eller frisør, driver salong i dag, jobber hos J&amp;K i dag), og når du ser for deg oppstart.")
        + tekstfelt("melding_1b49o1", "Fortell kort om deg og planene dine (valgfritt)")
        + samtykke("jeg_samtykker_til_at_j_k_barber_shop_lag_n7xkp3")
    )
    sk = L.section(
        f'<div class="split split-start split-16"><div class="sec-head">{L.eyebrow("Kontaktskjema")}<h2>Fortell oss om stedet ditt</h2>'
        '<p class="lead muted">Vi tar kontakt innen en uke.</p>'
        f'<p class="muted small">Heller e-post? Skriv til <a href="{MAILTO}?subject=Franchise">{s["epost"]}</a> med emne "Franchise".</p></div>'
        + skjema(s["forms"]["franchise"], "franchise", felter, "Send henvendelse", "Takk.", "Vi tar kontakt innen en uke. Hilsen J&amp;K Barber Shop.")
        + "</div>", tone="flate", id_="skjema")
    bunn = L.section(L.cta_box("Ikke klar for egen avdeling ennå?", "Start med å jobbe hos oss, som ansatt eller med egen stol. Det er uansett første steg.", L.btn("Les om jobb hos oss", "/jobb/", "s")))
    body = hero + konsept + dette + krav + sk + bunn
    return L.page(ctx, path="/franchise/", title="Franchise: åpne din egen barbershop | J&K Barber Shop",
                  description="Start barbershop med et etablert konsept: J&K Barber Shop tilbyr franchise med innkjøpsavtaler, app, booking og markedsføring. Les mer og ta kontakt.",
                  body=body, breadcrumbs=[("Franchise", None)], active=None,
                  og_image=IM.url("jk-barber-felles-interior-2025.jpg", 1200, 630))


# ---------- /kontakt/ ----------

def render_kontakt(ctx):
    s = ctx["site"]
    img = IM.picture("jk-barber-asenveien-fasade.jpg", "J&K Barber Shop hovedkontor i Åsenveien 3, Ski", 900, 700, cls="hero-bilde", lazy=False)
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("Kontakt")}<h1>Kontakt oss</h1>'
        '<p class="hero-ingress">Spørsmål om time, gavekort, app, produkter eller samarbeid? Her finner du oss. Timebestilling gjør du raskest på nett eller i appen.</p>'
        f'<div class="knapper">{L.btn("Ring " + s["telefonVisning"], "tel:" + s["telefon"], external=False)}{L.btn("Send e-post", MAILTO, "s", external=False)}{L.btn("Bestill time", "/bestill-time/", "s", bestill="felles", plassering="kontakt-hero")}</div></div>{img}</div>',
        cls="sec-hero")

    nap = L.section(
        '<div class="grid grid-3">'
        f'<div class="card kort-stor">{L.eyebrow("Telefon og e-post")}<h2>Snakk med oss</h2><p>Telefon <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a>, felles for alle avdelinger. Betjent i åpningstiden til avdelingene.</p>'
        f'<p>E-post <a href="{MAILTO}">{s["epost"]}</a>. Vi svarer innen én virkedag.</p><p class="muted small">Timebestilling gjøres raskest på <a href="/bestill-time/">bestill time</a> eller i <a href="/app/">appen</a>.</p></div>'
        f'<div class="card kort-stor">{L.eyebrow("Hovedkontor")}<h2>{e(s["juridisk"])}</h2><p>Åsenveien 3<br>1400 Ski<br>Org.nr. {e(s["orgnr"])}</p><p class="muted small">Samme adresse som avdelingen i Åsenveien 3. Post og fakturaer sendes hit.</p></div>'
        f'<div class="card kort-stor">{L.eyebrow("Presse, samarbeid og leverandører")}<h2>Samarbeid</h2><p>Henvendelser om samarbeid, sponsing, senteraktiviteter eller leveranser: <a href="{MAILTO}">{s["epost"]}</a>, merk emnet.</p>'
        '<p class="muted small">Franchise: se <a href="/franchise/">franchise</a>. Jobb: se <a href="/jobb/">jobb hos oss</a>.</p></div>'
        '</div>', tone="flate", id_="telefon")

    rader = []
    for a in ctx["avdelinger"]:
        rader.append(f'<div class="card info-kort"><div class="info-tittel"><a href="{a["url"]}">{e(avd_navn(a))}</a></div>'
                     f'<p>{e(a["gateadresse"])}, {e(a["postnummer"])} {e(a["poststed"])}<br>{e(plass_kort(a))}</p>'
                     f'<p class="muted">{apningstider_kort(a)}</p>'
                     f'<div class="kort-handling">{L.btn("Bestill time", a["fixitUrl"], "s", size="sm", bestill=a["ga4Avdeling"], plassering="kontakt-liste")}<a href="{e(a["mapsUrl"])}" target="_blank" rel="noopener">Veibeskrivelse</a></div></div>')
    avd = L.section(
        L.heading("Avdelinger", "Alle avdelingene har samme telefonnummer. Åpningstidene følger senteret.", "Sju avdelinger")
        + f'<div class="grid grid-3">{"".join(rader)}</div><p class="muted small"><a href="/avdelinger/">Se alle avdelinger med kart</a></p>', id_="avdelinger")

    opts = [avd_option(a) for a in ctx["avdelinger"]] + [("Hovedkontor", "hovedkontor")]
    felter = (
        felt("navn_6w8yvk", "Navn", required=True, autocomplete="name")
        + '<div class="felt-rad">' + felt("e_post_sstfv7", "E-post", type_="email", required=True, autocomplete="email")
        + felt("telefon_psecma", "Telefon (valgfritt)", type_="tel", autocomplete="tel") + "</div>"
        + nedtrekk("avdeling_r5b10m", "Gjelder avdeling", opts, required=True, avd_velger=True, tom="Velg avdeling", hint="Gjelder det noe generelt, velg Hovedkontor.")
        + tekstfelt("melding_rjikoj", "Melding", required=True, hint="Skriv gjerne hva det gjelder: time, gavekort, app og stempelkort, produkter, tilbakemelding, samarbeid eller annet.")
        + samtykke("jeg_samtykker_til_at_j_k_barber_shop_lag_2vm5q7")
    )
    sk = L.section(
        f'<div class="split split-start split-16"><div class="sec-head">{L.eyebrow("Send oss en melding")}<h2>Skriv til oss</h2><p class="lead muted">Vi svarer innen én virkedag. Gjelder det en time, er det raskere å ringe avdelingen på fellesnummeret.</p>'
        f'<p class="muted small">Har du vært hos oss og vil fortelle hvordan det var? Vi leser alt. <a href="/tilbakemelding/">Gi tilbakemelding</a>, eller legg igjen en anmeldelse på Google for avdelingen du besøkte.</p></div>'
        + skjema(s["forms"]["kontakt"], "kontakt", felter, "Send melding", "Takk for meldingen.", "Vi svarer innen én virkedag.")
        + "</div>", tone="flate", id_="skjema")
    body = hero + nap + avd + sk
    base = s["base"]
    ld = {"@context": "https://schema.org", "@type": "ContactPage", "@id": base + "/kontakt/#contactpage", "url": base + "/kontakt/",
          "name": "Kontakt J&K Barber Shop", "inLanguage": "nb-NO", "mainEntity": {"@id": base + "/#organization"}}
    return L.page(ctx, path="/kontakt/", title="Kontakt og adresser | J&K Barber Shop",
                  description="Telefon, e-post og adresser til alle J&K Barber Shop-avdelinger, pluss hovedkontor i Åsenveien 3, Ski. Spørsmål om time, gavekort, app eller samarbeid.",
                  body=body, breadcrumbs=[("Kontakt", None)], jsonld=[ld], active=None,
                  og_image=IM.url("jk-barber-asenveien-fasade.jpg", 1200, 630))


# ---------- /hjemmebarbering/ ----------

HJEMME_PRISER = [("Klassisk herreklipp", 639), ("Skin fade", 825), ("Pensjonistklipp", 550), ("Skjeggtrim", 579),
                 ("Knivbarbering", 529), ("Hodebarbering", 529), ("Kombo I (klipp og skjegg)", 1029), ("Kombo II (skin fade og skjegg)", 1299)]
HJEMME_OMRADER = ["Sandvika", "Oslo", "Asker", "Drammen"]


def render_hjemmebarbering(ctx):
    s = ctx["site"]
    img = IM.picture("jk-barber-felles-hjemmebarbering.jpg", "Barberer fra J&K Barber Shop klipper hjemme hos kunde", 900, 700, cls="hero-bilde", lazy=False,
                     motiv="Barberer klipper hjemme hos kunde")
    hero = L.section(
        f'<div class="split split-center hero-split"><div class="hero-tekst">{L.eyebrow("Hjemmebarbering")}<h1>Mobil barbering hjemme hos deg</h1>'
        '<p class="hero-ingress">Vi kommer hjem til deg, til kontoret, til sykehjemmet eller til hotellet, med alt utstyr. Klassisk herreklipp, skin fade, skjeggtrim og knivbarbering i Sandvika, Oslo, Asker og Drammen, andre områder på forespørsel. Send forespørsel, så bekrefter vi tid og pris.</p>'
        f'<p class="regel0">{s["regel0"]}</p>'
        f'<div class="knapper">{L.btn("Send forespørsel", "#skjema")}{L.btn("Ring " + s["telefonVisning"], "tel:" + s["telefon"], "s", external=False)}</div>'
        '<p class="muted small">Bestilles minst 24 timer før. 100 % tillegg på søn- og helligdager.</p></div>' + img + '</div>',
        cls="sec-hero")

    steg = [("Send forespørsel", "Fyll ut skjemaet under med ønsket behandling, dato, tid og adresse."),
            ("Vi bekrefter", "Vi bekrefter tid og pris på telefon eller e-post. Først da er avtalen bindende."),
            ("Barbereren kommer", "Til avtalt tid, med alt utstyr. Du trenger bare en stol og en stikkontakt.")]
    steg_html = "".join(f'<div class="steg"><div class="steg-num">{i + 1}</div><div><div class="steg-tittel">{t}</div><p class="muted">{x}</p></div></div>' for i, (t, x) in enumerate(steg))
    rader = "".join(L.pris_rad(n, p) for n, p in HJEMME_PRISER)
    slik = L.section(
        f'<div class="split split-start"><div><div class="sec-head">{L.eyebrow("Slik fungerer det")}<h2>Tre steg</h2></div><div class="steg-liste">{steg_html}</div>'
        '<p class="muted" style="margin-top:20px">Hjemmebarbering må bestilles minst 24 timer før. Prisene er høyere enn i salong fordi de dekker kjøretid, utstyr og én barberer dedikert til deg.</p></div>'
        f'<div><div class="sec-head">{L.eyebrow("Priser")}<h2>Faste priser hjemme hos deg</h2></div><div class="card pristabell-kort"><div class="rows">{rader}</div></div>'
        '<p class="muted small" style="margin-top:14px">100 % tillegg på søn- og helligdager. Alle priser inkludert mva. Prisene er faste og gjelder uavhengig av barberens nivå. Prisen bekreftes sammen med tidspunktet før barbereren kommer.</p></div></div>',
        tone="flate", id_="priser")

    hvem = L.section(
        '<div class="grid grid-3">'
        f'<div class="card kort-stor">{L.eyebrow("Hvor vi kommer")}<h2>Områder</h2><p>{", ".join(HJEMME_OMRADER[:-1])} og {HJEMME_OMRADER[-1]}. Andre områder på forespørsel, skriv adressen i skjemaet så svarer vi.</p></div>'
        f'<div class="card kort-stor">{L.eyebrow("Privat")}<h2>Hjemme</h2><p>Familier som vil ha alle klippet hjemme samme dag, eldre og andre som har vanskelig for å komme seg til salongen, gaver, og små grupper (bursdag, utdrikningslag, før bryllupet).</p></div>'
        f'<div class="card kort-stor">{L.eyebrow("Bedrift")}<h2>På jobben</h2><p>Klipp og barbering på kontoret, events, kickoff og personalgoder. Vi setter opp en eller flere barberere etter antall.</p></div>'
        '</div>', id_="for-hvem")

    tj_opts = ["Klassisk herreklipp", "Skin fade", "Skjeggtrim", "Knivbarbering", "Kombo: klipp og skjegg", "Barneklipp", "Annet"]
    felter = (
        felt("navn_ow9fud", "Navn", required=True, autocomplete="name")
        + '<div class="felt-rad">' + felt("telefon_zr4yg3", "Mobil", type_="tel", required=True, autocomplete="tel")
        + felt("e_post_jyhm5a", "E-post (valgfritt)", type_="email", autocomplete="email") + "</div>"
        + felt("adresse_eller_omrade_kj3tzh", "Adresse eller område", required=True, autocomplete="street-address", hint="Dit barbereren skal komme.")
        + '<div class="felt-rad">' + felt("onsket_dato_lpuejr", "Ønsket dato", type_="date", required=True, hint="Minst 24 timer frem i tid.")
        + nedtrekk("tjeneste_3erwog", "Ønsket behandling", tj_opts, required=True, hint="Flere behandlinger eller personer? Skriv det i kommentaren.") + "</div>"
        + tekstfelt("melding_1196g3", "Kommentar (valgfritt)", hint="Ønsket tidspunkt, antall personer, bedrift eller privat, annet vi bør vite.")
        + '<label class="samtykke"><input type="checkbox" required> <span>Jeg har lest vilkårene: bestilling minst 24 timer før, 100 % tillegg på søn- og helligdager, og J&amp;K bekrefter tid og pris før avtalen er bindende. Opplysningene behandles etter <a href="/personvern/">personvernerklæringen</a>.</span></label>'
    )
    sk = L.section(
        f'<div class="split split-start split-16"><div class="sec-head">{L.eyebrow("Forespørselsskjema")}<h2>Send forespørsel</h2>'
        '<p class="lead muted">Vi bekrefter tid og pris så snart vi kan, senest innen én virkedag.</p>'
        f'<p class="muted small">Foretrekker du salong? <a href="/avdelinger/">Se alle avdelingene</a> eller <a href="/tjenester/">prisene i salong</a>.</p></div>'
        + skjema(s["forms"]["hjemmebarbering"], "hjemmebarbering", felter, "Send forespørsel", "Takk for forespørselen.", "Vi bekrefter tid og pris så snart vi kan, senest innen én virkedag.")
        + "</div>", tone="flate", id_="skjema")
    body = hero + slik + hvem + sk
    base = s["base"]
    ld = {"@context": "https://schema.org", "@type": "Service", "@id": base + "/hjemmebarbering/#service", "name": "Hjemmebarbering",
          "serviceType": "Mobil barbering og herreklipp hjemme hos kunden", "url": base + "/hjemmebarbering/",
          "provider": {"@id": base + "/#organization"}, "areaServed": [{"@type": "City", "name": o} for o in HJEMME_OMRADER],
          "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Priser hjemmebarbering",
                              "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}, "price": str(p), "priceCurrency": "NOK"} for n, p in HJEMME_PRISER]}}
    return L.page(ctx, path="/hjemmebarbering/", title="Hjemmebarbering: barber hjem til deg | J&K Barber Shop",
                  description="Profesjonell herreklipp, skin fade og barbering hjemme eller på jobb i Bærum, Asker, Oslo og Drammen. Send forespørsel, vi svarer med ledig tid og pris.",
                  body=body, breadcrumbs=[("Tjenester og priser", "/tjenester/"), ("Hjemmebarbering", None)], jsonld=[ld], active="tjenester",
                  bestill_url="/hjemmebarbering/#skjema")


# ---------- /bestill-time/ ----------

def render_bestill(ctx):
    s = ctx["site"]
    kort = []
    for a in ctx["avdelinger"]:
        kort.append(f'<article class="card kort-stor bestill-kort" data-avd-kort="{a["slug"]}"><h2>{e(avd_navn(a))}</h2>'
                    f'<p class="muted small">{e(a["gateadresse"])}. {e(plass_kort(a))}.<br>{apningstider_kort(a)}</p>'
                    f'<div class="kort-handling">{L.btn(e(a["bestillKnapp"]), a["fixitUrl"], bestill=a["ga4Avdeling"], plassering="bestill-time")}<a href="{a["url"]}">Om avdelingen</a></div></article>')
    hero = L.section(
        f'<div class="sec-head sec-head-stor">{L.eyebrow("Velg avdeling")}<h1>Bestill time</h1>'
        '<p class="lead muted">Velg avdeling, så kommer du rett til bookingen. Der velger du behandling, barberer og tidspunkt, og ser prisen før du bekrefter. Det tar under ett minutt.</p></div>'
        f'<div class="grid grid-3">{"".join(kort)}</div>'
        f'<p class="muted small">Bookingen åpnes i ny fane hos Fixit, bookingsystemet vårt. {s["regel0"].split(". ")[0]}.</p>',
        cls="sec-hero", id_="avdelinger")

    app = L.section(
        f'<div class="rad-mellom"><div class="sec-head">{L.eyebrow("Heller i appen?")}<h2>Booking, stempelkort og kuponger samlet</h2>'
        '<p class="lead muted">Last ned J&amp;K-appen, så har du bookingen, stempelkortet og kupongene på ett sted. Hvert 10. stempel gir behandlingen gratis. <a href="/app/">Les om appen</a>.</p></div>'
        f'<div class="knapper">{L.btn("App Store", s["appStore"], "s", aria_label="Last ned J&K Barber Shop-appen på App Store")}{L.btn("Google Play", s["googlePlay"], "s", aria_label="Last ned J&K Barber Shop-appen på Google Play")}</div></div>',
        tone="flate", id_="app")

    godt = ["Avbestill eller flytt timen senest 24 timer før. Det gjør du i bekreftelsen du fikk på SMS eller e-post, i appen, eller ved å ringe oss.",
            "Du velger barberer selv i bookingen, og ser nivå og pris før du bekrefter.",
            "Hårvask inngår i klipp på alle nivåer. Du velger selv om du vil ha vask.",
            'Du betaler i salongen etter behandlingen, med kort eller Vipps i kassen. <a href="/gavekort/">Gavekort</a> brukes som betaling i kassen.',
            "Drop-in tar vi imot når vi har ledig, men timebestilling går alltid foran.",
            "Kommer du for sent, gi beskjed på telefon, så ser vi hva vi får til.",
            f'Spørsmål? Ring <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a> eller send e-post til <a href="{MAILTO}">{s["epost"]}</a>.']
    info = L.section(
        f'<div class="split split-start"><div class="sec-head">{L.eyebrow("Godt å vite")}<h2>Før timen</h2><p class="lead muted">{s["prisSetning"]}</p></div>'
        '<ul class="hake-liste">' + "".join(f"<li>{x}</li>" for x in godt) + '</ul></div>', id_="godt-a-vite")
    body = hero + app + info
    base = s["base"]
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Bestill time hos J&K Barber Shop",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"J&K Barber Shop {a['title']}", "url": a["fixitUrl"]} for i, a in enumerate(ctx["avdelinger"])]}
    return L.page(ctx, path="/bestill-time/", title="Bestill time hos barber | J&K Barber Shop",
                  description="Velg avdeling og bestill time på få sekunder: Sandvika, Ski, Åsenveien 3, Kolbotn, Jessheim, Strømmen og Rykkinn. Du velger barberer og tidspunkt selv.",
                  body=body, breadcrumbs=[("Bestill time", None)], jsonld=[ld], active=None, bestill_url="/bestill-time/#avdelinger")


# ---------- /personvern/ ----------

def render_personvern(ctx):
    s = ctx["site"]
    deler = [
        ("Behandlingsansvarlig", f"<p>{e(s['juridisk'])}, org.nr. {e(s['orgnr'])}, Åsenveien 3, 1400 Ski, er behandlingsansvarlig for personopplysninger som samles inn på j-kbarber.no og i salongene våre. Spørsmål om personvern sendes til <a href=\"{MAILTO}?subject=Personvern\">{s['epost']}</a> eller på telefon <a href=\"tel:{s['telefon']}\">{s['telefonVisning']}</a>.</p>"),
        ("Hvilke opplysninger vi behandler, og hvorfor",
         "<p><strong>Kontaktskjema og e-post.</strong> Navn, e-post, telefon, valgt avdeling og meldingen din. Brukes til å svare på henvendelsen. Grunnlag: vår berettigede interesse i å svare deg (GDPR artikkel 6 nr. 1 bokstav f). Slettes når saken er avsluttet, senest etter tolv måneder.</p>"
         "<p><strong>Jobbsøknader.</strong> Navn, kontaktopplysninger, erfaring, fagbrev, det du skriver om deg selv og eventuelle lenker til CV eller portefølje. Brukes til rekruttering. Grunnlag: samtykket du gir i skjemaet (artikkel 6 nr. 1 bokstav a). Søknader slettes når rekrutteringen er avsluttet, senest seks måneder etter, med mindre du ber oss beholde søknaden lenger.</p>"
         "<p><strong>Franchisehenvendelser.</strong> Navn, firma, kontaktopplysninger, ønsket område og det du skriver om bakgrunn og planer. Brukes til å vurdere og følge opp henvendelsen. Grunnlag: samtykke og tiltak før en eventuell avtale (artikkel 6 nr. 1 bokstav a og b). Slettes senest tolv måneder etter siste kontakt dersom det ikke blir noen avtale.</p>"
         "<p><strong>Forespørsler om hjemmebarbering.</strong> Navn, telefon, e-post, adresse eller område, ønsket dato og behandling. Brukes til å bekrefte tid og pris og gjennomføre oppdraget. Grunnlag: tiltak før og oppfyllelse av avtale (artikkel 6 nr. 1 bokstav b). Oppbevares så lenge bokføringsloven krever for gjennomførte oppdrag, ellers slettes forespørselen senest etter tolv måneder.</p>"
         "<p><strong>Tilbakemeldinger.</strong> Sendes som e-post til oss. Vi bruker dem til å forbedre tjenesten og svarer deg hvis du ber om det. Slettes senest etter tolv måneder.</p>"),
        ("Skjemaer og databehandlere",
         "<p>Skjemaene på nettsiden leveres av Wix (Wix.com Ltd.), som lagrer innsendingene på vegne av oss og er vår databehandler. Nettsiden er også driftet hos Wix. Wix kan behandle opplysninger utenfor EØS; overføringen er sikret med EU-kommisjonens standardavtaler. Vi har databehandleravtale med leverandørene vi bruker, og de kan ikke bruke opplysningene til egne formål.</p>"
         "<p>E-post håndteres i Microsoft 365. Innsendinger fra skjemaene varsles til oss på e-post.</p>"),
        ("Timebestilling hos Fixit",
         "<p>Når du bestiller time, gjør du det i bookingsystemet Fixit (fixit.no), som åpnes i en egen fane. Fixit er selvstendig behandlingsansvarlig for opplysningene du gir der, for eksempel navn, mobilnummer og bestillingshistorikk, og har sin egen personvernerklæring på <a href=\"https://fixit.no\" target=\"_blank\" rel=\"noopener\">fixit.no</a>. Vi får tilgang til bestillingen din for å gjennomføre timen og sende påminnelse. Gavekort kjøpes også gjennom Fixit.</p>"),
        ("J&amp;K-appen",
         "<p>Appen leveres av en ekstern apputvikler på vegne av oss. Når du registrerer deg, behandles mobilnummeret ditt, stemplene dine og besøkshistorikken for å gi deg stempelkort og kuponger. Appens egen personvernerklæring finner du i appen og i App Store og Google Play. Du kan når som helst be oss slette profilen din ved å sende e-post.</p>"),
        ("Informasjonskapsler og samtykke",
         "<p>Nettsiden bruker informasjonskapsler (cookies) og lignende teknologi. Nødvendige kapsler gjør at siden fungerer, blant annet for å huske samtykkevalget ditt og for å sende skjemaer. Kapsler til analyse og markedsføring settes bare hvis du samtykker i banneret som vises første gang du besøker siden. Banneret leveres av Wix (Usercentrics) og støtter Google Consent Mode. Du kan endre eller trekke samtykket når som helst via lenken \"Innstillinger for informasjonskapsler\" nederst på siden eller ved å slette kapslene i nettleseren.</p>"
         "<p>Med samtykke bruker vi Google Tag Manager til å laste følgende: Google Analytics 4 (statistikk over bruk av siden, IP-adressen anonymiseres), Google Ads (måling av annonser og konverteringer) og Meta Pixel (måling av annonser på Facebook og Instagram). Dataene kan overføres til USA i henhold til EU-kommisjonens beslutninger og standardavtaler. Vi bruker ikke opplysningene til å identifisere enkeltpersoner.</p>"),
        ("Hvem vi deler opplysninger med",
         "<p>Vi selger ikke personopplysninger. Vi deler bare med databehandlerne nevnt over, med Fixit når du selv bestiller time, og med offentlige myndigheter når loven krever det.</p>"),
        ("Dine rettigheter",
         "<p>Du har rett til innsyn i opplysningene vi har om deg, til å få rettet eller slettet dem, til å begrense eller protestere mot behandlingen, og til dataportabilitet. Har du gitt samtykke, kan du trekke det når som helst uten at det påvirker lovligheten av behandlingen før samtykket ble trukket. "
         f"Send henvendelsen til <a href=\"{MAILTO}?subject=Innsyn\">{s['epost']}</a>, så svarer vi innen 30 dager. Er du uenig i hvordan vi behandler opplysningene dine, kan du klage til <a href=\"https://www.datatilsynet.no\" target=\"_blank\" rel=\"noopener\">Datatilsynet</a>.</p>"),
        ("Sikkerhet",
         "<p>Nettsiden leveres over kryptert forbindelse (HTTPS). Tilgang til innsendinger og e-post er begrenset til dem som trenger det for å følge opp henvendelsen, og er beskyttet med tofaktorautentisering.</p>"),
        ("Endringer",
         "<p>Vi oppdaterer denne erklæringen når behandlingen endres eller når nye leverandører tas i bruk. Gjeldende versjon ligger alltid på denne siden. Sist oppdatert: oktober 2026.</p>"),
    ]
    innhold = "".join(f"<h2>{t}</h2>{x}" for t, x in deler)
    body = L.section(
        f'<div class="artikkel"><div class="sec-head">{L.eyebrow("Personvern")}<h1>Personvernerklæring</h1>'
        f'<p class="lead muted">Her forklarer vi hvilke personopplysninger J&amp;K Barber Shop behandler når du bruker nettsiden, sender oss et skjema, bestiller time eller bruker appen, hvorfor vi gjør det, og hvilke rettigheter du har.</p></div>'
        f'<div class="prosa">{innhold}</div></div>', cls="sec-hero")
    return L.page(ctx, path="/personvern/", title="Personvernerklæring | J&K Barber Shop",
                  description="Personvernerklæring for J&K Barber Shop (JK Barber Drift AS): opplysninger vi behandler fra skjemaer, booking, app og informasjonskapsler, og dine rettigheter.",
                  body=body, breadcrumbs=[("Personvern", None)], active=None, noindex=True)


# ---------- /tilbakemelding/ (noindex, mailto) ----------

def render_tilbakemelding(ctx):
    s = ctx["site"]
    kort = []
    for a in ctx["avdelinger"]:
        emne = f"Tilbakemelding {avd_navn(a)}".replace(" ", "%20").replace("&", "%26")
        kropp = "Avdeling:%20" + avd_navn(a).replace(" ", "%20") + "%0AHva%20syntes%20du%20(1%20til%205)%3A%20%0AHva%20kan%20bli%20bedre%3A%20%0ANavn%20og%20telefon%20(valgfritt)%3A%20"
        kort.append(f'<article class="card kort-stor" data-avd-kort="{a["slug"]}"><h2>{e(avd_navn(a))}</h2><p class="muted small">{e(a["gateadresse"])}, {e(a["poststed"])}</p>'
                    f'<div class="kort-handling">{L.btn("Send tilbakemelding", f"{MAILTO}?subject={emne}&body={kropp}", "s", size="sm", external=False)}'
                    f'<a href="{e(a["reviewsUrl"])}" target="_blank" rel="noopener">Anmeld på Google</a></div></article>')
    body = L.section(
        f'<div class="sec-head sec-head-stor">{L.eyebrow("Tilbakemelding")}<h1>Tilbakemelding etter besøk</h1>'
        '<p class="lead muted">Har du vært hos oss og vil fortelle hvordan det var? Vi leser alt, og vi bruker det til å bli bedre. Velg avdelingen du besøkte, så åpnes en e-post til oss med noen spørsmål du kan svare på. Skriv gjerne hva som var bra, hva som kan bli bedre, og om du vil at vi tar kontakt.</p>'
        f'<p class="muted small">Du kan også ringe <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a> eller skrive fritt til <a href="{MAILTO}?subject=Tilbakemelding">{s["epost"]}</a>.</p></div>'
        f'<div class="grid grid-3">{"".join(kort)}</div>', cls="sec-hero")
    body += L.section(L.cta_box("Var du fornøyd?", "En anmeldelse på Google betyr mye for barbereren som klippet deg. Velg avdelingen over og trykk \"Anmeld på Google\".",
                                L.btn("Bestill ny time", "/bestill-time/", "s", bestill="felles", plassering="tilbakemelding")), tone="flate")
    return L.page(ctx, path="/tilbakemelding/", title="Tilbakemelding | J&K Barber Shop",
                  description="Fortell oss hvordan besøket hos J&K Barber Shop var. Velg avdelingen du besøkte og send tilbakemelding på e-post, eller legg igjen en anmeldelse på Google.",
                  body=body, breadcrumbs=[("Tilbakemelding", None)], active=None, noindex=True)


# ---------- /takk/ og 404 ----------

def render_takk(ctx):
    s = ctx["site"]
    body = L.section(
        f'<div class="sentrert">{L.eyebrow("Takk")}<h1>Takk, vi har mottatt meldingen din</h1>'
        f'<p class="lead muted">Vi svarer så snart vi kan, normalt innen én virkedag. Haster det, ring <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a>.</p>'
        f'<div class="knapper">{L.btn("Til forsiden", "/")}{L.btn("Bestill time", "/bestill-time/", "s", bestill="felles", plassering="takk")}</div></div>', cls="sec-hero")
    return L.page(ctx, path="/takk/", title="Takk | J&K Barber Shop",
                  description="Takk for meldingen til J&K Barber Shop. Vi svarer så snart vi kan, normalt innen én virkedag. Haster det, ring oss på fellesnummeret 90 80 00 86.",
                  body=body, active=None, noindex=True)


def render_404(ctx):
    s = ctx["site"]
    lenker = " · ".join(f'<a href="{a["url"]}">{e(avd_navn(a))}</a>' for a in ctx["avdelinger"])
    body = L.section(
        f'<div class="sentrert">{L.eyebrow("404")}<h1>Siden finnes ikke</h1>'
        '<p class="lead muted">Adressen kan være skrevet feil, eller siden er flyttet. Det du leter etter, finner du sannsynligvis her:</p>'
        f'<div class="knapper">{L.btn("Bestill time", "/bestill-time/", bestill="felles", plassering="404")}{L.btn("Avdelinger", "/avdelinger/", "s")}{L.btn("Tjenester og priser", "/tjenester/", "s")}{L.btn("Til forsiden", "/", "s")}</div>'
        f'<p class="muted small andre-avd">{lenker}</p>'
        f'<p class="muted small">Ring <a href="tel:{s["telefon"]}">{s["telefonVisning"]}</a> hvis du ikke finner frem.</p></div>', cls="sec-hero")
    return L.page(ctx, path="/404.html", title="Siden finnes ikke | J&K Barber Shop",
                  description="Siden du lette etter hos J&K Barber Shop finnes ikke. Gå til forsiden, finn din avdeling, se tjenester og priser eller bestill time direkte.",
                  body=body, active=None, noindex=True)


def render(ctx):
    return {
        "/om-oss/": render_om_oss(ctx),
        "/app/": render_app(ctx),
        "/gavekort/": render_gavekort(ctx),
        "/produkter/": render_produkter(ctx),
        "/jobb/": render_jobb(ctx),
        "/franchise/": render_franchise(ctx),
        "/kontakt/": render_kontakt(ctx),
        "/hjemmebarbering/": render_hjemmebarbering(ctx),
        "/bestill-time/": render_bestill(ctx),
        "/personvern/": render_personvern(ctx),
        "/tilbakemelding/": render_tilbakemelding(ctx),
        "/takk/": render_takk(ctx),
        "404.html": render_404(ctx),
    }

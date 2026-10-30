# BUILD-LOG: rammeverk, kjernesider og statiske sider (30. oktober 2026)

Kjør: `cd /home/claude/jkbarber-site/build && python3 build.py --check`
Resultat: dist/ slettes og bygges på nytt. 70 sider (29 kjerne/statiske + 41 blogg) + sitemap.xml + robots.txt + assets. Alle kontroller grønne (balanserte tagger, én H1 per side, ingen tankestreker, title under 60 tegn, description 120 til 160 tegn, ingen "midlertidig"/"under arbeid").

## Filer

| Fil | Innhold |
|---|---|
| build/build.py | Inngang. Laster ctx, importerer alle moduler i build/pages/ (forside først, så alfabetisk), skriver dist/, kopierer build/assets/* og design/messing-800.png (som dist/assets/logo-messing.png), lager sitemap.xml (alle sider uten noindex) og robots.txt, kjører HTML-kontroll per side. |
| build/lib/data.py | Laster cms-data/data.json, fjerner tankestreker, bygger ctx. Faste fakta i SITE (telefon, e-post, org.nr., app-lenker, gavekort, form-ID-er, nivåer, regel 0, prissetning), MERKER (11 med j-kshop-lenker + UTM), GOOGLE (rating og antall per avdeling), BLOGG_AVD / BLOGG_TJ (post-slug + tittel + ingress per avdeling og tjeneste), HOVED_BEHANDLING. |
| build/lib/layout.py | page(), header(), footer(), sticky(), breadcrumbs, JSON-LD-hjelpere og komponenter (btn, link, section, heading, eyebrow, review_card, cta_box, faq_block, faq_jsonld, pris_rad, tabell, og). |
| build/lib/images.py | IMAGES: avtalt filnavn -> wixstatic-URL. picture() gir <img> med skalering (fill w,h, q_80, lazy, width/height) eller plassholder-div. ph() for rene plassholdere. LOGO og LOGO_SCHEMA. |
| build/lib/util.py | e (escape), slugify, nb_num / kr (1 029 kr), fix_dashes, strip_tags, split_sentences, chunk_even, tid ("10:00-21:00" -> "10 til 21"), tid_schema, truncate. |
| build/lib/md.py | md_to_html(text, h_shift) og md_meta(text) (frontmatter) for bloggmodulen. |
| build/lib/ricos.py | ricos_to_html(richContent, skip_image_id) for de migrerte innleggene (PARAGRAPH, HEADING, lister, IMAGE med wixstatic-URL, BOLD/ITALIC/UNDERLINE/LINK), wix_image_url(id, w, h), ricos_plain. Tankestreker byttes, overskrifter flyttes så øverste nivå blir h2, avsnitt som starter med "• " samles til ul. |
| build/pages/blogg.py | /blogg/, 5 kategorisider og 35 innlegg under /post/. Se eget avsnitt under. |
| cms-data/blogg-migrert.json | Cache av de 15 migrerte innleggene (komprimert Ricos, excerpt, kategori, forsidebilde, SEO-beskrivelse) hentet 30. okt fra draft-posts på ny site. Bygget trenger ikke nett. |
| build/lib/anmeldelser.py | Google-sitater per avdeling (3 stk) og GENERELLE (forside). |
| build/pages/forside.py | / . Eksporterer også avd_kort() og apningstider_kort() som andre moduler kan gjenbruke. |
| build/pages/avdelinger.py | /avdelinger/ og 7 avdelingssider. |
| build/pages/tjenester.py | /tjenester/ og 6 tjenestesider. |
| build/pages/statiske.py | /om-oss/, /app/, /gavekort/, /produkter/, /jobb/, /franchise/, /kontakt/, /hjemmebarbering/, /bestill-time/, /personvern/, /tilbakemelding/, /takk/ og 404.html. Skjemahjelpere (felt, tekstfelt, nedtrekk, valg, samtykke, skjema) øverst i filen. |
| build/assets/styles.css | Én CSS-fil, mobil først, brytpunkt 720 og 1080. Kopieres til dist/assets/styles.css. |
| build/assets/site.js | Mobilmeny, sticky CTA (vises etter 300 px på under 1080 px), dataLayer-push, Wix Forms-innsending med visitor-token, ?avd= forhåndsvalg. Kopieres til dist/assets/site.js. |

Kilde for CSS/JS er build/assets/. Ikke rediger i dist/, alt der overskrives.

## Genererte sider

/, /avdelinger/, /avdelinger/{sandvika,ski,asenveien,kolbotn,jessheim,strommen,rykkinn}/, /tjenester/, /tjenester/{herreklipp,skin-fade,skjeggtrim,barbering,barneklipp,kombo}/.

Schema: forside Organization + WebSite + FAQPage; avdeling BarberShop (adresse, openingHoursSpecification, hasOfferCatalog med Barber-pris som minPrice og Senior som maxPrice der den finnes i Priser, ellers +50/+70/+100, ReserveAction til Fixit) + FAQPage + BreadcrumbList; tjeneste Service (availableChannel per avdeling, minPrice/maxPrice) + FAQPage + BreadcrumbList; /avdelinger/ ItemList; /tjenester/ FAQPage.

## Statiske sider (statiske.py)

| Side | Innhold | Schema |
|---|---|---|
| /om-oss/ | Etter OmOss.dc.html: hero (H1 "Om J&K Barber Shop", regel 0), historien med tidslinje 2018, 2019, 2020, 2021 til 2024 (app og nettbutikk, uten årstall for appen), 2025, i dag; navnet (Jan og Kevin, det tredje barnet, J&K-familien, ingen personnavn); slik jobber vi (konsultasjon, fire nivåkort, lærebedrift-kort, kvalitetsløftet med fem punkter); J&K i tall (7 avdelinger, 12 000+ kunder, 1 100+ anmeldelser, 4,8, 2018); resten av J&K-familien; jobb/franchise-kort uten tall (seks-måneders-kravet står bare på /franchise/); CTA og avdelingsliste. | AboutPage (about/mainEntity = Organization @id) + BreadcrumbList |
| /app/ | Fire stempelkort, hvert 10. gratis, barbereren registrerer stempelet, stempel gyldig ett år, gjelder på tvers. App Store/Google Play-lenker fra innholdsplanen. Kuponger omtalt generelt (ingen 10 %-velkomstkupong lovet, [SJEKK] i planen). FAQ: CMS-FAQ for "app" pluss seks fra planen uten [SJEKK]-punktene (papirkort, glemt stempel, påminnelse utelatt). | MobileApplication + FAQPage + BreadcrumbList |
| /gavekort/ | Valgfritt beløp, kjøpes på fixit.no/gavekort/1634, innløses i kassen (ikke i onlinebookingen). Forslag til beløp regnes ut fra høyeste pris i Priser-samlingen rundet opp til 50 (gir 700/900/1 350/600 kr som i planen). Gyldighetstid, produkter og hjemmebarbering ([SJEKK]) er utelatt. Sticky "Bestill" peker på gavekortkjøpet. | FAQPage + BreadcrumbList |
| /produkter/ | 11 merker i planens rekkefølge (styling, skjegg og barbering, hårpleie) med tekst, barberens tips og kjøp-knapp til j-kshop.no (collection + UTM fra data.py). Ingen nettbutikk her. Hoppelenker til hvert merke (#reuzel osv.). | ItemList med Brand + BreadcrumbList |
| /jobb/ | Ansettelse og stolleie uten tall, "vi jobber mot å bli godkjent lærebedrift", "vi tar imot åpne søknader til alle avdelinger". Skjema Jobbsøknad (formId 4db6b92d) med de ni feltene fra WIX-NY-SITE.md, CV som URL-felt. Takkemelding uten svarfrist (to uker er [SJEKK]). | BreadcrumbList |
| /franchise/ | Nærområde (Follo, Asker og Bærum, Romerike), minst seks måneder hos J&K først, seks-stegs liste, økonomi uten tall, skjema Franchise (formId af4ebbfe, åtte felt). "Eget selskap som inngår franchiseavtale med oss" (AS/JK Barber Drift AS er [SJEKK]). | BreadcrumbList |
| /kontakt/ | Felles telefon og e-post, hovedkontor med org.nr., presse/samarbeid, alle sju avdelinger som kort (adresse, plassering, åpningstid, Fixit, veibeskrivelse), skjema Kontakt (formId 46d9f072) med avdelingsvalg (data-avd-velger, ?avd= forhåndsvelger) pluss Hovedkontor. Emne-nedtrekk fra planen finnes ikke i Wix-skjemaet og er lagt som hint i meldingsfeltet. Lenke til /tilbakemelding/. | ContactPage + BreadcrumbList |
| /hjemmebarbering/ | Innholdsplan 6.12: H1 "Mobil barbering hjemme hos deg", tre steg, faste priser (639/825/550/579/529/529/1 029/1 299), 100 % tillegg søn- og helligdager, områder (Sandvika, Oslo, Asker, Drammen), privat/bedrift, minst 24 timer før, regel 0. Skjema Hjemmebarbering (formId 28632583, sju felt) pluss en vilkårsavkrysning uten name (sendes ikke til Wix, bare klientvalidering). Breadcrumb under Tjenester og priser. | Service (areaServed, hasOfferCatalog med faste priser) + BreadcrumbList |
| /bestill-time/ | Sju kort med Fixit-lenke (data-bestill per avdeling, plassering "bestill-time"), adresse, plassering og åpningstid; data-avd-kort så ?avd= markerer kortet. Heller i appen (App Store/Google Play), godt å vite med avbestilling 24 timer og gavekort-lenke. Fakturering ved uteblivelse og 10-minuttersregel ([SJEKK]) utelatt. | ItemList + BreadcrumbList |
| /personvern/ | Behandlingsansvarlig JK Barber Drift AS, org.nr. 932 372 614, Åsenveien 3. Dekker kontaktskjema, jobbsøknader (slettes senest seks måneder etter avsluttet rekruttering), franchise, hjemmebarbering, tilbakemelding, Wix Forms som databehandler, Fixit som egen behandlingsansvarlig, appen, informasjonskapsler med Wix/Usercentrics-banner og Consent Mode (GA4, GTM, Google Ads, Meta Pixel), rettigheter, Datatilsynet. noindex (som planen sier), derfor utenfor sitemap. | BreadcrumbList |
| /tilbakemelding/ | noindex. Enkel mailto-løsning: ett kort per avdeling med "Send tilbakemelding" (mailto med emne og ferdig utfylt kropp: avdeling, 1 til 5, hva kan bli bedre, navn/telefon) og "Anmeld på Google" (reviewsUrl). ?avd=<slug> markerer kortet via data-avd-kort. Byttes til Wix-skjema når skjema nr. 5 finnes. | BreadcrumbList |
| /takk/ | noindex, felles takkeside. | ingen |
| 404.html | I rot, noindex, knapper til bestilling, avdelinger, tjenester og forside. | ingen |

Skjemaverdier: nedtrekk og avkrysninger sender verdiene "Sandvika Storsenter", "Ski Storsenter", "Åsenveien 3", "Kolbotn Torg", "Jessheim Storsenter", "Strømmen Storsenter", "Rykkinn Senter" (+ "Hovedkontor" i Kontakt), erfaring "Under 1 år" osv., fagbrev "Ja/Nei/Under utdanning", tjeneste som i WIX-NY-SITE.md. Wix-API-et var ikke tilgjengelig fra byggemiljøet, så alternativverdiene er ikke lest tilbake fra skjemaene: sjekk i Forms-dashbordet at valgene har nøyaktig samme tekst (ellers avviser Wix innsendingen med fieldViolations).

CSS lagt til i build/assets/styles.css for disse sidene: .tidslinje/.tl/.yr, .kort-navn, .laere, .kvalitet, .tall-grid/.tall-kort/.tall-num, .hake-liste, .h2-gruppe, .produkt-merke, .bestill-kort, .felt-gruppe, .bilde-rund/.bilde-stabel.

## Plassholdere (class "ph", mørk boks med motiv og filnavn)

- Forside: app-bilde (jk-barber-felles-app-stempelkort-mobil.jpg), tre bloggbilder, avdelingskort for Jessheim og Strømmen (ingen egne bilder med avklarte rettigheter), barneklipp-kort (jk-barber-felles-barneklipp.jpg). Merkelogoer er tekstbokser (lenker til j-kshop.no) inntil logofiler finnes.
- Avdelingssider: Google Maps-kart (boks + knapp "Åpne i Google Maps" med mapsUrl). Galleri: filnavn fra innholdsplan 10.2, bare de som finnes i images.py vises som bilde (Ski fasade/interiør, Sandvika interiør/skin fade/skjeggtrim/slickback, Kolbotn interiør, Åsenveien fasade/interiør, Rykkinn fasade). Hero for Jessheim og Strømmen er plassholder. Bloggkort-bilde per avdeling (jk-barber-<slug>-blogg.jpg).
- Tjenestesider: før/etter (4 bokser, jk-barber-felles-<tjeneste>-1..4.jpg), produktbilder (3 bokser), hero for barneklipp.
- /avdelinger/: kart med alle sju.
- Statiske sider: /om-oss/ hero (jk-barber-asenveien-historisk-2018.jpg) og håndverksdetalj (jk-barber-felles-handverk-detalj.jpg); /app/ skjermbilder (jk-barber-felles-app-skjermbilder.jpg) og kasse (jk-barber-felles-app-kasse.jpg); /gavekort/ (jk-barber-felles-gavekort.jpg); /produkter/ ett per merke (jk-barber-felles-produkt-<handle>.jpg, Davines bruker eksisterende produkter-davines-bilde, hylle bruker produkter-harvoks); /jobb/ hero og opplæring (jk-barber-felles-jobb-hero.jpg, jk-barber-felles-jobb-opplaering.jpg); /hjemmebarbering/ (jk-barber-felles-hjemmebarbering.jpg). Ekte bilder: /franchise/ interiør 2025, /kontakt/ og /om-oss/ Åsenveien-fasade, /om-oss/ barberer-med-kunde (2021).
- Anmeldelser-lenke per avdeling er Google Maps-søk (reviewsUrl i data.py) inntil gbpUrl/reviewsUrl fylles i CMS. lat/lng mangler, derfor ingen geo i schema (legges inn automatisk når feltene fylles).
- Logo i schema peker på den svarte Wix-logoen (2270x2041), bør byttes til 512x512 messing-variant.

Ikke brukt: "Barbers Working"/"Barber's Portraits" og Strømmen-pressebildene (rettigheter).

## Slik legger du til sider

1. Lag build/pages/<navn>.py med `def render(ctx) -> dict`. Nøkkel er ren URL med skråstrek ("/om-oss/") eller filnavn i rot ("404.html"). build.py skriver "/x/" til dist/x/index.html.
2. Bygg HTML med `from lib import layout as L` og kall
   `L.page(ctx, path=..., title=..., description=..., body=..., breadcrumbs=[("Om oss", None)], jsonld=[...], active="om-oss", bestill_url="/bestill-time/", avdeling="felles", og_image=None, noindex=False, og_type="website", extra_head="")`.
   page() legger selv til head (canonical, OG, Twitter, fonts, CSS, JS, GTM-markører), header, breadcrumbs (Hjem legges til), skip-link, footer, sticky CTA og BreadcrumbList-schema når breadcrumbs er satt. body må ha nøyaktig én <h1>.
3. Komponenter: `L.section(inner, tone="flate"|"mork"|"", id_=..., cls=...)` (wrap inni), `L.heading(h2, lead, eye)`, `L.btn(tekst, href, "p"|"s", size="sm", bestill="<ga4Avdeling>", plassering="...")` (eksterne lenker får target/rel automatisk), `L.link(...)`, `L.cta_box(tittel, tekst, knapp_html)`, `L.faq_block(items, heading_text=..., side=True|False)` + `L.faq_jsonld(items)`, `L.review_card(tekst, hvem)`, `L.tabell(head, rows)`, `L.pris_rad(...)`, `L.eyebrow(...)`. Bilder: `IM.picture(filnavn, alt, w, h, cls=..., lazy=True, motiv=...)`, `IM.ph(motiv, filnavn)`, `IM.url(filnavn, w, h)`.
4. Data i ctx: `ctx["site"]` (fakta og form-ID-er i `ctx["site"]["forms"]`), `ctx["avdelinger"]` (liste, felt som i CMS pluss url, nabo, rating, antall, reviewsUrl, apningstider), `ctx["avd"][slug]`, `ctx["tjenester"]`, `ctx["tj"][slug]`, `ctx["priser"]`, `ctx["faq"]`, `ctx["merker"]`, og funksjoner i `ctx["fn"]`: hovedpriser(slug), pris(tjeneste_slug, avd_slug, behandling=None, niva="Barber"), priser_tjeneste(slug), priser_kategori(), faq_for("app"|"gavekort"|"forside"|"tjeneste"|"avdeling", slug=None), nabo_avdelinger(slug).
5. Skjemaer: `<form class="skjema" data-wix-form="<formId>" data-skjema="kontakt" data-takk="#takk">` med felt der `name` er feltets target fra WIX-NY-SITE.md del 5, en `<p class="skjema-status" aria-live="polite"></p>` i skjemaet og en `<div class="skjema-takk card" id="takk">` rett etter. site.js sender til Wix og viser takk uten sideskifte. CSS-klasser: .felt, .felt-rad, .valg, .samtykke. Tilbakemelding: mailto-fallback til post@j-kbarber.no.
6. Markdown: `from lib.md import md_to_html, md_meta`. md_to_html(tekst, h_shift=1) gjør # til h2. CSS for artikler: .artikkel, .artikkel-topp, .artikkel-meta, .kategorier, .prosa, .blogg-kort (kortene på forsiden bruker .card.blogg-kort + .kort-bilde + .kort-innhold).
7. Menyen og footeren lenker allerede til /app/, /gavekort/, /produkter/, /om-oss/, /blogg/, /bestill-time/, /kontakt/, /jobb/, /franchise/, /hjemmebarbering/, /personvern/. Blogglenker fra kjernesidene: /post/<slug>/ og /blogg/. 404.html: returner {"404.html": L.page(..., path="/404.html", noindex=True)}. /takk/: noindex=True (holdes utenfor sitemap, robots.txt disallower /takk/).

## Blogg (blogg.py)

Kilder: de 20 nye artiklene i /home/claude/jkbarber-analyse/blogg/01-*.md til 20-*.md (H1, blank linje, metablokk Slug/Title tag/Meta/Kategori/Hovedsøkeord/Bilde/Forfatter, så brødtekst) og de 15 migrerte innleggene i cms-data/blogg-migrert.json (hentet med `GET /blog/v3/draft-posts/{id}?fieldsets=RICH_CONTENT` for draftPostId-ene i WIX-NY-SITE.md del 4, lagret uten COLOR-dekorasjoner, id-er og tomme avsnitt; fire av dem (slik-barberer-du-deg-hjemme, harstyling-del-1 og -2, mykt-skjegg-pa-1-2-3, reuzel) hadde ren tekst med linjeskift som overskrifter og lister, og er normalisert til HEADING/LIST-noder i cachen).

| Side | Innhold | Schema |
|---|---|---|
| /blogg/ | Etter Blogg.dc.html: hero (H1 "Guider fra barbererne"), kategorichips (.kategorier), fremhevet prisguide (hva-koster-herreklipp-og-skin-fade, knapper "Les prisguiden" og "Se alle priser"), "Guider for din avdeling" med de seks lokale (Ski, Kolbotn, Sandvika, Jessheim, Strømmen, Rykkinn, tag = stedsnavn), rutenett med de 28 øvrige (nye først, så migrerte), app-boks (App Store, Google Play, /app/; ingen nyhetsbrevskjema), CTA og kategorilenker. | Blog (blogPost-liste) + ItemList + BreadcrumbList |
| /blogg/kategori/{guider,skjegg,har-og-styling,produkter,barbershop-livet}/ | H1 = kategorinavn, beskrivelse, chips med aktiv kategori, kort for alle innlegg i kategorien, app-boks, CTA. | CollectionPage med ItemList + BreadcrumbList |
| /post/{slug}/ (35) | Breadcrumbs Hjem > Blogg > Kategori > Tittel, eyebrow, H1, meta (dato, kategori, "Barbererne hos J&K Barber Shop", lesetid), hovedbilde (nye: images.py-plassholder eller eksisterende bilde via BILDE_OVERRIDE; migrerte: wixstatic-forsidebilde 1200x675, samme bilde hoppes over i brødteksten), brødtekst (.prosa), CTA-boks "Bestill time", "Flere guider" med 3 relaterte (samme kategori først, nye først), bunn-CTA. | BlogPosting (headline, description, image, datePublished/dateModified, author Organization "Barbererne hos J&K Barber Shop", publisher, articleSection, wordCount, keywords fra Hovedsøkeord) + FAQPage på de 20 nye (spørsmål/svar hentes fra fete FAQ-spørsmål) + BreadcrumbList. og:type article. |

Regler i modulen: interne lenker får skråstrek (`_slashify`, /tjenester/skin-fade -> /tjenester/skin-fade/), fete FAQ-spørsmål blir egne avsnitt med class faq-q, avsnittet "## Bestill time" nederst i artiklene beholdes som tekst uten overskrift (CTA-boksen følger). Dato: 2026-11-03 for de nye, for de migrerte brukes richContent.metadata.updatedTimestamp (2024, firstPublishedDate finnes ikke på kladdene). Titler på migrerte er normalisert (ikke versaler, #2 kortet til "Slik behandler du flass med Davines hårprodukter") i MIGRERT_TITTEL; title tags og meta descriptions for dem ligger i MIGRERT_TITTEL/MIGRERT_META. For de nye brukes metablokken, med TITLE_FIX (14 slugs over 60 tegn) og META_FIX (16 slugs over 160 tegn) der den ikke holdt grensene.

CSS lagt til i build/assets/styles.css: .fremhevet/.fremhevet-bilde/.fremhevet-tekst, .app-boks/.app-boks-bilde, .blogg-kort h3/.tag/.kort-les, .artikkel-hode, .prosa figure/figcaption/faq-q/table, .sec-hero .kategorier.

Bilder: plassholdere (class ph) for de nye artiklene bruker filnavnet fra metablokken (jk-barber-prisguide-herreklipp-2026.jpg osv.), unntatt 12 slugs i BILDE_OVERRIDE som bruker eksisterende bilder i images.py (Ski-fasade, Kolbotn-interiør, Sandvika-serien, 2021-bildene, hårvoks). Merk at forsiden (forside.py GUIDER) og avdelingssidene bruker andre plassholdernavn for de samme artiklene (jk-barber-felles-blogg-prisguide.jpg, jk-barber-<avd>-blogg.jpg); når fotografens bilder kommer, legg samme URL på begge navnene i images.py, eller samkjør navnene. Migrerte innlegg med bilder utenfor 8c3e53-kontoen (11062b_..., og id-er uten prefiks) er Wix-arkivbilder fra den gamle siten; de lastes fra wixstatic som før.

Merknader: det gamle innlegget hvor-ofte-bor-jeg-besoke-frisoren-min bygges som egen side (WIX-NY-SITE.md anbefaler å ikke publisere det og la hvor-ofte-bor-menn-klippe-seg ta over; fjern slugen fra blogg-migrert.json eller filtrer i last_migrerte hvis det skal ut). Kilde-linjene "Kilde: grooming.no" i fem migrerte innlegg er beholdt. Ingen av de migrerte peker på /post/<gammel slug> lenger (eneste interne lenke, i mykt-skjegg-pa-1-2-3, er rettet til /post/slik-foner-du-skjegget/).

## Merknader til Alan / neste runde

- Rykkinn er publisert=false i CMS, men siden er bygget (briefen sier 7 avdelinger). Fjern fra ctx["avdelinger"] i data.py hvis den skal holdes utenfor.
- Hvis gbpUrl, reviewsUrl, lat, lng, heroBilde fylles i Avdelinger-samlingen og data.json genereres på nytt, plukkes reviewsUrl og geo opp automatisk; bilder må legges i images.py.
- Sitater fra Google nevner noen barberere ved fornavn (Ibo, Nicolae, Saad, Nehat, Abdo, Muha, Moon). Fjern i lib/anmeldelser.py hvis det ikke er ønsket.
- /personvern/ er satt til noindex slik innholdsplanen sier (del 2 og 6.13). Vil du ha den indeksert, sett noindex=False i render_personvern.
- Åpne [SJEKK]-punkter som påvirker de statiske sidene og er skrevet rundt: velkomstkupong 10 % (ikke nevnt), gavekortets gyldighet, svarfrist på søknader, fakturering ved uteblivelse, krav om svennebrev, hvilket selskap franchiseavtalen inngås med, lagringstid for søknader (satt til seks måneder i skjemaet og personvernerklæringen, som byggeplanen foreslår). Bekreft og juster tekstene i statiske.py.
- Personvernerklæringen nevner en lenke "Innstillinger for informasjonskapsler" nederst på siden. Den finnes ikke i footeren ennå; legg den inn når Usercentrics-banneret er på plass (lenken åpner bannerets innstillinger).

# -*- coding: utf-8 -*-
"""Genererer CMS-data (JSON) for J&K Barber Shop Wix-samlinger."""
import json, os, re

OUT = os.path.dirname(os.path.abspath(__file__))
TEL = "+4790800086"
TELV = "90 80 00 86"
EPOST = "post@j-kbarber.no"
STD = "Priser for nivå Barber. Prisen avhenger av barberens nivå, endelig pris ser du i onlinebookingen."

def p(*paras):
    return "".join("<p>%s</p>" % x for x in paras)

def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>"

def maps(adr):
    from urllib.parse import quote_plus
    return "https://www.google.com/maps/dir/?api=1&destination=" + quote_plus(adr)

# ---------------------------------------------------------------- AVDELINGER
A = []
def avd(**k):
    A.append(k)

avd(slug="sandvika", title="Sandvika Storsenter", kortnavn="Sandvika", ga4="sandvika", rekkefolge=1, publisert=True,
    h1="Barbershop og herrefrisør i Sandvika Storsenter",
    undertittel="Herreklipp, skin fade, skjeggtrim og knivbarbering i Kjørbokollen, ved siden av Cewe Japan Photo.",
    seoTittel="Barbershop og herrefrisør Sandvika Storsenter | J&K",
    seoBeskrivelse="Barbershop og herrefrisør i Sandvika Storsenter, i Kjørbokollen ved Cewe Japan Photo. Herreklipp, skin fade, skjeggtrim og knivbarbering. Bestill time online.",
    senter="Sandvika Storsenter", plassering="I Kjørbokollen, ved siden av Cewe Japan Photo. Følg skiltene mot Kjørbokollen.",
    gate="Brodtkorbsgate 7", gatenavn="Brodtkorbsgate", nr=7, postnr="1338", sted="Sandvika", kommune="Bærum",
    parkering="Parkeringshus i Sandvika Storsenter. 2 timer gratis parkering (senterets regler gjelder).",
    kollektiv="3 til 5 minutters gange fra Sandvika stasjon (tog og buss). Bussterminalen ligger vegg i vegg med senteret.",
    fixit=2882, apnet=2020,
    tider=("10:00-21:00",)*5 + ("09:00-19:00", "Stengt"),
    prisniva="kr 449-1799", dropIn=True,
    oversikt="Den travleste avdelingen vår, sterk på skin fade. I Kjørbokollen ved Cewe Japan Photo.",
    naboer=["rykkinn", "asenveien"],
    ingress="J&K Barber Shop ligger i Kjørbokollen i Sandvika Storsenter, ved siden av Cewe Japan Photo. Her får du klassisk herreklipp, skin fade, skjeggtrim og tradisjonell knivbarbering av erfarne barberere, alltid med en kort konsultasjon først. Kort vei fra Sandvika stasjon og bussterminalen, og du parkerer i senteret.",
    beskrivelse=p(
        "Sandvika er stedet der Bærum møtes, og Sandvika Storsenter er stedet der Sandvika møtes. Da vi åpnet her i mai 2020, var planen enkel: en barbershop der folk i Bærum kunne få en ordentlig klipp uten å reise til Oslo. I dag er avdelingen vår i Sandvika den mest besøkte vi har, med flere hundre anmeldelser på Google og et snitt på 4,9.",
        "Du finner oss i Kjørbokollen, ved siden av Cewe Japan Photo. Det er et sted mange går forbi, og det er helt bevisst. Mange av kundene våre kommer innom på vei hjem fra jobb, mellom to ærender eller mens familien handler. Andre har bestilt time for lenge siden hos en bestemt barberer, og kommer fra Bekkestua, Høvik, Kolsås, Slependen og Asker for å få akkurat den fade-en de vet de får her.",
        "Barbererne i Sandvika er spesielt sterke på skin fade og teksturert klipp, og det er her vi oftest ser de unge fra videregående på Nadderud og Sandvika som vil ha linjene helt rene. Samtidig er det mange som har gått hos oss siden åpningen og som bestiller samme klassiske klipp hver fjerde uke, gjerne med en skjeggtrim på toppen. Begge deler er like velkomne, og alle behandlingene på menyen er for både menn og kvinner.",
        "Praktisk: Sandvika stasjon ligger tre til fem minutters gange unna, med tog på Drammenbanen og Askerbanen og buss fra hele Bærum. Kjører du, er det parkeringshus i senteret med 2 timer gratis parkering (senterets regler gjelder). Vi holder åpent til 21 på hverdager, så det er plass til en time etter jobb, og lørdag fra 9.",
        "Har du ikke prøvd oss før, bestill time hos en av barbererne på nivå Barber eller Senior første gang, så får du en konsultasjon og et resultat du kan måle oss på. Og last ned J&K-appen før du kommer, så får du første stempel på stempelkortet med en gang."),
    faq=[
        ("Kan jeg komme på drop-in i Sandvika Storsenter?", "Ja, når vi har ledig. Sandvika er den travleste avdelingen vår, så på lørdager og etter klokken 16 på hverdager anbefaler vi å bestille time på nett eller i appen."),
        ("Hvor parkerer jeg?", "I parkeringshuset til Sandvika Storsenter. De første 2 timene er gratis (senterets regler gjelder). Følg skiltene mot Kjørbokollen, vi ligger ved siden av Cewe Japan Photo."),
        ("Hvor lang tid tar det fra Sandvika stasjon?", "Tre til fem minutter til fots. Gå inn hovedinngangen fra stasjonssiden og følg skiltene mot Kjørbokollen."),
        ("Tar dere imot barn?", "Ja. Barneklipp koster 529 kr i Sandvika (nivå Barber), og mange foreldre bestiller time til seg selv og barnet etter hverandre hos samme barberer."),
        ("Hvordan betaler jeg?", "Du betaler i salongen etter behandlingen, med kort eller Vipps i kassen. Gavekort fra fixit.no gjelder også her."),
        ("Snakker barbererne engelsk?", "Ja. Alle barbererne i Sandvika snakker engelsk."),
    ])

avd(slug="ski", title="Ski Storsenter", kortnavn="Ski Storsenter", ga4="ski_storsenter", rekkefolge=2, publisert=True,
    h1="Barbershop og herrefrisør i Ski Storsenter",
    undertittel="På brugangen i 2. etasje mot Telia, to minutter fra Ski stasjon. Flest barberere og åpent til 21.",
    seoTittel="Barbershop og herrefrisør Ski Storsenter | J&K Barber Shop",
    seoBeskrivelse="Barbershop og herrefrisør i Ski Storsenter, på brugangen mot Telia. Herreklipp, skin fade, skjeggtrim og barbering, to minutter fra Ski stasjon.",
    senter="Ski Storsenter", plassering="2. etasje, på brugangen som binder sammen nye og gamle delen, mot Telia.",
    gate="Jernbanesvingen 6", gatenavn="Jernbanesvingen", nr=6, postnr="1400", sted="Ski", kommune="Nordre Follo",
    parkering="Parkeringshus under og ved Ski Storsenter. 2 timer gratis parkering (senterets regler gjelder).",
    kollektiv="2 minutters gange fra Ski stasjon (Follobanen, Østfoldbanen) og Ski bussterminal. Fra Oslo S tar toget 12 minutter.",
    fixit=2881, apnet=2019,
    tider=("10:00-21:00",)*4 + ("09:00-21:00", "09:00-19:00", "Stengt"),
    prisniva="kr 399-1599", dropIn=True,
    oversikt="På brugangen mot Telia. Flest barberere, åpent til 21.",
    naboer=["asenveien", "kolbotn"],
    ingress="J&K Barber Shop i Ski Storsenter ligger på brugangen i 2. etasje, mellom den nye og den gamle delen av senteret, mot Telia. Her åpnet vi i 2019, og her får du klassisk herreklipp, skin fade, skjeggtrim og knivbarbering to minutter fra Ski stasjon.",
    beskrivelse=p(
        "J&K Barber Shop startet i Åsenveien 3 i 2018, og året etter, i 2019, åpnet vi avdeling nummer to her i Ski Storsenter. Siden den gang har det blitt over 400 anmeldelser på Google og mange tusen klipp. Ski er blitt by, Follobanen har gjort Oslo til en tolv minutters togtur, og senteret har vokst rundt oss. Vi står fortsatt på brugangen i 2. etasje, mellom den nye og den gamle delen, med Telia som nærmeste nabo.",
        "Avdelingen i Ski Storsenter er den av salongene våre med flest barberere og lengst åpningstid, og den som passer best når du vil ha time på kort varsel. Kundene kommer fra hele Nordre Follo: Ski, Langhus, Vevelstad, Siggerud, Kråkstad og Ås, og mange pendlere tar en klipp på vei hjem fra toget. Ski stasjon ligger to minutter unna, så du rekker en klassisk herreklipp mellom to avganger.",
        "Her gjør vi alt: skin fade for de unge fra Ski videregående og Drømtorp, klassisk klipp med skjeggtrim for dem som har gått hos oss siden 2019, knivbarbering for den som vil unne seg en halvtime med varme håndklær, og barneklipp for de minste. Alle behandlingene på menyen er for både menn og kvinner. Er du usikker på hvilken barberer du skal velge, ser du nivået til hver barberer i bookingen før du bestiller.",
        "Ski Storsenter er også senteret med flest frisører og barbere under samme tak. Det vi tilbyr som de andre ikke gjør, er kombinasjonen: barberere som er spesialister på kort hår og herreklipp, konsultasjon før hver klipp, produkter fra Reuzel, Uppercut Deluxe og Proraso i hyllene, og stempelkort i appen som gir deg den tiende behandlingen gratis.",
        "Vil du ha det enda roligere, ligger den andre Ski-avdelingen vår i Åsenveien 3, fem minutters gange unna, med parkering rett utenfor døren."),
    faq=[
        ("Hvor i senteret er dere?", "På brugangen i 2. etasje mellom nye og gamle delen, mot Telia. Kommer du fra stasjonen, går du inn i den nye delen og tar rulletrappen opp."),
        ("Er det parkering?", "Ja, i parkeringshuset under og ved senteret. De første 2 timene er gratis (senterets regler gjelder)."),
        ("Kan jeg komme uten time?", "Ja, når vi har ledig. Med flere barberere på jobb er sjansen god på hverdager før klokken 15. Ettermiddag og lørdag bør du bestille."),
        ("Hvor lang tid tar det fra Ski stasjon?", "To minutter til fots. Senterets inngang ligger rett over plassen fra stasjonsbygget."),
        ("Hva er forskjellen på dere og den andre J&K-avdelingen i Ski?", "Samme standard og nesten samme priser, Åsenveien 3 ligger noen kroner lavere på de fleste behandlinger. Ski Storsenter har flest barberere og lengst åpningstid. Åsenveien 3 er roligere, er der det hele startet i 2018, og har 1 time gratis parkering rett utenfor."),
        ("Har dere barneklipp?", "Ja, 499 kr for nivå Barber. Bestill gjerne en tidlig time på lørdag, da er det roligst for de minste."),
    ])

avd(slug="asenveien", title="Åsenveien 3, Ski", kortnavn="Åsenveien 3", ga4="asenveien", rekkefolge=3, publisert=True,
    h1="Barbershop og herrefrisør i Åsenveien 3, Ski sentrum",
    undertittel="Der det startet i 2018. Den roligste salongen vår, med 1 time gratis parkering rett utenfor døren.",
    seoTittel="Barbershop og herrefrisør Ski sentrum | J&K Barber Shop",
    seoBeskrivelse="J&K Barber Shop i Åsenveien 3 i Ski sentrum: der det startet i 2018, den roligste salongen vår, med gratis parkering rett utenfor. Herreklipp, skin fade og skjegg.",
    senter="", plassering="Gateplan, samme inngang som Unilabs. Inngang fra Åsenveien.",
    gate="Åsenveien 3", gatenavn="Åsenveien", nr=3, postnr="1400", sted="Ski", kommune="Nordre Follo",
    parkering="Parkeringsplasser rett utenfor døren, 1 time gratis parkering.",
    kollektiv="5 til 7 minutters gange fra Ski stasjon. Busstopp i Åsenveien.",
    fixit=2883, apnet=2018,
    tider=("10:00-20:00",)*5 + ("10:00-19:00", "Stengt"),
    prisniva="kr 399-1599", dropIn=True,
    oversikt="Der det startet i 2018. Den roligste salongen vår, 1 time gratis parkering rett utenfor.",
    naboer=["ski", "kolbotn"],
    ingress="J&K Barber Shop i Åsenveien 3 er der det hele startet i 2018, og den roligste av salongene våre. Samme inngang som Unilabs, 1 time gratis parkering rett utenfor døren. Her får du god tid i stolen til herreklipp, skin fade, skjeggtrim og tradisjonell knivbarbering.",
    beskrivelse=p(
        "Noen vil ha pulsen i kjøpesenteret. Andre vil ha ro. Åsenveien 3 er for dem som vil ha ro. Det var her J&K Barber Shop startet i 2018, et steinkast fra Ski Storsenter, og avdelingen har siden vært salongen vår for den som vil parkere rett utenfor, gå inn uten å passere femti butikker, og sette seg i stolen hos en barberer som har satt av god tid.",
        "Inngangen deler vi med Unilabs, så mange kombinerer en blodprøve med en klipp. Åsenveien 3 er også hovedkontoret til J&K, og det merkes: her prøver vi ut nye produkter først, her lærer vi opp nye barberere under oppsyn av erfarne barberere, og her tar vi oss tid til knivbarbering slik den skal gjøres, med varme håndklær og uten klokke i nakken.",
        "Kundene kommer fra Ski sentrum, Finstad, Hebekk, Langhus og Kråkstad, og mange av dem har gått her siden åpningen. Det er en avdeling med stamkunder, der barbereren vet hvordan du vil ha nakken før du har satt deg. Alle behandlingene på menyen er for både menn og kvinner, og nye kunder er like velkomne som de faste.",
        "Kommer du med tog, er det fem til sju minutters gange fra Ski stasjon, gjennom sentrum og over mot Åsenveien. Kommer du med bil, er det parkeringsplasser utenfor døren med 1 time gratis parkering, noe som gjør denne avdelingen til favoritten for dem som har liten tid men vil ha mye ro.",
        "Er det fullt hos oss, er Ski Storsenter-avdelingen fem minutter unna med flere barberere og lengre åpningstid."),
    faq=[
        ("Er det parkering?", "Ja, rett utenfor døren, med 1 time gratis parkering."),
        ("Hvor langt er det fra Ski stasjon?", "Fem til sju minutter til fots gjennom Ski sentrum."),
        ("Hva er forskjellen på Åsenveien 3 og Ski Storsenter?", "Samme standard, og Åsenveien ligger noen kroner lavere på de fleste behandlinger (klassisk herreklipp 585 kr mot 599 kr, nivå Barber). Åsenveien er mindre og roligere, med 1 time gratis parkering utenfor. Ski Storsenter har flere barberere og åpent til 21."),
        ("Kan jeg få knivbarbering her?", "Ja, og dette er avdelingen vi anbefaler for det. Vi setter av 30 minutter i bookingen."),
        ("Er dere åpne søndag?", "Nei. Mandag til fredag 10 til 20, lørdag 10 til 19."),
    ])

avd(slug="kolbotn", title="Kolbotn Torg", kortnavn="Kolbotn", ga4="kolbotn", rekkefolge=4, publisert=True,
    h1="Barbershop og herrefrisør på Kolbotn Torg",
    undertittel="Ved Vinmonopolet, kort vei fra Kolbotn stasjon. Stabilt team, mye barneklipp og 2 timer gratis parkering.",
    seoTittel="Barbershop og herrefrisør Kolbotn Torg | J&K Barber Shop",
    seoBeskrivelse="Barbershop og herrefrisør på Kolbotn Torg, ved Vinmonopolet. Herreklipp, skin fade, skjeggtrim og barbering. 2 timer gratis parkering. Bestill time.",
    senter="Kolbotn Torg", plassering="Ved Vinmonopolet.",
    gate="Strandliveien 4", gatenavn="Strandliveien", nr=4, postnr="1410", sted="Kolbotn", kommune="Nordre Follo",
    parkering="Parkeringshus i Kolbotn Torg. 2 timer gratis parkering (senterets regler gjelder).",
    kollektiv="1 til 2 minutters gange fra Kolbotn stasjon (Østfoldbanen, L2). Buss fra Sofiemyr, Tårnåsen, Oppegård og Greverud stopper ved torget.",
    fixit=2880, apnet=2020,
    tider=("10:00-21:00",)*5 + ("09:00-18:00", "Stengt"),
    prisniva="kr 399-1599", dropIn=True,
    oversikt="Ved Vinmonopolet. Stabilt team, mye barneklipp, 2 timer gratis parkering.",
    naboer=["ski", "asenveien"],
    ingress="J&K Barber Shop ligger på Kolbotn Torg, ved Vinmonopolet, kort vei fra togstasjonen. Her får du klassisk herreklipp, skin fade, skjeggtrim og knivbarbering, med 2 timer gratis parkering i senteret.",
    beskrivelse=p(
        "Kolbotn er et sted der folk kjenner hverandre, og barbershopen vår på Kolbotn Torg har siden mars 2020 vært en del av det. Vi ligger ved Vinmonopolet, kort vei fra togstasjonen, så du kan gå rett fra toget og inn i stolen på et par minutter. Polet er nabo, og det hender at kundene våre tar handelen der etterpå.",
        "Avdelingen på Kolbotn er den av salongene våre med flest anmeldelser i forhold til størrelsen, og med et snitt på 4,9 på Google. Det handler om barbererne. Her er det et stabilt team som har vært med lenge, og som har klippet mange av barna på Kolbotn fra første barneklipp til første skin fade før russetiden. Foreldre og barn som bestiller etter hverandre er noe av det vi ser mest av her, og barbererne er gode på å få de minste til å sitte stille.",
        "Kundene kommer fra hele gamle Oppegård: Kolbotn, Sofiemyr, Tårnåsen, Greverud, Myrvoll, Oppegård og Svartskog. Mange kjører, og da er 2 timer gratis parkering i senteret et poeng. Mange tar toget fra Oslo og hopper av på Kolbotn på vei hjem. Og en del går fra Ingieråsen og Kolbotn sentrum.",
        "Faglig er Kolbotn sterk på hele bredden: klassisk herreklipp med saks for dem som vil ha det tidløst, skin fade med skarpe linjer for dem som vil ha det moderne, skjeggtrim og knivbarbering for dem som vil ha begge deler. Alle behandlingene er for både menn og kvinner. Her finner du også de fleste av produktene vi selger, med Reuzel og Pan Drwal som de mest etterspurte.",
        "Vi holder åpent til 21 på hverdager og fra 9 på lørdag, og tar imot drop-in når vi har ledig. Det tryggeste er likevel å bestille time på nett eller i appen, der du også samler stempler."),
    faq=[
        ("Er parkeringen gratis?", "Ja, de første 2 timene i Kolbotn Torg sitt parkeringshus (senterets regler gjelder)."),
        ("Hvor er inngangen deres?", "Vi ligger ved Vinmonopolet, så går du mot polet, finner du oss."),
        ("Hvor lang tid tar det fra Kolbotn stasjon?", "Ett til to minutter til fots."),
        ("Passer det for barn?", "Ja, barneklipp er noe av det vi gjør mest av på Kolbotn. Barbererne er vant med barn i alle aldre, og vi har alltid noe å se på i stolen."),
        ("Kan jeg bestille time til meg og barnet mitt samtidig?", "Ja. Bestill to tider etter hverandre hos samme barberer i bookingen, eller ring oss, så setter vi det opp."),
        ("Kan jeg bare stikke innom?", "Ja, når vi har ledig. Hverdager før 15 er best. Ettermiddag og lørdag anbefaler vi å bestille."),
    ])

avd(slug="jessheim", title="Jessheim Storsenter", kortnavn="Jessheim", ga4="jessheim", rekkefolge=5, publisert=True,
    h1="Barbershop og herrefrisør i Jessheim Storsenter",
    undertittel="1. etasje mot Lindex, midt i Jessheim sentrum. Åpnet 2025, lett å få time, 2 timer gratis parkering.",
    seoTittel="Barbershop og herrefrisør Jessheim Storsenter | J&K",
    seoBeskrivelse="Barbershop og herrefrisør i Jessheim Storsenter, Storgata 6. Herreklipp, skin fade, skjeggtrim og knivbarbering av erfarne barberere. Bestill time online.",
    senter="Jessheim Storsenter", plassering="1. etasje, mot Lindex.",
    gate="Storgata 6", gatenavn="Storgata", nr=6, postnr="2050", sted="Jessheim", kommune="Ullensaker",
    parkering="Parkeringshus i Jessheim Storsenter. 2 timer gratis parkering (senterets regler gjelder).",
    kollektiv="Ca. 5 minutters gange fra Jessheim stasjon (Hovedbanen). Buss fra Gardermoen, Kløfta, Nannestad og Eidsvoll stopper ved senteret.",
    fixit=2952, apnet=2025,
    tider=("10:00-21:00",)*5 + ("10:00-19:00", "Stengt"),
    prisniva="kr 300-999", dropIn=True,
    oversikt="Åpnet 2025, 1. etasje mot Lindex, lett å få time.",
    naboer=["strommen"],
    ingress="J&K Barber Shop i Jessheim Storsenter, Storgata 6, er barbershopen for Ullensaker og Gardermoen-regionen. Klassisk herreklipp, skin fade, skjeggtrim og knivbarbering av erfarne barberere, i 1. etasje mot Lindex, midt i Jessheim sentrum med 2 timer gratis parkering i senteret og kort vei fra Jessheim stasjon.",
    beskrivelse=p(
        "Jessheim er en av de raskest voksende byene på Østlandet, og i 2025 åpnet vi dørene i Jessheim Storsenter for å være med på veksten. Avdelingen er en av de nyeste i kjeden, med nytt interiør i mørkt tre og messing, og et team av barberere som har tatt med seg erfaringen fra de andre avdelingene våre til Romerike. Du finner oss i 1. etasje, mot Lindex.",
        "Kundene våre i Jessheim er en blanding du ikke finner mange andre steder: folk som jobber på Gardermoen og vil ha en klipp mellom to skift, pendlere fra Hovedbanen, studenter og elever fra Jessheim videregående, familier fra Kløfta, Nannestad, Eidsvoll og Nordkisa som handler på senteret, og en god del som har flyttet til Jessheim fra Oslo og savnet en skikkelig barbershop. Vi hører ofte at det var akkurat det de lette etter.",
        "Jessheim Storsenter ligger midt i sentrum, med parkeringshus (2 timer gratis, senterets regler gjelder) og fem minutters gange fra Jessheim stasjon. Vi holder åpent til 21 på hverdager, så en time etter jobb på flyplassen eller etter toget fra Oslo går fint.",
        "Faglig satser vi i Jessheim tungt på skin fade og taper fade, som er det flest spør etter her, i tillegg til klassisk herreklipp, skjeggtrim og knivbarbering. Alle behandlingene er for både menn og kvinner. Som i de andre avdelingene starter alt med en kort konsultasjon, og du velger selv barberer og nivå når du bestiller.",
        "Vi er fortsatt nye i Jessheim, og det betyr to ting: du får lett time, og vi setter ekstra pris på tilbakemeldinger. Har du vært hos oss, legg gjerne igjen noen ord på Google. Har du ikke, bestill time og la oss vise hva vi kan."),
    faq=[
        ("Hvor i Jessheim Storsenter er dere?", "I 1. etasje, mot Lindex. Følg skiltene mot Lindex, så ser du oss."),
        ("Er det parkering?", "Ja, i senterets parkeringshus. De første 2 timene er gratis (senterets regler gjelder)."),
        ("Jeg jobber på Gardermoen. Rekker jeg en klipp mellom skift?", "Ja. Med bil tar det rundt 10 minutter fra flyplassen, og vi har åpent til 21 på hverdager. Bestill time i appen, så er stolen klar når du kommer."),
        ("Tar dere drop-in?", "Ja, når vi har ledig, og i Jessheim er sjansen god. Bestill likevel om du vil ha en bestemt barberer."),
        ("Har dere barneklipp?", "Ja, 399 kr for nivå Barber. Lørdag formiddag er roligst for de minste."),
    ])

avd(slug="strommen", title="Strømmen Storsenter", kortnavn="Strømmen", ga4="strommen", rekkefolge=6, publisert=True,
    h1="Barbershop og herrefrisør i Strømmen Storsenter",
    undertittel="1. etasje i den eldste delen av senteret, mellom Fransa og Gullfunn. Fem minutter fra Lillestrøm.",
    seoTittel="Barbershop og herrefrisør Strømmen Storsenter | J&K",
    seoBeskrivelse="Barbershop og herrefrisør i Strømmen Storsenter, Støperiveien 5. Herreklipp, skin fade, skjeggtrim og barbering, fem minutter fra Lillestrøm. Bestill time.",
    senter="Strømmen Storsenter", plassering="1. etasje i den eldste delen av senteret, mellom Fransa og Gullfunn.",
    gate="Støperiveien 5", gatenavn="Støperiveien", nr=5, postnr="2010", sted="Strømmen", kommune="Lillestrøm",
    parkering="Parkeringshus i Strømmen Storsenter. 2 timer gratis parkering (senterets regler gjelder).",
    kollektiv="3 til 5 minutters gange fra Strømmen stasjon (Hovedbanen, 15 minutter fra Oslo S). Buss fra Lillestrøm, Skjetten og Lørenskog stopper ved senteret.",
    fixit=2950, apnet=2025,
    tider=("10:00-21:00",)*5 + ("10:00-18:00", "Stengt"),
    prisniva="kr 329-1499", dropIn=True,
    oversikt="1. etasje i den eldste delen, fem minutter fra Lillestrøm.",
    naboer=["jessheim"],
    ingress="J&K Barber Shop i Strømmen Storsenter, Støperiveien 5, er barbershopen for Strømmen, Lillestrøm, Skjetten og Lørenskog. Klassisk herreklipp, skin fade, skjeggtrim og knivbarbering, i 1. etasje i den eldste delen av senteret, med 2 timer gratis parkering og kort vei fra Strømmen stasjon.",
    beskrivelse=p(
        "Strømmen Storsenter er et av Norges største kjøpesentre, og for mange på Nedre Romerike er det her uken handles inn. I 2025 åpnet vi barbershopen vår her, i 1. etasje i den eldste delen av senteret, mellom Fransa og Gullfunn, for å gi folk i Strømmen, Lillestrøm, Skjetten, Fjellhamar og Lørenskog et sted å få en ordentlig klipp uten å dra inn til Oslo. Avdelingen har i dag et snitt på 5,0 på Google, og det er en standard vi har tenkt å holde.",
        "Strømmen ligger på Hovedbanen, femten minutter fra Oslo S og fem minutter fra Lillestrøm, og stasjonen er noen minutters gange fra senteret. Mange av kundene våre hopper av her på vei hjem, tar en klipp og handler middag før de går videre. Andre kjører inn fra Skjetten, Skedsmokorset eller Lørenskog og parkerer i senterets parkeringshus, med 2 timer gratis (senterets regler gjelder).",
        "Barbererne i Strømmen er gode på hele programmet, men det er skin fade og kombinasjonen klipp og skjegg vi gjør mest av her. Mange kunder kommer med bilde av det de vil ha, og det liker vi. Konsultasjonen før klippen handler om å tilpasse bildet til ditt hår og din hodeform, slik at resultatet blir like bra på deg som på bildet. Knivbarbering med varme håndklær tilbyr vi også, og det er en fin måte å avslutte en handletur på. Alle behandlingene er for både menn og kvinner.",
        "Strømmen og Lillestrøm har flere barbershops, og flere av dem er dyktige. Det vi tilbyr i tillegg er en kjede med sju avdelinger og felles stempelkort, slik at stemplene du samler i Strømmen også gjelder i Jessheim eller Sandvika, barberere med tydelige nivåer så du vet hva du betaler for, og en salong midt i senteret du likevel besøker.",
        "Bestill time på nett eller i appen, eller stikk innom når du er på senteret og se om vi har ledig."),
    faq=[
        ("Hvor i senteret finner jeg dere?", "I 1. etasje i den eldste delen av senteret, mellom Fransa og Gullfunn."),
        ("Er det parkering?", "Ja, i senterets parkeringshus. De første 2 timene er gratis (senterets regler gjelder)."),
        ("Hvor lang tid tar det fra Strømmen stasjon?", "Tre til fem minutter til fots."),
        ("Jeg bor i Lillestrøm. Er dere nærmest?", "Vi er fem minutter unna med tog eller bil, og du parkerer i senteret. Stemplene i appen gjelder i alle avdelingene våre."),
        ("Tar dere drop-in?", "Ja, når vi har ledig. Bestill time om du vil være sikker, særlig lørdag."),
        ("Har dere barneklipp?", "Ja, 429 kr for nivå Barber."),
    ])

avd(slug="rykkinn", title="Rykkinn Senter", kortnavn="Rykkinn", ga4="rykkinn", rekkefolge=7, publisert=False,
    h1="Barbershop og herrefrisør på Rykkinn Senter",
    undertittel="Den eneste barbershopen i Bærum vest. 1. etasje, med 2 timer gratis parkering ved senteret.",
    seoTittel="Barbershop og herrefrisør Rykkinn Senter | J&K Barber Shop",
    seoBeskrivelse="Barbershop og herrefrisør på Rykkinn Senter, Munins vei 1. Herreklipp, skin fade, skjeggtrim og barneklipp for hele Bærum vest. Bestill time online.",
    senter="Rykkinn Senter", plassering="1. etasje.",
    gate="Munins vei 1", gatenavn="Munins vei", nr=1, postnr="1348", sted="Rykkinn", kommune="Bærum",
    parkering="Parkering ved senteret. 2 timer gratis parkering (senterets regler gjelder).",
    kollektiv="Buss fra Sandvika, Bærums Verk og Kolsås stopper ved Rykkinn senter. Kolsås T-banestasjon ligger ca. 10 minutter unna med buss.",
    fixit=2964, apnet=2025,
    tider=("10:00-20:00",)*5 + ("09:00-18:00", "Stengt"),
    prisniva="kr 300-1499", dropIn=True,
    oversikt="Eneste barbershop i Bærum vest. 1. etasje.",
    naboer=["sandvika"],
    ingress="J&K Barber Shop på Rykkinn Senter, Munins vei 1, er den eneste barbershopen i Bærum vest. Klassisk herreklipp, skin fade, skjeggtrim og barneklipp for Rykkinn, Bærums Verk, Kolsås, Gommerud og Lommedalen, i 1. etasje, med 2 timer gratis parkering ved senteret.",
    beskrivelse=p(
        "Rykkinn er et av de største boligområdene i Bærum, og Rykkinn Senter er nærbutikken, apoteket og møteplassen for alle som bor på Rykkinn, Gommerud, Berger og i Lommedalen. Vi åpnet her i 2025, i 1. etasje, og er den eneste barbershopen i senteret og i hele Bærum vest. Det tar vi på alvor. Her skal du slippe å kjøre til Sandvika eller Bekkestua for en skikkelig herreklipp.",
        "Avdelingen på Rykkinn er liten og personlig. Barbereren kjenner kundene, og kundene kjenner barbereren. Det er mye barneklipp her, siden Rykkinn er et barnefamilieområde, og vi er vant med at foreldre kommer med to barn og vil ha alle tre klippet på rad. Det ordner vi. Det er også mange godt voksne kunder som har bodd på Rykkinn siden blokkene var nye, og som setter pris på en klassisk klipp med saks og en rolig prat.",
        "Samtidig gjør vi akkurat det samme her som i de andre avdelingene: skin fade med rene linjer, skjeggtrim med kniv, knivbarbering med varme håndklær. Alle behandlingene er for både menn og kvinner. Produktene fra Reuzel, Uppercut Deluxe og Proraso står i hyllene, og stempelkortet i appen gjelder her like mye som i Sandvika.",
        "Praktisk er Rykkinn lett: 2 timer gratis parkering rett utenfor, buss fra Sandvika og Kolsås til døren, og åpent til 20 på hverdager og fra 9 på lørdag. Er det fullt hos oss, er Sandvika-avdelingen vår tolv minutter unna med bil."),
    faq=[
        ("Er parkeringen gratis?", "Ja, de første 2 timene ved senteret (senterets regler gjelder)."),
        ("Hvor i senteret er dere?", "I 1. etasje."),
        ("Kan jeg komme med flere barn samtidig?", "Ja, bestill flere tider etter hverandre i bookingen, eller ring så hjelper vi deg."),
        ("Tar dere drop-in?", "Ja, når vi har ledig. Siden vi er en liten avdeling, anbefaler vi å bestille."),
        ("Er det samme priser som i Sandvika?", "Nei, Rykkinn har egne priser som ligger litt under Sandvika: klassisk herreklipp koster 539 kr på Rykkinn mot 639 kr i Sandvika (nivå Barber). Stempelkortet gjelder på tvers av alle avdelingene."),
    ])

DAGER = ["apentMan", "apentTir", "apentOns", "apentTor", "apentFre", "apentLor", "apentSon"]
avd_items = []
for a in A:
    full = "%s, %s %s" % (a["gate"], a["postnr"], a["sted"])
    d = {
        "title": a["title"], "slug": a["slug"], "kortnavn": a["kortnavn"], "ga4Avdeling": a["ga4"],
        "publisert": a["publisert"], "rekkefolge": a["rekkefolge"], "h1": a["h1"], "undertittel": a["undertittel"],
        "ingress": a["ingress"],
        "seoTittel": a["seoTittel"], "seoBeskrivelse": a["seoBeskrivelse"],
        "senter": a["senter"], "plassering": a["plassering"],
        "gateadresse": a["gate"], "postnummer": a["postnr"], "poststed": a["sted"], "kommune": a["kommune"],
        "adresse": {"formatted": full + ", Norge", "streetAddress": {"name": a["gatenavn"], "number": a["nr"]},
                    "city": a["sted"], "postalCode": a["postnr"], "country": "NO", "subdivision": "Akershus"},
        "telefon": TEL, "telefonVisning": TELV, "epost": EPOST,
        "fixitId": a["fixit"], "fixitUrl": "https://fixit.no/booking/%d" % a["fixit"],
        "fixitBehandlingerUrl": "https://fixit.no/booking/%d/behandlinger" % a["fixit"],
        "mapsUrl": maps(full),
        "parkering": a["parkering"], "kollektiv": a["kollektiv"],
        "apningstiderAvvik": "<p>Åpningstidene følger senteret. Avvikende tider i høytider vises i bookingen og på Google.</p>",
        "beskrivelse": a["beskrivelse"],
        "adkomst": p("<strong>Plassering:</strong> " + a["plassering"], "<strong>Parkering:</strong> " + a["parkering"], "<strong>Kollektiv:</strong> " + a["kollektiv"]),
        "dropIn": a["dropIn"], "prisniva": a["prisniva"], "status": "apen", "apnet": a["apnet"],
        "oversiktTekst": a["oversikt"], "naboSlugs": ",".join(a["naboer"]),
        "bestillKnapp": "Bestill time %s %s" % ("på" if a["slug"] in ("kolbotn", "rykkinn") else "i", a["kortnavn"]),
    }
    for k, v in zip(DAGER, a["tider"]):
        d[k] = v
    avd_items.append({"id": a["slug"], "data": d})

# ---------------------------------------------------------------- TJENESTER
KNAPPER = "Bestill i: Sandvika, Ski Storsenter, Åsenveien 3, Kolbotn, Jessheim, Strømmen og Rykkinn."
T = []
def tj(**k):
    T.append(k)

tj(slug="herreklipp", title="Klassisk herreklipp", rekkefolge=1, h1="Klassisk herreklipp", knapp="Bestill herreklipp",
   seoTittel="Klassisk herreklipp | J&K Barber Shop",
   seoBeskrivelse="Klassisk herreklipp med konsultasjon, vask og styling hos erfarne barberere i Sandvika, Ski, Kolbotn, Jessheim, Strømmen og Rykkinn. Se pris, bestill time.",
   ingress="Saks og maskin, vask og styling. Klippen som ser like bra ut på mandag som på lørdag.",
   intro="En klassisk herreklipp hos J&K Barber Shop er en klipp som er tilpasset deg: hodeform, hårtype, hvordan du styler den til daglig, og hvordan du vil at den skal vokse ut. Saks og maskin, vask, styling og en barberer som har tid. Behandlingen er for både menn og kvinner.",
   fra=449, til=639, varighet=30, varighetTekst="Vi setter av 30 minutter i bookingen, med vask og styling inkludert.",
   far=ul(["Konsultasjon i stolen før vi begynner: hva du vil ha, hva du hadde sist, og hva som fungerer med ditt hår.",
           "Klipp med saks og maskin, tilpasset lengde på sidene og toppen, og rene linjer i nakken og rundt ørene.",
           "Hårvask inngår i klippen på alle nivåer. Du velger selv om du vil ha vask.",
           "Styling med produkter fra Reuzel, Uppercut Deluxe, Slickhaven eller HUFS, og tips om hvordan du får til det samme hjemme.",
           "Rens av nakke og kinn med maskin eller kniv for en ren avslutning."]),
   slik="Du setter deg i stolen, og barbereren spør hva du vil ha. Har du bilde, vis det. Har du ikke, beskriver du hvordan du vil ha det, og barbereren foreslår hva som kler deg. Så klipper vi: sidene først, deretter toppen, deretter detaljene. Underveis sjekker vi med deg i speilet. Til slutt vasker vi ut løst hår, styler og viser deg resultatet fra alle vinkler. Er det noe du vil justere, gjør vi det før du går.",
   hvem="Alle som vil ha en klipp som ser bra ut i tre til fem uker, enten du vil ha det kort og enkelt, side part med lengde på toppen, slickback, teksturert topp eller lengre hår med form. Vil du ha skin fade på sidene, bestiller du skin fade i stedet; den inkluderer klipp på toppen.",
   for_="Kom med rent eller nesten rent hår, uten tunge produkter, så barbereren ser hvordan håret faller naturlig. Ta med bilde om du har et.",
   etter="Vent 24 timer før du vasker håret om du har fått styling du liker. Bestill neste time før du går, tre til fem uker frem, så holder klippen seg. I appen får du stempel for hver klassiske klipp.",
   niva="Velger du en Senior, koster klippen 50 kr mer enn prisen i tabellen. Lærling og Junior ligger litt under der avdelingen har det. Alle nivåer jobber etter samme standard med samme produkter; forskjellen er erfaring. Har du vært hos oss de siste 15 dagene, kan du bestille Re-fresh klassisk hårklipp (15 minutter, 449 kr i Sandvika, 399 kr i Ski Storsenter, Åsenveien 3 og Kolbotn; tilbys ikke i Jessheim, Strømmen og Rykkinn).",
   blogg1="https://www.j-kbarber.no/blogg/hvor-ofte-bor-menn-klippe-seg", relaterte="skin-fade,kombo",
   faq=[("Hvor ofte bør jeg klippe meg?", "Kort hår: hver tredje til fjerde uke. Mellomlangt: hver fjerde til sjette uke. Lengre hår: hver sjette til åttende uke for å holde formen."),
        ("Inngår vask i prisen?", "Ja. Hårvask inngår i klippen på alle nivåer, uten tillegg, og du velger selv om du vil ha vask eller ikke."),
        ("Kan jeg få klippet skjegget samtidig?", "Ja, bestill Kombo, så får du klipp og skjeggtrim i samme time hos samme barberer."),
        ("Hva om jeg ikke blir fornøyd?", "Si fra i stolen, så justerer vi før du går. Oppdager du noe hjemme, ring eller send e-post innen en uke, så retter vi det.")])

tj(slug="skin-fade", title="Skin fade", rekkefolge=2, h1="Skin fade og taper fade", knapp="Bestill skin fade",
   seoTittel="Skin fade hos erfaren barber | J&K Barber Shop",
   seoBeskrivelse="Skin fade, taper fade og low, mid og high fade utført med presisjon. Se hva du får, hvor lang tid det tar og hva det koster. Bestill hos nærmeste avdeling.",
   ingress="Fra hud til lengde uten synlige overganger. Low, mid eller high, med eller uten tekstur på toppen.",
   intro="Skin fade er en klipp der sidene går fra bar hud nederst til full lengde øverst, uten synlige overganger. Det ser enkelt ut og er det vanskeligste vi gjør. Hos J&K Barber Shop får du skin fade av barberere som har gjort det tusenvis av ganger, med konsultasjon om høyde, form og topp før vi starter. Behandlingen er for både menn og kvinner.",
   fra=599, til=829, varighet=45, varighetTekst="Vi setter av 45 minutter i bookingen. Med skjeggtrim (Kombo II) settes det av 60 minutter.",
   far=ul(["Konsultasjon om hvilken fade som passer deg: low, mid eller high, skin eller taper, og hvordan toppen skal klippes.",
           "Fade med maskin i flere lengder, trinnvis blending til null med foil shaver og kniv der det trengs.",
           "Klipp og form på toppen: teksturert, crop, slickback, quiff eller lengde.",
           "Rene linjer i panne, tinning og nakke, formet med trimmer og kniv.",
           "Vask, styling og råd om hvordan du holder fade-en frisk mellom besøkene."]),
   slik="Vi starter med å bli enige om tre ting: hvor høyt fade-en skal starte (low ligger rett over øret, mid midt på siden, high oppe mot kronen), om det skal være skin (null nederst) eller taper (kort men ikke bart), og hva som skal skje på toppen. Deretter legger barbereren inn referanselinjene, jobber seg oppover i lengder og blender overgangene til de forsvinner. Toppen klippes og tilpasses fade-en. Til slutt tegnes linjene opp, vi vasker ut og styler. En god fade sjekkes fra alle vinkler i speilet før du reiser deg.",
   hvem="Skin fade passer de fleste hodeformer, men høyden bør tilpasses: low fade er mest diskret og fungerer godt på jobb, high fade er tøffest og krever hyppigere vedlikehold. Har du krøller, fungerer en mid fade med tekstur på toppen svært godt. Har du tynt hår på toppen, anbefaler vi ofte taper fremfor skin, fordi kontrasten blir mindre. Spør barbereren.",
   for_="Kom med rent hår uten produkt. Ta med bilde av fade-en du vil ha; de fleste gjør det, og det gjør konsultasjonen enklere.",
   etter="En skin fade er skarpest de første 7 til 10 dagene. Vil du holde den skarp, bestill ny time etter to til tre uker. Har du vært hos oss de siste 15 dagene, kan du bestille Re-fresh skin fade til lavere pris i Sandvika, Ski Storsenter, Åsenveien 3 og Kolbotn. Line-up er ikke en egen tjeneste hos oss; linjene i skjegget inngår i skjeggtrimmen. Bruk en lett matte paste eller sjøsaltspray på toppen, så beholder du teksturen.",
   niva="Velger du en Senior, koster skin fade 50 kr mer enn prisen i tabellen. Skin fade er den behandlingen der nivået betyr mest, fordi blendingen krever trening. Vil du ha den skarpeste overgangen, velg Barber eller Senior. Har du vært hos oss de siste 15 dagene, kan du bestille Re-fresh skin fade (30 minutter, 625 kr i Sandvika, 580 kr i Ski Storsenter, Åsenveien 3 og Kolbotn; tilbys ikke i Jessheim, Strømmen og Rykkinn).",
   blogg1="https://www.j-kbarber.no/blogg/skin-fade-taper-fade-forskjellen", relaterte="kombo",
   faq=[("Hva er forskjellen på skin fade og taper fade?", "Skin fade går helt ned til bar hud nederst. Taper fade går kort, men ikke bart, og er mer diskret. Begge kan være low, mid eller high."),
        ("Hvor ofte må jeg ta skin fade?", "Hver andre til tredje uke om du vil ha den skarp hele tiden. Hver fjerde uke om du tåler at den vokser litt ut."),
        ("Kan jeg ta skin fade med skjegg?", "Ja, og det er en av de vanligste kombinasjonene våre. Bestill Kombo, så fader vi også overgangen mellom skjegg og hår."),
        ("Får jeg stempel i appen for skin fade?", "Ja. Skin fade har sitt eget stempelkort i appen. Hvert tiende stempel gir deg behandlingen gratis, og barbereren registrerer stempelet i salongen.")])

tj(slug="skjeggtrim", title="Skjeggtrim", rekkefolge=3, h1="Skjeggtrim og skjeggforming", knapp="Bestill skjeggtrim",
   seoTittel="Skjeggtrim og skjeggforming | J&K Barber Shop",
   seoBeskrivelse="Skjeggtrim, konturbarbering med kniv og skjeggtrim deluxe med varme håndklær og skjeggolje. Se pris per avdeling og bestill time hos J&K Barber Shop.",
   ingress="Form, lengde og rene linjer med kniv. Deluxe-varianten gir deg varme håndklær og skjeggolje på toppen.",
   intro="Et godt skjegg er ikke tilfeldig. Hos J&K Barber Shop former vi skjegget etter ansiktet ditt, med maskin, saks og kniv, og lærer deg hvordan du holder formen hjemme. Velg vanlig skjeggtrim eller deluxe med varme håndklær og skjeggolje.",
   fra=399, til=579, varighet=28, varighetTekst="Vi setter av 28 minutter til skjeggtrim og 60 minutter til skjeggtrim deluxe i bookingen.",
   far="<p><strong>Skjeggtrim</strong></p>" + ul(["Konsultasjon om lengde, form og hvor linjene skal gå.", "Trim med maskin og saks til jevn lengde, eller fade i skjegget om du vil ha det.", "Konturer (line-up) på kinn og hals med kniv eller trimmer. Line-up inngår alltid i skjeggtrimmen.", "Skjeggolje eller balm til slutt."]) + "<p><strong>Skjeggtrim deluxe</strong></p>" + ul(["Alt over, pluss varmt håndkle før konturbarberingen, barberkrem og kniv på kinn og hals, kaldt håndkle og pleie etterpå."]),
   slik="Vi ser på skjegget sammen i speilet og blir enige om form: hvor høyt kinnlinjen skal gå, hvor halslinjen skal ligge (vanligvis en fingerbredde over adamseplet), og hvor langt det skal være. Barbereren trimmer ned til lengde, former med saks der det trengs, og tegner opp linjene. Velger du deluxe, legger vi et varmt håndkle over kinnene og barberer konturene med kniv, slik at linjene blir helt rene. Til slutt får du olje eller balm, og råd om hva du bør bruke hjemme.",
   hvem="Alle med skjegg, fra tre ukers stubb som trenger linjer, til fullskjegg som trenger form og lengde. Skjeggtrim passer også godt om du er i ferd med å gro ut skjegg og vil ha hjelp til å få det til å se bevisst ut underveis. Har du ujevn vekst, kan barbereren forme slik at det synes mindre.",
   for_="Vask skjegget samme dag, uten olje, så barbereren ser den naturlige veksten. Tenk over om du vil ha det kortere eller bare renere.",
   etter="Skjeggolje daglig holder huden under skjegget myk og hindrer flass. Børst skjegget nedover om morgenen. Gjenta trim hver tredje til fjerde uke for å holde formen. Skjeggtrim gir stempel i appen.",
   niva="Velger du en Senior, koster skjeggtrim 70 kr mer og deluxe 100 kr mer enn prisen i tabellen. Konturer med kniv gjøres av alle nivåer. Har du vært hos oss de siste 15 dagene, kan du bestille Re-fresh skjeggtrim (15 minutter, 429 kr i Sandvika, 399 kr i Ski Storsenter, Åsenveien 3 og Kolbotn; tilbys ikke i Jessheim, Strømmen og Rykkinn).",
   blogg1="https://www.j-kbarber.no/blogg/slik-styler-du-skjegget", relaterte="barbering",
   faq=[("Hvor ofte bør jeg trimme skjegget?", "Hver tredje til fjerde uke for form. Konturene kan du vedlikeholde hjemme med trimmer mellom besøkene."),
        ("Kan jeg ta skjeggtrim sammen med klipp?", "Ja, bestill Kombo. Da får du klipp eller skin fade og skjeggtrim i samme time."),
        ("Hva er forskjellen på skjeggtrim og deluxe?", "Deluxe har varmt håndkle, barberkrem og knivbarbering av konturene, pluss kaldt håndkle og pleie. Det tar lengre tid og gir renere linjer."),
        ("Hvilke produkter anbefaler dere?", "Skjeggolje fra Pan Drwal eller Proraso daglig, balm om skjegget er langt, og en skjeggbørste. Vi har alt i salongen og på j-kshop.no.")])

tj(slug="barbering", title="Knivbarbering", rekkefolge=4, h1="Knivbarbering", knapp="Bestill knivbarbering",
   seoTittel="Knivbarbering, tradisjonell barbering | J&K Barber Shop",
   seoBeskrivelse="Tradisjonell barbering med kniv, varme håndklær, barberkrem og etterbehandling. Et ritual på 30 minutter hos J&K Barber Shop. Se pris og bestill time.",
   ingress="Varme håndklær, barberkrem, kniv og etterbehandling. Tradisjonen slik den skal gjøres.",
   intro="Tradisjonell barbering med kniv er den eldste tjenesten i faget og den vi er stoltest av. Varme håndklær, barberkrem pisket for hånd, kniv i rolige strøk, kaldt håndkle og etterbehandling. Tretti minutter du ikke får andre steder.",
   fra=399, til=529, varighet=30, varighetTekst="Vi setter av 30 minutter i bookingen. Med skjeggtrim deluxe eller klipp i tillegg, se Kombo.",
   far=ul(["Forberedelse med varmt håndkle og pre-shave-olje som mykgjør skjeggstubbene og åpner porene.",
           "Barberkrem fra Proraso eller Taylor of Old Bond Street, påført med kost.",
           "Barbering med kniv i to omganger: med veksten, så mot eller på tvers der huden tåler det.",
           "Kaldt håndkle som lukker porene, deretter aftershave-balm uten alkohol som roer huden.",
           "Hodebarbering med kniv tilbys på samme måte, som egen behandling i bookingen."]),
   slik="Du legges bakover i stolen. Barbereren legger et varmt håndkle over ansiktet og lar det ligge i noen minutter mens oljen virker. Så piskes kremen og legges på med kost. Barberingen gjøres med kniv, stramt skinn og korte, rolige strøk, først med veksten over hele ansiktet, deretter en ny runde krem og en andre omgang for det helt glatte resultatet. Kaldt håndkle, balm, og du er ferdig. Mange sovner. Det er lov.",
   hvem="Deg som vil ha helt glatt hud, deg som vil unne deg en halvtime med ro, deg som skal i bryllup, konfirmasjon eller jobbintervju, og deg som aldri har prøvd og er nysgjerrig. Har du sensitiv hud eller mye inngrodde hår, si fra, så tilpasser barbereren antall omganger og produkter.",
   for_="Ikke barber deg selv de siste to til tre dagene; litt lengde gjør jobben lettere og resultatet bedre. Kom med ren hud.",
   etter="Unngå alkoholholdig aftershave og sterk sol de første timene. Bruk fuktighetskrem. Resultatet holder glattere og lenger enn hjemmebarbering, typisk to til tre dager før du kjenner stubb.",
   niva="Velger du en Senior, koster barberingen 50 til 100 kr mer enn prisen i tabellen. Knivbarbering utføres av barberere med opplæring i knivbarbering. Du velger barberer i bookingen.",
   blogg1="https://www.j-kbarber.no/blogg/knivbarbering-slik-foregar-det", relaterte="skjeggtrim",
   faq=[("Gjør det vondt?", "Nei. Varmt håndkle og riktig krem gjør huden klar, og kniven i trente hender er mer skånsom enn de fleste maskiner."),
        ("Er det trygt?", "Ja. Vi bruker engangsblad som byttes for hver kunde, og barbererne er trent i hygiene og teknikk."),
        ("Kan jeg få barbert hodet?", "Ja, hodebarbering med kniv tilbys i alle avdelinger. Bestill Hodebarbering med kniv i bookingen, eller Kombo III om du vil ha hode og skjegg barbert i samme time."),
        ("Kan jeg kombinere med klipp?", "Ja. Bestill Kombo med knivbarbering, eller legg til barbering på en vanlig klipp i bookingen.")])

tj(slug="barneklipp", title="Barneklipp", rekkefolge=5, h1="Barneklipp", knapp="Bestill barneklipp",
   seoTittel="Barneklipp hos barberer | J&K Barber Shop",
   seoBeskrivelse="Barneklipp hos barberere som er vant med barn i alle aldre. Trygt, rolig og uten stress, i Sandvika, Ski, Kolbotn, Jessheim, Strømmen og Rykkinn. Bestill time.",
   ingress="For barn som sitter i stolen for første gang, og for dem som allerede vet hva de vil ha.",
   intro="Barneklipp hos J&K Barber Shop er for barn fra første klipp til de er store nok til å bestille selv, gutter og jenter. Barbererne våre er vant med alt fra tårer til tydelige meninger, og tar seg tiden som trengs. Prisen for nivå Barber er 399 til 529 kr avhengig av avdeling, og foreldre kan bestille time rett etter hos samme barberer.",
   fra=399, til=529, varighet=30, varighetTekst="Vi setter av 30 minutter i bookingen (45 minutter for barneklipp skin fade), så det er tid nok uansett alder og klipp.",
   far=ul(["En barberer som snakker med barnet, ikke bare med deg.",
           "Klipp med saks og maskin tilpasset alder, hårtype og det barnet (eller du) vil ha.",
           "Rolig tempo, pauser når det trengs, og noe å se på i stolen.",
           "Styling til slutt så barnet får se resultatet. Barneklipp gir ikke stempel i appen, men tar du klipp samtidig, får du stempel for din egen klipp."]),
   slik="Vi setter barnet i stolen (eller på fanget til en voksen om det er lite) og viser maskinen og saksen før vi begynner. Barbereren spør hva barnet vil ha, og tar hensyn til det så langt det går. Vi starter med det som er enklest og minst kilent, og tar nakken og ørene til slutt. Blir det for mye, tar vi en pause. Målet er at barnet vil komme tilbake, ikke at vi blir ferdige på tid.",
   hvem="Barn i alle aldre, fra første klipp til ungdomsskolen. Også for barnet som vil ha skin fade som storesøsken: det gjør vi gjerne, tilpasset alder og hår, bestill Barneklipp skin fade. Og for foreldre som vil klippe seg samtidig og slippe to turer.",
   for_="Fortell barnet hva som skal skje, gjerne med bilder fra siden vår. Kom med rent hår. Ikke rett etter barnehagen når barnet er slitent, heller formiddag i helgen. Ta med noe barnet liker å holde i.",
   etter="Ros barnet. Bestill neste time hos samme barberer, så blir dere kjent. Fem til seks uker er vanlig for barneklipp.",
   niva="Barneklipp gjelder barn under 12 år, slik det står i bookingen. Fra 12 år bestilles herreklipp eller skin fade. Velger du en Senior, koster barneklippen 50 kr mer enn prisen i tabellen.",
   blogg1="https://www.j-kbarber.no/blogg/barneklipp-forste-gang-tips", relaterte="herreklipp",
   faq=[("Hvor gammelt bør barnet være første gang?", "Når håret er i veien, vanligvis fra ett til to år. Yngre barn sitter på fanget til en voksen."),
        ("Hva om barnet gråter?", "Da tar vi en pause, eller gjør det ferdig på fanget. Barbererne våre har sett det før, og ingen blir stresset."),
        ("Kan jeg bestille til meg og barnet mitt samtidig?", "Ja. Bestill to tider etter hverandre hos samme barberer i bookingen, så slipper dere å vente på hverandre."),
        ("Klipper dere både gutter og jenter?", "Ja. Alle behandlingene på menyen er for både gutter og jenter, og vi er spesialister på kort hår og skin fade. Vil barnet ha en lengre, klassisk klipp med mer forming, anbefaler vi søstersalongen vår J&K Beauty Salon i Ski (j-kbeauty.no).")])

tj(slug="kombo", title="Kombo: klipp og skjegg", rekkefolge=6, h1="Kombo: klipp og skjegg i ett besøk", knapp="Bestill kombo",
   seoTittel="Kombo: klipp og skjeggtrim i ett | J&K Barber Shop",
   seoBeskrivelse="Kombo hos J&K Barber Shop: herreklipp eller skin fade sammen med skjeggtrim eller knivbarbering, i ett besøk hos samme barberer. Se priser og bestill time.",
   ingress="Klipp eller skin fade og skjeggtrim i samme time, hos samme barberer.",
   intro="Kombo er for deg som vil ha hår og skjegg gjort samtidig, av samme barberer, med overgangene mellom dem tilpasset hverandre. Velg klassisk herreklipp eller skin fade på toppen, og skjeggtrim eller knivbarbering under.",
   fra=799, til=1279, varighet=60, varighetTekst="Kombo I og Kombo II er satt opp med 60 minutter i bookingen, Kombo III med 45 minutter og Kombo deluxe med 90 minutter.",
   far="<p><strong>Kombo I: Herreklipp og skjeggtrim eller knivbarbering</strong></p>" + ul(["Klassisk herreklipp med konsultasjon, vask og styling.", "Skjeggtrim med form, lengde og konturer, eller full knivbarbering med varme håndklær om du heller vil ha glatt hud. Du velger i stolen.", "Overgangen mellom kinnskjegg og hår tilpasset slik at det henger sammen."]) +
       "<p><strong>Kombo II: Skin fade og skjeggtrim eller knivbarbering</strong></p>" + ul(["Skin fade (low, mid eller high) med klipp på toppen.", "Skjeggtrim med fade i overgangen til hår, konturer med kniv, eller full knivbarbering.", "Vask, styling og skjeggolje."]) +
       "<p><strong>Kombo III: Hode- og skjeggbarbering med kniv</strong></p>" + ul(["Barbering av både hode og skjegg med kniv, varme håndklær og etterbehandling, 45 minutter."]) +
       "<p><strong>Kombo deluxe</strong></p>" + ul(["Hårklipp deluxe og skjeggtrim deluxe eller barbering deluxe i samme time, med hodebunnsmassasje, 90 minutter."]),
   slik="Vi starter med konsultasjonen om begge deler, fordi skjegg og hår må passe sammen: en high skin fade med langt fullskjegg ser annerledes ut enn en low fade med kort stubb. Så klipper vi håret først, deretter skjegget, og til slutt jobber barbereren med overgangen på kinnbeinet og foran øret så det hele ser ut som en helhet. Vask, styling, olje.",
   hvem="Deg med skjegg som klipper deg jevnlig. De fleste med skjegg trenger trim like ofte som klipp, og det er enklere å få begge deler gjort samtidig, hos en person som ser helheten. Kombo er også det vi anbefaler før bryllup, fest og fotografering.",
   for_="Kom med rent hår og vasket skjegg, uten produkter. Ha en tanke om hvor langt skjegget skal være, eller la barbereren foreslå.",
   etter="Hold linjene hjemme med trimmer, bruk skjeggolje daglig, og bestill ny kombo etter tre til fire uker. Da ser det alltid nyklippet ut.",
   niva="Velger du en Senior, koster kombo 50 til 100 kr mer enn prisen i tabellen. Kombo er litt rimeligere enn å bestille de to behandlingene hver for seg: i Sandvika koster klassisk herreklipp og skjeggtrim 1 218 kr hver for seg og 1 029 kr som Kombo I. Kombo har sitt eget stempelkort i appen: hver kombo gir ett stempel på kombokortet, og den tiende komboen er gratis.",
   blogg1="", relaterte="skin-fade,skjeggtrim,barbering",
   faq=[("Kan jeg velge skin fade i kombo?", "Ja, det er Kombo II. Skin fade i håret og fade i overgangen til skjegget."),
        ("Får jeg to stempler for kombo?", "Nei, kombo har sitt eget stempelkort i appen. Hver kombo gir ett stempel på kombokortet, og det tiende gir deg gratis kombo. Klassisk klipp, Skin fade og Skjeggtrim har egne stempelkort når du bestiller dem hver for seg. Barbereren registrerer stempelet i salongen."),
        ("Hvor lang tid må jeg sette av?", "Rundt en time for Kombo I og II, tre kvarter for Kombo III og halvannen time for Kombo deluxe. Tiden står i bookingen."),
        ("Kan jeg bestille kombo for barnet mitt?", "Kombo er for voksne med skjegg. For barn bestiller du barneklipp.")])

tj_items = []
for t in T:
    besk = ("<p>%s</p><h2>Hva du får</h2>%s<h2>Slik foregår det</h2><p>%s</p><h2>Hvem passer det for</h2><p>%s</p>"
            "<h2>Før og etter</h2><p><strong>Før:</strong> %s</p><p><strong>Etter:</strong> %s</p>") % (
        t["intro"], t["far"], t["slik"], t["hvem"], t["for_"], t["etter"])
    d = {
        "title": t["title"], "slug": t["slug"], "publisert": True, "rekkefolge": t["rekkefolge"], "h1": t["h1"],
        "seoTittel": t["seoTittel"], "seoBeskrivelse": t["seoBeskrivelse"], "ingress": t["ingress"],
        "beskrivelse": besk, "fraPris": t["fra"], "tilPris": t["til"],
        "pristekst": "%d til %d kr" % (t["fra"], t["til"]),
        "prisnivaer": p(STD, t["niva"]),
        "varighetMin": t["varighet"], "varighetTekst": t["varighetTekst"],
        "knappetekst": t["knapp"], "fixitKode": "",
        "bloggUrl1": t["blogg1"] or None, "relaterteSlugs": t["relaterte"],
        "avdelingSlugs": "sandvika,ski,asenveien,kolbotn,jessheim,strommen,rykkinn",
    }
    if not d["bloggUrl1"]:
        del d["bloggUrl1"]
    tj_items.append({"id": t["slug"], "data": d})

# ---------------------------------------------------------------- PRISER
AVD_ORDER = ["sandvika", "ski", "kolbotn", "asenveien", "jessheim", "strommen", "rykkinn"]
AVD_NAME = {a["slug"]: a["kortnavn"] for a in A}
# (kategori, behandling, varighet_min, tjeneste_slug, hovedpris, [priser i AVD_ORDER])
P = [
 ("Re-fresh", "Re-Fresh Klassisk Hårklipp", 15, "herreklipp", False, [449, 399, 399, 399, None, None, None]),
 ("Re-fresh", "Re-Fresh Skjeggtrim", 15, "skjeggtrim", False, [429, 399, 399, 399, None, None, None]),
 ("Re-fresh", "Re-Fresh Skin-Fade Hårklipp", 30, "skin-fade", False, [625, 580, 580, 580, None, None, None]),
 ("Hårklipp", "Barneklipp klassisk (under 12 år)", 30, "barneklipp", True, [529, 499, 499, 489, 399, 429, 429]),
 ("Hårklipp", "Klassisk herreklipp", 30, "herreklipp", True, [639, 599, 599, 585, 449, 529, 539]),
 ("Hårklipp", "Klassisk klipp + voksing av nesehår", 30, "herreklipp", False, [788, 748, 748, 734, 598, 678, 688]),
 ("Hårklipp", "Skin fade", 45, "skin-fade", True, [829, 775, 775, 765, 599, 649, 699]),
 ("Hårklipp", "Pensjonistklipp", 30, "herreklipp", True, [500, 485, 485, 475, 399, 399, 450]),
 ("Hårklipp", "Midtskill/taper fade", 30, "skin-fade", False, [669, 625, 625, 625, 449, 549, 549]),
 ("Hårklipp", "Maskinklipp", 15, "herreklipp", False, [300, 300, 300, 300, 300, 329, 300]),
 ("Hårklipp", "Barneklipp skin fade (under 12 år)", 45, "barneklipp", True, [675, 650, 650, 625, 449, 499, 549]),
 ("Hårklipp", "Studentklipp skin fade (kun tirsdager)", 45, "skin-fade", False, [659, 675, 675, 675, 449, 549, 599]),
 ("Hårklipp", "Studentklipp (kun tirsdager)", 30, "herreklipp", False, [525, 525, 525, 499, 349, 449, 499]),
 ("Kombo", "Kombo I med voksing av nese", 60, "kombo", False, [1178, 1148, 1148, 1124, 948, 1038, 1078]),
 ("Kombo", "Kombo I: klassisk herreklipp og skjeggtrim eller knivbarbering", 60, "kombo", True, [1029, 999, 999, 975, 799, 889, 929]),
 ("Kombo", "Kombo II: skin fade og skjeggtrim eller knivbarbering", 60, "kombo", True, [1279, 1199, 1175, 1175, 899, 999, 1079]),
 ("Kombo", "Kombo III: hode- og skjeggbarbering med kniv", 45, "kombo", False, [899, 899, 899, 899, 699, 799, 799]),
 ("Skjegg", "Skjeggtrim", 28, "skjeggtrim", True, [579, 559, 549, 549, 399, 449, 479]),
 ("Skjegg", "Bart/mustasjetrim", 15, "skjeggtrim", False, [150, 100, 100, 100, 100, 189, 150]),
 ("Deluxe", "Hårklipp deluxe", 60, "herreklipp", False, [999, 999, 999, 999, 599, 899, 999]),
 ("Deluxe", "Barbering deluxe", 60, "barbering", False, [999, 899, 899, 899, 599, 799, 749]),
 ("Deluxe", "Skjeggtrim deluxe", 60, "skjeggtrim", False, [999, 899, 899, 899, 599, 799, 749]),
 ("Deluxe", "Kombo deluxe", 90, "kombo", False, [1799, 1599, 1599, 1599, 999, 1499, 1499]),
 ("Barbering", "Barbering av skjegget med kniv", 30, "barbering", True, [529, 499, 499, 499, 399, 449, 479]),
 ("Barbering", "Hodebarbering med kniv", 30, "barbering", False, [529, 499, 499, 499, 399, 399, 479]),
 ("Voksing", "Voksing pakke for nese, øre og ansikt", 30, None, False, [469]*7),
 ("Voksing", "Voksing av ansikt", 10, None, False, [175, 175, 175, 175, 175, 199, 175]),
 ("Voksing", "Voksing av nesehår", 10, None, False, [149]*7),
 ("Voksing", "Voksing av ørehår", 15, None, False, [175, 175, 175, 175, 175, 149, 175]),
 ("Voksing", "Voksing pakke", 45, None, False, [499, 499, 499, 499, 499, 497, 499]),
 ("Voksing", "Napping av hår med tråd", 15, None, False, [250, 250, 250, 250, 250, 200, 250]),
]
# Senior (Sandvika, Ski) i samme rekkefølge som P (indeks 0..24), voksing uendret
SENIOR = {
 0: (499, 449), 1: (450, 429), 2: (650, 599), 3: (579, 549), 4: (689, 649), 5: (838, 798), 6: (879, 825),
 7: (550, 529), 8: (699, 649), 9: (349, 349), 10: (725, 699), 11: (699, 715), 12: (579, 575),
 13: (1248, 1198), 14: (1099, 1049), 15: (1329, 1249), 16: (949, 949), 17: (650, 629), 18: (150, 100),
 19: (1099, 1099), 20: (1099, 999), 21: (1099, 999), 22: (1899, 1799), 23: (579, 599), 24: (579, 499),
}
def prisfmt(n):
    s = "%d" % n
    if n >= 1000:
        s = s[:-3] + " " + s[-3:]
    return s + " kr"

pris_items = []
seq = 0
for i, (kat, navn, var, tslug, hoved, priser) in enumerate(P):
    for j, aslug in enumerate(AVD_ORDER):
        pr = priser[j]
        if pr is None:
            continue
        seq += 1
        d = {"title": "%s, %s, Barber" % (navn, AVD_NAME[aslug]), "behandling": navn, "kategori": kat,
             "avdeling": aslug, "avdelingSlug": aslug, "niva": "Barber", "pris": pr, "pristekst": prisfmt(pr),
             "varighetMin": var, "hovedpris": hoved, "rekkefolge": i + 1, "publisert": True}
        if tslug:
            d["tjeneste"] = tslug
            d["tjenesteSlug"] = tslug
        pris_items.append({"data": d})
        if i in SENIOR and aslug in ("sandvika", "ski"):
            sp = SENIOR[i][0 if aslug == "sandvika" else 1]
            d2 = dict(d); d2["title"] = "%s, %s, Senior" % (navn, AVD_NAME[aslug]); d2["niva"] = "Senior"
            d2["pris"] = sp; d2["pristekst"] = prisfmt(sp)
            pris_items.append({"data": d2})

# ---------------------------------------------------------------- FAQ
faq_items = []
def faq(q, a, avd=None, tj=None, vis=(), r=0):
    d = {"title": q, "svar": "<p>%s</p>" % a, "visPa": list(vis), "rekkefolge": r, "publisert": True}
    if avd:
        d["avdeling"] = avd; d["avdelingSlug"] = avd
    if tj:
        d["tjeneste"] = tj; d["tjenesteSlug"] = tj
    faq_items.append({"data": d})

G = [
 ("Klipper dere bare menn?", "Nei. Alle behandlingene på menyen er for både menn og kvinner. Vi er spesialister på kort hår, skin fade og moderne herreklipp. Bestill på vanlig måte og velg behandlingen du vil ha.", ("forside", "tjeneste", "avdeling")),
 ("Må jeg bestille time, eller kan jeg stikke innom?", "Vi tar imot drop-in når vi har ledig, men anbefaler å bestille time på nett eller i appen. Da er du sikker på å få den barbereren og det tidspunktet du vil ha.", ("forside",)),
 ("Hvorfor kan prisen bli en annen enn den som står her?", "Prisene på siden er for nivå Barber. Prisen avhenger av barberens nivå: en Senior koster litt mer, en Lærling eller Junior litt mindre der avdelingen har det. Du velger barberer selv når du bestiller, og endelig pris ser du i onlinebookingen før du bekrefter.", ("forside", "tjeneste")),
 ("Hvor lang tid tar en klipp?", "Vi setter av 30 minutter til en klassisk herreklipp, 45 minutter til skin fade og 60 minutter til kombo med skjegg. Nøyaktig varighet står i bookingen når du velger behandling.", ("forside",)),
 ("Kan jeg ta med barnet mitt?", "Ja. Barneklipp er en av de vanligste behandlingene våre, og barbererne er vant med både tålmodige og utålmodige barn. Bestill gjerne time til dere begge etter hverandre hos samme barberer.", ("forside",)),
 ("Hvordan fungerer stempelkortet i appen?", "Du får ett stempel per Klassisk klipp, Skin fade, Skjeggtrim eller Kombo, på hvert sitt stempelkort. Hvert tiende stempel gir deg behandlingen gratis. Barbereren registrerer stempelet i salongen. Hvert stempel er gyldig i ett år.", ("forside", "app")),
 ("Hvordan betaler jeg?", "Du betaler i salongen etter behandlingen, med kort eller Vipps i kassen, i alle avdelinger. Gavekort gjelder som betalingsmiddel i kassen.", ("tjeneste", "avdeling")),
 ("Hva skjer hvis jeg må avbestille?", "Avbestill senest 24 timer før timen, i bookingen eller ved å ringe oss på 90 80 00 86.", ("tjeneste", "avdeling")),
 ("Velger jeg barberer selv?", "Ja. I bookingen ser du hvilke barberere som jobber i avdelingen, nivået deres og ledige tider. Velg den du vil ha, eller første ledige.", ("tjeneste", "avdeling")),
 ("Inngår hårvask i klippen?", "Ja. Hårvask inngår i klipp på alle nivåer, og du velger selv om du vil ha vask.", ("tjeneste",)),
 ("Gjelder gavekortet i alle avdelinger?", "Ja. Gavekort kjøpes på fixit.no/gavekort/1634, har valgfritt beløp, gjelder i alle avdelinger og innløses i kassen.", ("gavekort",)),
]
for i, (q, a, vis) in enumerate(G):
    faq(q, a, vis=vis, r=i + 1)
for a in A:
    for i, (q, ans) in enumerate(a["faq"]):
        faq(q, ans, avd=a["slug"], vis=("avdeling",), r=i + 1)
for t in T:
    for i, (q, ans) in enumerate(t["faq"]):
        faq(q, ans, tj=t["slug"], vis=("tjeneste",), r=i + 1)

# ---------------------------------------------------------------- sjekk: ingen tankestreker
alltxt = json.dumps([avd_items, tj_items, pris_items, faq_items], ensure_ascii=False)
assert "–" not in alltxt and "—" not in alltxt, "tankestrek funnet"

json.dump({"avdelinger": avd_items, "tjenester": tj_items, "priser": pris_items, "faq": faq_items,
           "naboer": {a["slug"]: a["naboer"] for a in A}},
          open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("avdelinger", len(avd_items), "tjenester", len(tj_items), "priser", len(pris_items), "faq", len(faq_items))
print("size", len(alltxt))

"""Google-sitater per avdeling (fra fakta-priser-anmeldelser.md, lest 23.10.2026, 5 stjerner, gjengitt ordrett
men uten tankestreker). Måned er regnet om fra "for N måneder siden" per 23.10.2026.

Byttes ut med nyere sitater ved behov. 'navn' er fornavn og forbokstav slik Google viser dem.
"""

ANMELDELSER = {
    "sandvika": [
        ("Har brukt Ibo på J&K Barber shop Sandvika i flere år. Kjempe dyktig i sitt fag med både saks og kniv. Vet at det alltid blir et bra resultat, så det er bare å lene seg godt tilbake i stolen og nyte 30-60 minutter hver gang jeg er der.",
         "Pål-Erik", "oktober 2026"),
        ("Veldig fornøyd med hvor raskt man kan få time og kvaliteten på jobben. Superhyggelige ansatte. Kan særlig anbefale Nicolae, men alle jeg har vært hos har vært flinke.",
         "Christian L.", "mai 2026"),
        ("Veldig hyggelig opplevelse og for første gang på over to måneder klarte jeg virkelig å slappe av. Klippen ble bra og skjegget ble fantastisk. Tusen takk.",
         "Espen Johannes F.", "mai 2026"),
    ],
    "ski": [
        ("Jeg kunne ikke vært mer fornøyd! En frisør som kombinerer ekstremt høy faglig dyktighet med en fantastisk serviceinnstilling. Her blir du møtt med kunnskap, presisjon og ekte interesse for å gi deg det beste resultatet, hver eneste gang.",
         "Per Kristoffer H.", "oktober 2025"),
        ("Jeg tok med barnet mitt hit for en skinfade-klipp, og vi er superfornøyde! Frisøren var utrolig dyktig og tok seg god tid for å sørge for at alt ble perfekt. Han var veldig hyggelig, skapte en trygg og rolig stemning, og spurte flere ganger underveis om vi var fornøyde. Resultatet ble kjempebra, og barnet mitt gikk smilende ut døra.",
         "Lillian T.", "oktober 2025"),
        ("God og effektiv klipp. En hyggelig opplevelser. Jeg er meget fornøyd med sluttresultatet.",
         "Jan K. B.", "november 2025"),
    ],
    "asenveien": [
        ("Alltid hyggelige og imøtekommende ansatte. Meget god service, og høy faglig kompetanse.",
         "Morten S.", "april 2026"),
        ("Nehat er supervennlig og gjør en fantastisk jobb. Anbefales på det sterkeste.",
         "B.", "oktober 2025"),
        ("Topp klipp og skjegg trimm. Og hyggelig samtale",
         "MrEasybite", "oktober 2025"),
    ],
    "kolbotn": [
        ("Saad er helt suveren, skjønner nøyaktig hva du vil ha, klipper håret ditt etter hvordan han skjønner at du vil style det. Aldri møtt en så flink frisør, ikke engang til 50% høyere pris. De andre frisørene her er også dyktige. 5 stjerner.",
         "Julian W.", "mai 2026"),
        ("Overraskende god atmosfære der til å være på et senter, også så fantastisk dyktig barber! Deilig å finne en barber i byen her som virkelig kan faget sitt, og leverer et godt stykke arbeid.",
         "Oliver F.", "oktober 2025"),
        ("Meget fornøyd kunde som ble klippet av barber Saad som virkelig kunne faget sitt og som var veldig blid og hyggelig. Håper han blir lenge på Kolbotn Torg.",
         "Roar A.", "juni 2026"),
    ],
    "jessheim": [
        ("Helt fenomenal barberer MOON, uten tvil en av de beste i Norge. Dette er rett og slett toppklasse. Presis fade, perfekte overganger og en ekstremt ren og stilfull finish. Frisøren har åpenbart full kontroll på håndverket sitt og legger stor stolthet i detaljene.",
         "Auris", "februar 2026"),
        ("Veldig flinke, vi er alltid fornøyd! Guttene mine på 9 år vil alltid tilbake hit.",
         "Sofie K.", "mars 2026"),
        ("Super service! De utfører førsteklasses klipp og yter god service, kaffe og litt attåt:)",
         "Gry Ånesland G.", "september 2026"),
    ],
    "strommen": [
        ("Klipte meg her hos Abdo og er utrolig fornøyd. God stemning med chill musikk og hyggelig ansatte. Alt dette til en meget god pris. 5/5 opplevelse.",
         "Daniel K.", "juli 2026"),
        ("Altid fornøyd med skjegget etter å ha vært her. Anbefaler for de med skjegg og som vil ha orden på det.",
         "Thomas H.", "juli 2026"),
        ("Fantastisk frisør. Kvaliteten på klippen min er fantastisk hver eneste gang. Anbefales på det sterkeste.",
         "Ryan M.", "september 2026"),
    ],
    "rykkinn": [
        ("Muha er en veldig veldig dyktig barber! Har fulgt med han fra Sandvika til Rykkinn nå og kan ikke annet enn å anbefale han!",
         "Bård O.", "november 2025"),
        ("Jeg anbefaler denne butikken på det sterkeste. De har veldig gode frisører som både kan klippe hår og er veldig hyggelig. Anbefales på det sterkeste!!",
         "Mohamed A.", "juli 2026"),
        ("Det var et veldig fint lokale, det var både ryddig og rent der. Jeg fikk en veldig fin klipp av en av frisørene der som både klippet meg meget bra og var veldig hygglig fra start til slutt. Anbefaler sterkt!!!!",
         "Foad A.", "november 2025"),
    ],
}

# Generelle sitater (uten navn på barberer) til forside og tjenestesider.
GENERELLE = [
    ("Veldig hyggelig opplevelse og for første gang på over to måneder klarte jeg virkelig å slappe av. Klippen ble bra og skjegget ble fantastisk. Tusen takk.",
     "Espen Johannes F., Sandvika Storsenter", "mai 2026"),
    ("Overraskende god atmosfære der til å være på et senter, også så fantastisk dyktig barber! Deilig å finne en barber i byen her som virkelig kan faget sitt, og leverer et godt stykke arbeid.",
     "Oliver F., Kolbotn Torg", "oktober 2025"),
    ("Fantastisk frisør. Kvaliteten på klippen min er fantastisk hver eneste gang. Anbefales på det sterkeste.",
     "Ryan M., Strømmen Storsenter", "september 2026"),
]


def for_avdeling(slug):
    return ANMELDELSER.get(slug) or GENERELLE

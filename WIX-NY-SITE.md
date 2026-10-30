# Teknisk logg: ny Wix Headless-site for J&K Barber Shop

Dato: 30. oktober 2026. Alt under er gjort via Wix REST API (ExecuteWixAPI i Wix MCP) som site-eier. Den gamle editor-siten (8e23fe36-d2f2-458b-a5b5-5f1576a2c6bc) er kun lest fra, ingenting er endret der. Ingenting er publisert på den nye siten: alle blogginnlegg ligger som UNPUBLISHED kladder, CMS-innhold er lesbart for besøkende (read ANYONE) fordi det er slik samlingene må være for at et headless-nettsted skal kunne lese dem, akkurat som på den gamle siten.

## 1. Site-ID-er og nøkler

| Hva | Verdi |
|---|---|
| Ny headless-site (metaSiteId / siteId) | `6063335a-f2d7-4e08-b813-4ff23ae700a0` |
| OAuth-app (clientId, offentlig) | `dbd18313-acf6-4a35-b6e3-11b05b4d0914` |
| Midlertidig host | https://headless-ojzxvuidssr-jkbarbershop-140c.wix-site-host.com/ |
| Dashbord | https://manage.wix.com/dashboard/6063335a-f2d7-4e08-b813-4ff23ae700a0/ |
| Gammel editor-site (kun lesing) | `8e23fe36-d2f2-458b-a5b5-5f1576a2c6bc` |
| Forfatter (site member, eier) | `8c3e53bc-3b17-4ccd-9d2d-c6c6301fedc6` (nickname på ny site: "Alan Hansen", på gammel: "J&K Barber Shop") |

Plan: Free. Det gir begrensninger i Wix Forms (se del 5).

## 2. Apper installert (steg 1)

Kall: `POST https://www.wixapis.com/apps-installer-service/v1/app-instance/install`, scope site, body `{ tenant: { tenantType: "SITE", id: siteId }, appInstance: { appDefId, enabled: true } }` (fra seed-cms.mjs / seed-forms.mjs).

| App | appDefId | appInstance.id | Avhengighet installert samtidig |
|---|---|---|---|
| Wix Blog (fantes fra provisjonering) | `14bcded7-0066-7c35-14d7-466cb3f09103` | (fra provisjonering) | |
| CMS / Wix Data | `e593b0bd-b783-45b8-97c2-873d42aacaf4` | `bec7567f-1776-4869-82eb-a4eb695a3ce1` | `1a711f05-2040-47df-a9f0-4f9cddb4c3c6` (instans `001b5f2d-df2c-45f0-95d2-e764c47ec75d`) |
| Wix Forms | `225dd912-7dea-4738-8688-4b8c6955ffc2` | `52f226b4-10f1-44a1-a234-e1586ec321c9` | `c435f412-d571-4c48-aada-ddf65a4a56b4` (instans `ab446435-24e5-4105-9492-ebaee1abdbfb`) |

FAQ-appen er ikke installert: FAQ-innholdet ligger i CMS-samlingen `Faq` slik som på den gamle siten, og templaten for cms/blog/forms krever ikke FAQ-appen. Fra provisjoneringen ligger det også Promote SEO, Wix Hotels og Wix Invoices på siten (ikke rørt; Hotels og Invoices kan avinstalleres i dashbordet).

GetSiteContext før installasjon viste bare Blog, Hotels, Invoices, Promote SEO. Install-kallene returnerte 200 med `installed: true` for begge apper og avhengighetene.

## 3. CMS-samlinger (steg 2)

Gjort ved å lese skjema og alle elementer fra den gamle siten (Get Data Collection, Query Data Items med `includeReferencedItems: ["naboer","tjenester"]`) og opprette identiske samlinger på den nye (Create Data Collection, Bulk Insert Data Items med `id` = gammel `_id`, Bulk Insert Data Item References). gen.py/data.json ble ikke kjørt på nytt: gen.py genererer bare JSON (har ingen siteId), og en direkte kopi fra den gamle siten gir garantert samme felt og innhold. Kopiene i cms-data/ er uendret.

Collection-ID-er er navnene (Wix Data bruker ID som nøkkel, ingen GUID): `Avdelinger`, `Tjenester`, `Priser`, `Faq` (visningsnavn FAQ). Tillatelser: read ANYONE, insert/update/remove ADMIN. displayField = title.

| Samling | Elementer gammel | Elementer ny | Verifisert |
|---|---|---|---|
| Tjenester | 6 | 6 | skin-fade -> avdelinger: alle 7 |
| Avdelinger | 7 | 7 | sandvika -> naboer rykkinn, asenveien; tjenester 6 |
| Priser | 258 | 258 | "Skin fade, Sandvika, Senior" 879 kr med oppslåtte referanser Sandvika Storsenter / Skin fade |
| Faq | 74 | 74 | 6 med visPa forside |

Element-ID-er er de samme som på gammel site (slug for Avdelinger og Tjenester, GUID for Priser og Faq). Felt: identiske med cms-logg.md (alle ikke-systemfelt kopiert med type og typeMetadata). Flerreferanser: `Avdelinger.naboer` (motfelt `naboAv`, selvreferanse) og `Avdelinger.tjenester` (motfelt `Tjenester.avdelinger`), 53 koblinger (11 naboer + 42 tjenester), alle persistert. Systemfeltet `link-avdelinger-title` (PAGE_LINK fra den gamle dynamiske siden) er ikke kopiert, det hører til editoren.

Org.nr.: søkt gjennom alle tekstfelt etter "923 441 794". Ingen treff, så ingen rettelse var nødvendig. Riktig nummer for footer og JSON-LD er 932 372 614.

Tomt som før (må fylles senere): lat, lng, placeId, gbpUrl, reviewsUrl, heroBilde, ogBilde, galleri på Avdelinger; ikon, bilde, forEtter på Tjenester. Samlingen Anmeldelser er ikke opprettet (var tom på gammel site og ikke i bestillingen).

Dashbord: https://manage.wix.com/dashboard/6063335a-f2d7-4e08-b813-4ff23ae700a0/wix-cms

## 4. Blogg (steg 3)

### Kategorier (opprettet med beskrivelser fra gammel site)

| Kategori | categoryId | slug |
|---|---|---|
| Guider | `44a07fa6-496b-4899-abd2-509934166426` | guider |
| Skjegg | `5a51bf08-3998-4727-8671-bb09a3b15a12` | skjegg |
| Hår og styling | `ca65403d-510a-4f3e-8f4f-41debc40ed22` | har-og-styling (Wix laget "hår-og-styling", rettet med PATCH /blog/v3/categories/{id}) |
| Produkter | `32d16a59-46f5-44d7-acba-05478852e208` | produkter |
| Barbershop-livet | `48b6f084-4c8c-4754-8363-7bdfafd41c29` | barbershop-livet |

### Forfatter

Oppskrift fra seed-blog.mjs: `GET /members/v1/members?fieldsets=PUBLIC&paging.limit=1`, bruk `members[0].id`. På den nye siten er eneste medlem eieren, `8c3e53bc-3b17-4ccd-9d2d-c6c6301fedc6`, samme member-ID som forfatteren på den gamle siten. Alle 35 kladder har denne som memberId. Nickname på den nye siten er "Alan Hansen" (på gammel "J&K Barber Shop"); endres i dashbordet under Blog > Writers eller Members hvis bylinen skal være "J&K Barber Shop". Ingen nytt medlem er opprettet.

### De 15 migrerte innleggene (publisert på gammel site, kladd på ny)

Opprettet med `POST /blog/v3/draft-posts` body `{ draftPost: {...}, publish: false }`: title (uendret), memberId, language "no" (fire var "en"), seoSlug (ny slug), excerpt, richContent (hentet med fieldsets RICH_CONTENT fra Query Posts), categoryIds, seoData.tags der den gamle hadde SEO (2 av 15), media `{ displayed: true, custom: true, wixMedia: { image: { id, url, width, height } } }` med den gamle wixstatic-URL-en. Alle 15 fikk forsidebildet med (verifisert via GET med fieldsets).

| # | draftPostId (ny) | Ny slug | Gammel slug | Kategori |
|---|---|---|---|---|
| 1 | `5a48a56a-eeab-40bb-a326-a4fb84d83885` | pan-drwal-skjegg-og-kropp | pan-drwal-polsk-barbershop-luksus-for-skjegg-og-kropp | Produkter |
| 2 | `2cc4b4a9-e139-4518-8fba-51c4b96fd09c` | flass-davines-harprodukter | hvordan-behandle-flass-med-davines-hårprodukter | Produkter |
| 3 | `739a8bad-14d6-47bd-8ba9-9f3ec61f8dc5` | hvor-ofte-bor-jeg-besoke-frisoren-min | hvor-ofte-bør-jeg-besøke-frisøren-min | Guider |
| 4 | `81581b36-c863-41e2-af5d-0d4e1c3be24c` | fordelene-med-a-ga-til-barberer | hva-er-fordelene-med-å-gå-til-en-barberer | Barbershop-livet |
| 5 | `b7c0ccee-55d1-44af-ad5d-fa07c3d74b6f` | ta-vare-pa-skjegget | hvordan-ta-godt-vare-på-skjegget | Skjegg |
| 6 | `7c6e51e9-b92a-405d-ab60-1a9353d00cc0` | pleietips-for-alle-hartyper | tips-for-alle-hårtyper-pleie | Hår og styling |
| 7 | `05b0e648-6501-4ed3-b083-2d5fadedc54d` | flass-i-skjegget | hvorfor-vises-flass-på-skjegget-mitt | Skjegg |
| 8 | `d5283fcd-fe8d-46c8-a870-35a30f62255d` | reuzel-harvoks-og-pomade | reuzel-det-beste-alternativet-for-hårvoks | Produkter |
| 9 | `e4391e15-c858-428d-956f-38f1ea73312d` | skjeggolje-slik-bruker-du-den | skjeggolje-hvordan-bruke-det | Skjegg |
| 10 | `f50219ac-02de-4069-bb56-5e56c3a37137` | slik-foner-du-skjegget | hvordan-føne-skjegget | Skjegg |
| 11 | `7d43ccfd-d017-42c9-8113-819225592775` | slik-barberer-du-deg-hjemme | slik-barberer-du-deg-lynraskt | Barbershop-livet |
| 12 | `732455d0-6510-47b4-8886-b748eee1245e` | mer-skjeggvekst | kan-jeg-få-mer-skjeggvekst | Skjegg |
| 13 | `e602c35b-8f66-45a9-addf-016e2a11f7a7` | harstyling-del-2-teknikker | alt-om-hårstyling-del-2-smarte-teknikker | Hår og styling |
| 14 | `5906cae1-ae54-4140-8506-3e848fb6078b` | harstyling-del-1-grunnleggende | alt-om-hårstyling-del-1 | Hår og styling |
| 15 | `20f64ebc-acea-477d-8123-7cd10c7b3dd1` | mykt-skjegg-pa-1-2-3 | mykt-skjegg-på-1-2-3 | Skjegg |

Avvik: Innholdsplanen del 7.1 gir #3 slug `hvor-ofte-bor-menn-klippe-seg`, men den slugen er brukt av den nye artikkelen (kladd 04 under), og planen sier at det gamle innlegget erstattes av den nye. For å unngå kollisjon fikk det gamle innlegget slug `hvor-ofte-bor-jeg-besoke-frisoren-min`. Anbefaling: ikke publiser #3, la den nye artikkelen ta over, og legg 301 fra gammel URL til /post/hvor-ofte-bor-menn-klippe-seg. Titlene er beholdt som de var (oppgaven sa samme tittel); de normaliserte titlene i del 7.1 (uten versaler, kortere #2) må settes manuelt eller i en senere API-runde.

### De 20 nye artiklene (kladd på gammel site, kladd på ny)

Hentet med `GET /blog/v3/draft-posts?status=UNPUBLISHED&fieldsets=RICH_CONTENT&fieldsets=URL`, opprettet med samme kall som over (ingen forsidebilder fantes). Alle har seoData (title + meta description), excerpt, kategori og language "no".

| # | draftPostId (ny) | Slug | Kategori |
|---|---|---|---|
| 01 | `6c9e700b-88f9-48c0-8c63-a1f9201ed41f` | skin-fade-taper-fade-forskjellen | Guider |
| 02 | `140d61a4-dc0c-4b3d-b5ff-632ae209c987` | hva-koster-herreklipp-og-skin-fade | Guider |
| 03 | `66f6f3eb-0c35-46cd-8ce4-fa9ee6a652e3` | barneklipp-forste-gang-tips | Guider |
| 04 | `4e358cf3-d606-4a11-a861-8c724cb0580b` | hvor-ofte-bor-menn-klippe-seg | Guider |
| 05 | `e3037db9-3277-4035-87e8-b76ab568f422` | slik-styler-du-skjegget | Guider |
| 06 | `e20547c0-d94f-4321-860e-c519d1102b41` | knivbarbering-slik-foregar-det | Guider |
| 07 | `5ed4b725-7af0-4273-b5cd-718bd292f477` | barbershop-ski | Barbershop-livet |
| 08 | `e22694f0-b89e-4ff5-8fc2-066953e3daa8` | frisor-kolbotn-barbershop | Barbershop-livet |
| 09 | `a3e86a1c-9c7e-42d9-a79a-c4e5988b0a05` | barbershop-sandvika-storsenter | Barbershop-livet |
| 10 | `d63acd25-784a-462c-900c-0b47e9734474` | barbershop-jessheim | Barbershop-livet |
| 11 | `c4683a61-83d0-4810-975a-7d9306fed13e` | barbershop-strommen-storsenter | Barbershop-livet |
| 12 | `698dc3e3-9c17-485f-a647-c2577ff0ea37` | frisor-rykkinn-senter | Barbershop-livet |
| 13 | `706b901d-f325-402c-bac0-f9ed8f73cf92` | herrefrisor-eller-barber-forskjellen | Guider |
| 14 | `5503dd02-2437-455c-94d4-46cc758542a3` | herreklipp-for-kvinner | Guider |
| 15 | `289d92c8-27c6-4664-a536-090f8d59bc4d` | skjeggtrim-etter-ansiktsform | Skjegg |
| 16 | `6420d847-8bc4-4524-aacf-71d0f19fab37` | hodebarbering-guide | Guider |
| 17 | `dfb8e484-3915-4c5d-95e3-35edfe1a5f51` | pomade-voks-leire-saltspray | Produkter |
| 18 | `bf41500b-ce60-4631-b2c2-cbae2ac8f146` | drop-in-eller-bestilt-time | Barbershop-livet |
| 19 | `e338dd6f-7be6-42e5-85ba-1f9d93111ef4` | stempelkort-app-gratis-klipp | Barbershop-livet |
| 20 | `1312745e-e2e8-4ce2-b194-017b4016eed0` | gavekort-barber | Barbershop-livet |

Verifisering: List Draft Posts på ny site gir 35 kladder, alle UNPUBLISHED. richContent sammenlignet i bytes mot kilden: de 20 nye er identiske, de 15 gamle er 46 bytes kortere hver (Ricos-metadata som Wix setter på nytt, ikke innhold). Interne lenker i innleggene peker fortsatt på /post/<gammel slug> og /blogg/..., og må gjennomgås før publisering (eller håndteres med redirects).

Dashbord: https://manage.wix.com/dashboard/6063335a-f2d7-4e08-b813-4ff23ae700a0/blog/posts (fanen Drafts).

## 5. Skjemaer (steg 4)

### Slik fungerer Wix Forms på headless (dokumentert, ikke antatt)

Kilde: headless-templates/forms/INSTRUCTIONS.md, seed/seed-forms.mjs, rest/forms.ts og rest/submissions.ts.

- Et skjema er et **Form-skjema (Form Schemas v4)** i namespace `wix.form_app.form`. Det kan opprettes i dashbordet (Forms & Submissions) eller via API `POST /form-schema-service/v4/forms` med `{ form: { name, namespace, formFields, steps, submitSettings, ... } }`. Det er det seed-skriptet gjør, og det er gjort her.
- Et statisk nettsted leser skjemaet som besøkende: `GET /form-schema-service/v4/forms/{formId}` med visitor-token (returnerer 200 til anonym besøkende selv om docs lister eier-scope; verifisert her, se del 7).
- Innsending går direkte fra nettleseren til `POST /form-submission-service/v4/submissions` med visitor-token. Ingen backend, ingen API-nøkkel, ingen elevate. Besøkende kan ikke lese innsendinger tilbake (403), svaret på POST er bekreftelsen.
- Filopplasting: `POST /form-submission-service/v4/submissions/media-upload-url { formId, filename, mimeType }` -> `{ uploadUrl }`, så PUT av filen, og `[{ fileId, displayName, fileType, url }]` som feltverdi. Krever betalt plan (se under).
- Innsendinger havner i dashbordet under Forms & Submissions per skjema, og felt med contactMapping (e-post, telefon, firma) oppretter/oppdaterer kontakt i Wix Kontakter.

### Opprettede skjemaer

Free-plan-grenser lest fra `GET /form-app-service/v4/restrictions`: maks 4 skjemaer, 10 inputfelt per skjema, 3 steg, 3 regler, ingen filopplasting. Derfor er 4 av 5 skjemaer opprettet. Alle har requiredIndicator ASTERISK, takkemelding (THANK_YOU_MESSAGE) i stedet for redirect til /takk-side (endelig domene er ikke kjent, og et statisk nettsted kan selv navigere videre når innsendingen er bekreftet; redirect kan settes i dashbordet senere). Telefonfelt har standard landkode NO. Alle skjemaer lest tilbake etter opprettelse: ingen felt degradert.

**Kontakt** formId `46d9f072-fc1c-4aa0-8e3e-ef43548f3c1d`

| Felt | target | type | påkrevd |
|---|---|---|---|
| Navn | navn_6w8yvk | TEXT_INPUT | ja |
| E-post | e_post_sstfv7 | TEXT_INPUT (EMAIL, kontaktfelt) | ja |
| Telefon | telefon_psecma | PHONE_INPUT (kontaktfelt) | nei |
| Avdeling | avdeling_r5b10m | DROPDOWN (7 avdelinger + Hovedkontor) | ja |
| Melding | melding_rjikoj | TEXT_AREA | ja |
| Samtykke | jeg_samtykker_til_at_j_k_barber_shop_lag_2vm5q7 | CHECKBOX (må krysses av) | ja |

**Jobbsøknad** formId `4db6b92d-98f9-4964-bdf8-c3a7ec589c15`

| Felt | target | type | påkrevd |
|---|---|---|---|
| Navn | navn_7pb7rx | TEXT_INPUT | ja |
| E-post | e_post_7w4sea | EMAIL | ja |
| Telefon | telefon_tzs0xj | PHONE_INPUT | ja |
| Ønsket avdeling | onsket_avdeling_h1rtid | CHECKBOX_GROUP (7 avdelinger) | ja |
| Erfaring som barberer eller frisør | erfaring_som_barberer_eller_frisor_pjh5wz | DROPDOWN (Under 1 år / 1 til 3 år / 3 til 5 år / Over 5 år) | ja |
| Har du fagbrev? | har_du_fagbrev_mpbucg | RADIO_GROUP (Ja / Nei / Under utdanning) | ja |
| Fortell kort om deg selv | fortell_kort_om_deg_selv_82l8ni | TEXT_AREA | ja |
| Lenke til CV eller portefølje (valgfritt) | lenke_til_cv_eller_portefolje_valgfritt_hy5u1q | URL | nei |
| Samtykke | jeg_samtykker_til_at_j_k_barber_shop_lag_uj9xfs | CHECKBOX | ja |

CV-opplasting (fil, PDF/JPG, maks 2) er erstattet av URL-felt fordi FILE_UPLOAD krever betalt plan. Når siten oppgraderes: legg til feltet "CV og attester" (File upload, maks 2 filer, PDF/JPG) i dashbordet, og fjern URL-feltet om ønskelig.

**Franchise** formId `af4ebbfe-481d-4a49-bbeb-c86c9fd70e6d`

| Felt | target | type | påkrevd |
|---|---|---|---|
| Navn | navn_24rehu | TEXT_INPUT | ja |
| Firma | firma_6y29cs | TEXT_INPUT (kontaktfelt COMPANY) | nei |
| Telefon | telefon_o5lnov | PHONE_INPUT | ja |
| E-post | e_post_q52elm | EMAIL | ja |
| Ønsket område | onsket_omrade_4o5eqs | TEXT_INPUT | ja |
| Erfaring fra bransjen | erfaring_fra_bransjen_27ejxk | TEXT_AREA | ja |
| Melding | melding_1b49o1 | TEXT_AREA | nei |
| Samtykke | jeg_samtykker_til_at_j_k_barber_shop_lag_n7xkp3 | CHECKBOX | ja |

**Hjemmebarbering** formId `28632583-0742-4e13-9a61-37a609717a9a`

| Felt | target | type | påkrevd |
|---|---|---|---|
| Navn | navn_ow9fud | TEXT_INPUT | ja |
| Telefon | telefon_zr4yg3 | PHONE_INPUT | ja |
| E-post | e_post_jyhm5a | EMAIL | nei |
| Adresse eller område | adresse_eller_omrade_kj3tzh | TEXT_INPUT | ja |
| Ønsket dato | onsket_dato_lpuejr | DATE_PICKER (minimum i dag) | ja |
| Tjeneste | tjeneste_3erwog | DROPDOWN (Klassisk herreklipp / Skin fade / Skjeggtrim / Knivbarbering / Kombo: klipp og skjegg / Barneklipp / Annet) | ja |
| Melding | melding_1196g3 | TEXT_AREA | nei |

**Tilbakemelding: IKKE opprettet** (skjema nr. 5 går over free-plan-grensen på 4). Når siten er oppgradert, opprett i dashbordet (Forms & Submissions > Create form) eller be om en ny API-runde med denne feltlisten: Avdeling (nedtrekk, 7 avdelinger; forhåndsvelges fra ?avd= i nettstedets kode), Vurdering 1 til 5 (Rating), Hva kan bli bedre (lang tekst), Navn (valgfritt), Telefon (valgfritt). Alternativ uten oppgradering: lagre tilbakemeldinger i en CMS-samling med insert ANYONE, men da uten spamfilter og kontaktkobling.

Hva Alan må gjøre i dashbordet uansett: (a) Automations: trigger "Form submitted" per skjema, handling "Send email" til post@j-kbarber.no; (b) hvitliste avsendere fra wixforms.com / crm.wix.com / automations.ascendbywix.com i Outlook; (c) eventuelt reCAPTCHA på Jobbsøknad og Franchise (Forms settings > Spam protection); (d) sletterutine for jobbsøknader etter 6 måneder.

Dashbord: https://manage.wix.com/dashboard/6063335a-f2d7-4e08-b813-4ff23ae700a0/wix-forms og `.../wix-forms/form/{formId}/submissions`.

## 6. Site-egenskaper (steg 5)

Satt via Site Properties API og lest tilbake (versjon 21):

| Egenskap | Verdi | Kall |
|---|---|---|
| language | no | `PATCH /site-properties/v4/properties { properties: { language: "no" }, fields: { paths: ["language"] } }` |
| locale | languageCode no, country NO | `PATCH /site-properties/v4/properties { properties: { locale: { languageCode: "no", country: "NO" } }, fields: { paths: ["locale"] } }` |
| paymentCurrency / timeZone | NOK / Europe/Oslo | `POST /site-properties/v4/properties/business-region` |
| siteDisplayName / businessName | J&K Barber Shop | `POST /site-properties/v4/properties/business-profile` |
| email / phone | post@j-kbarber.no / +4790800086 | `POST /site-properties/v4/properties/business-contact` |
| address | Åsenveien 3, 1400 Ski, NO (street Åsenveien, streetNumber 3, zip 1400, city Ski, isPhysical true) | samme kall |

Merk: Wix bruker språkkoden "no" (ikke "nb"); "nb" finnes ikke som sitespråk i Wix. Site-navnet i ListWixSites var "J&K Barber Shop ny" og er nå "J&K Barber Shop" (siteDisplayName).

## 7. Slik leser et statisk nettsted siten som besøkende

### Visitor-token fra appId (fra headless-templates/shared/rest/client.ts)

clientId er den offentlige OAuth-app-ID-en `dbd18313-acf6-4a35-b6e3-11b05b4d0914`. Den er ikke hemmelig og kan ligge i sidekoden. Token mintes én gang per besøkende, lagres i localStorage og fornyes; aldri per kall.

```js
const WIX_CLIENT_ID = "dbd18313-acf6-4a35-b6e3-11b05b4d0914";
const WIX_API_BASE = "https://www.wixapis.com";
const TOKEN_URL = `${WIX_API_BASE}/oauth2/token`;
const STORAGE_KEY = `wix-visitor-${WIX_CLIENT_ID}`;

// grantType "anonymous" minter en besøkende; "refresh_token" fornyer og beholder identiteten.
async function mintTokens(body, role = "visitor") {
  const res = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ clientId: WIX_CLIENT_ID, ...body }),
  });
  if (!res.ok) throw new Error(`Wix auth failed (${res.status}).`);
  const data = await res.json(); // { access_token, refresh_token, expires_in (14400 s), token_type: "Bearer" }
  return { accessToken: data.access_token, refreshToken: data.refresh_token, expiresAt: Date.now() + data.expires_in * 1000, role };
}

let pending = null;
async function accessToken() {
  let t = null;
  try { t = JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch {}
  if (t && t.expiresAt - 60_000 > Date.now()) return t.accessToken;
  pending ??= (async () => {
    let fresh;
    if (t?.refreshToken) {
      try { fresh = await mintTokens({ grantType: "refresh_token", refreshToken: t.refreshToken }, t.role ?? "visitor"); } catch {}
    }
    fresh ??= await mintTokens({ grantType: "anonymous" });
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(fresh)); } catch {}
    return fresh.accessToken;
  })().finally(() => { pending = null; });
  return pending;
}

// Alle kall: Authorization-headeren bærer det rå access_token (uten "Bearer "), Content-Type application/json.
async function wixRequest(path, { method = "POST", body, query } = {}) {
  const url = new URL(path, WIX_API_BASE);
  for (const [k, v] of Object.entries(query ?? {})) for (const item of Array.isArray(v) ? v : [v]) url.searchParams.append(k, String(item));
  const res = await fetch(url, { method, headers: { Authorization: await accessToken(), "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body) });
  if (!res.ok) throw new Error(`${method} ${url.pathname} failed (${res.status}).`);
  return res.status === 204 ? null : res.json();
}
```

### Publiserte blogginnlegg (fra blog/rest/posts.ts og posts-core.ts)

Bare publiserte innlegg kommer tilbake til en besøkende (kladder gir 403 PermissionDenied på /draft-posts, verifisert).

Feed, første side (pinned først, så nyeste):
```
POST https://www.wixapis.com/blog/v3/posts/query
{ "fieldsets": ["METRICS"],
  "query": { "sort": [{ "fieldName": "pinned", "order": "DESC" }, { "fieldName": "firstPublishedDate", "order": "DESC" }],
             "cursorPaging": { "limit": 20 } } }
```
Filtrert på kategori: legg til `"filter": { "categoryIds": { "$hasSome": ["<categoryId>"] } }`. Neste side: bare `{ "fieldsets": ["METRICS"], "query": { "cursorPaging": { "limit": 20, "cursor": "<pagingMetadata.cursors.next>" } } }`.

Ett innlegg med brødtekst og SEO:
```
GET https://www.wixapis.com/blog/v3/posts/slugs/{slug}?fieldsets=RICH_CONTENT&fieldsets=CONTENT_TEXT&fieldsets=SEO&fieldsets=REFERENCE_ID&fieldsets=INTERNAL_ID
```
Kategorier: `POST /blog/v3/categories/query { "query": { "paging": { "limit": 100 } } }`. Forfatter: `GET /members/v1/members/{memberId}?fieldsets=PUBLIC` (batch i authors.ts). Forsidebilde: `media.wixMedia.image.url` (wixstatic), alt-tekst `media.altText`; `media.displayed === false` betyr skjult cover.

Besøkende-sjekk gjort 30. okt: posts/query 200 med 0 innlegg (alt er kladd), categories/query 200 med 5 kategorier.

### CMS (fra cms/rest/items.ts)

```
POST https://www.wixapis.com/wix-data/v2/items/query
{ "dataCollectionId": "Avdelinger",
  "query": { "filter": { "publisert": true }, "sort": [{ "fieldName": "rekkefolge", "order": "ASC" }], "paging": { "limit": 10, "offset": 0 } },
  "includeReferencedItems": ["tjenester"] }
```
Svar: `dataItems[].data` (flat, `_id` er ID; RICH_TEXT er HTML-streng; ADDRESS er objekt). Verifisert som besøkende: 6 avdelinger med 6 tjenester hver (Rykkinn er publisert = false og filtreres bort). Priser for en avdelingsside: filter `{ "avdelingSlug": "ski", "hovedpris": true, "niva": "Barber" }` gir de 9 hovedprisene. FAQ på forsiden: `POST /wix-data/v2/items/count { "dataCollectionId": "Faq", "filter": { "visPa": { "$hasSome": ["forside"] } } }` gir 6. Ett element på slug: filter `{ "slug": { "$eq": "sandvika" } }`, limit 1.

### Skjema: lese og sende inn (fra forms/rest/forms.ts og submissions.ts)

Lese skjemaet (for å tegne feltene fra `formFields[].inputOptions.target` og komponenttypen):
```
GET https://www.wixapis.com/form-schema-service/v4/forms/46d9f072-fc1c-4aa0-8e3e-ef43548f3c1d
```
Verifisert som besøkende: 200, 6 inputfelt.

Sende inn (nøklene er feltenes `target`, verdiene i feltets form: tekst som streng, CHECKBOX som boolean, CHECKBOX_GROUP som array av valgte verdier, DATE som "YYYY-MM-DD", PHONE som E.164-streng):
```
POST https://www.wixapis.com/form-submission-service/v4/submissions
{ "submission": {
    "formId": "46d9f072-fc1c-4aa0-8e3e-ef43548f3c1d",
    "submissions": {
      "navn_6w8yvk": "Ola Nordmann",
      "e_post_sstfv7": "ola@example.com",
      "telefon_psecma": "+4790000000",
      "avdeling_r5b10m": "Ski Storsenter",
      "melding_rjikoj": "Hei, ...",
      "jeg_samtykker_til_at_j_k_barber_shop_lag_2vm5q7": true
    } },
  "captchaToken": "<bare hvis reCAPTCHA er slått på>" }
```
Svar: `{ "submission": { "id", "status": "CONFIRMED" | "PENDING" | "PAYMENT_WAITING", ... } }`, alle tre betyr at innsendingen finnes. Feil 400 bærer `details.validationError.fieldViolations[]` (per felt) eller `details.applicationError.code` (f.eks. INVALID_CAPTCHA). Ingen testinnsending er sendt (det ville laget en ekte innsending og kontakt).

Takkemeldingen ligger i skjemaet: `submitSettings.thankYouMessageOptions.richContent` (Ricos), les den fra GET-svaret og vis den etter bekreftet innsending.

## 8. Gjenstår / feilet

- Ingen API-kall feilet til slutt. To mellomsteg ble rettet underveis: `includeReferencedItems` er en liste med strenger (ikke objekter), og Bulk Insert krever `id` på elementet når `data._id` er satt.
- Skjema 5 (Tilbakemelding) og filopplasting i Jobbsøknad venter på betalt Wix-plan (free: maks 4 skjemaer, ingen filfelt). Domene j-kbarber.no krever uansett premium.
- Blogg: alle 35 er kladd, ingen publisert. Før publisering: gjennomgå interne lenker (/post/<gammel slug>, /blogg/...), de normaliserte titlene fra innholdsplan 7.1, forsidebilder på de 20 nye, og beslutning om #3 (gammelt "hvor ofte"-innlegg). Bylinen viser "Alan Hansen" til nickname endres.
- CMS: bildefelt, lat/lng/placeId/gbpUrl/reviewsUrl er tomme. Anmeldelser- og Merker-samling er ikke opprettet.
- Redirects fra gamle blogg-URL-er (gammel site) til nye slugs må lages når domenet flyttes.
- Apper fra provisjonering som ikke trengs (Wix Hotels, Wix Invoices) kan avinstalleres i dashbordet; ikke gjort.
- Sidene (HTML/JS som leser dette) er ikke laget i denne runden; design-utkast ligger i /home/claude/jkbarber-site/design/.

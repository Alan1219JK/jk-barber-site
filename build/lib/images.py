"""Bildetabell: avtalt filnavn -> offentlig URL.

Fotografens bilder byttes inn senere ved å legge inn / erstatte én URL per filnavn her.
Filnavn som mangler i tabellen gir en mørk plassholder (class "ph") med motiv og filnavn,
slik at det er lett å se hva som skal fotograferes.

Wix-bilder skaleres med URL-parametre (fill = beskjær til format):
  https://static.wixstatic.com/media/<id>/v1/fill/w_1600,h_900,al_c,q_80/<navn>.jpg
"""
from .util import e

WIX = "https://static.wixstatic.com/media/"

# Kun bilder med avklarte rettigheter (fasade Ski, interiør 2025, 2021-fotograferingen, Sandvika-serien 2026, logoer).
# IKKE "Barbers Working"/"Barber's Portraits" (a22503_...) og ikke Strømmen-pressebildene.
IMAGES = {
    # Felles
    "jk-barber-felles-hero-klipp-i-stol.jpg": WIX + "8c3e53_bd6015b9fe3847fc90c0d97cc8c5c42c~mv2.jpg",      # _I7A0181, 2021, 2880x3600
    "jk-barber-felles-barberer-med-kunde.jpg": WIX + "8c3e53_eaf508b57dff413995399ce7f746555c~mv2.jpg",    # _I7A0467, 2021, 2880x3600
    "jk-barber-felles-interior-2025.jpg": WIX + "8c3e53_449bfc76e3c742c8a3f6d45496c59919~mv2.jpg",          # mai 2025, 2522x1816
    "jk-barber-felles-interior-resepsjon.jpg": WIX + "8c3e53_91542e8112ac485b9eded3c13faf2c3f~mv2.jpg",     # jkbs-0211, 2487x1419
    "jk-barber-felles-fasade-skilt-2025.jpg": WIX + "8c3e53_e7158325fc814110aa96967b41c593d3~mv2.jpg",      # juli 2025, 1600x1037
    "jk-barber-felles-skjegg.jpg": WIX + "8c3e53_d574e17736b24f5bbf20bc2b48b2a822~mv2.jpg",                 # 2021, 1024x1536
    "jk-barber-felles-barbering.jpg": WIX + "8c3e53_bffd676236bd44e7acbb6849a196e253~mv2.jpg",              # 2021, 1024x1536
    "jk-barber-felles-fixit-banner.jpg": WIX + "8c3e53_9c7ef26e499f4c5da4410a81b8e775ce~mv2.jpg",           # 2100x990
    # Sandvika (serie april 2026)
    "jk-barber-sandvika-interior.jpg": WIX + "8c3e53_66817c4b94554af1b3dc58a17afc7edb~mv2.jpg",             # 1600x956
    "jk-barber-sandvika-skin-fade.jpg": WIX + "8c3e53_35651d6ac6c04a608f0b582780a40ead~mv2.jpg",            # 1080x1350
    "jk-barber-sandvika-skjeggtrim.jpg": WIX + "8c3e53_74cdfcd72b5a496ea5b7d158d176e345~mv2.jpg",           # 827x1036
    "jk-barber-sandvika-herreklipp-slickback.jpg": WIX + "8c3e53_2462b96b436f4074882833f601f42113~mv2.jpg", # 1075x1076
    "jk-barber-sandvika-herreklipp-teksturert.jpg": WIX + "8c3e53_c8bce34b7f93434facd64222b3ecc2d1~mv2.jpg",# 1080x1350
    "jk-barber-sandvika-taper-fade.jpg": WIX + "8c3e53_4dcff5aa80cb4e4ba9425f4a8211486e~mv2.jpg",           # 815x816
    "jk-barber-sandvika-barbering.jpg": WIX + "8c3e53_bd05b237b40249ac907139dc5c6c20eb~mv2.jpg",            # 1080x1350
    # Ski
    "jk-barber-ski-fasade.jpg": WIX + "8c3e53_dd49f700ba4f40cf94454a7e8094f56e~mv2.jpg",                    # 4032x1979
    "jk-barber-ski-interior.jpg": WIX + "8c3e53_aaeeebbbb8644bb2a198ce73f2eed080~mv2.jpg",                  # 1486x976
    # Åsenveien
    "jk-barber-asenveien-fasade.jpg": WIX + "8c3e53_0abc92810dec4bf9ac5f51bb161f7df7~mv2.jpg",              # 1024x575
    "jk-barber-asenveien-interior.jpg": WIX + "8c3e53_96b1ed57b12f48848b9cea7b80b34531~mv2.jpg",            # 1024x683
    # Kolbotn
    "jk-barber-kolbotn-interior.jpg": WIX + "8c3e53_1a093c995baf4fff8492ca1edc1b8fb3~mv2.jpg",              # 1600x1067
    # Rykkinn
    "jk-barber-rykkinn-fasade.jpg": WIX + "8c3e53_b7c6cab7fa46464889b58b3faa4bd73d~mv2.jpeg",               # 1200x700
    # Produkter
    "jk-barber-felles-produkter-davines.jpg": WIX + "8c3e53_7fe1a96e151c471bb300dd60a8c2d4a7~mv2.png",      # 959x639
    "jk-barber-felles-produkter-harvoks.jpg": WIX + "8c3e53_4c6333ca51c544dc8e998bfa21ecbf2a~mv2.jpg",      # 720x496
}

LOGO = "/assets/logo-messing.png"
# Kvadratisk logo for schema (svart på transparent, 2270x2041, på Wix). Byttes til 512x512-variant senere.
LOGO_SCHEMA = WIX + "8c3e53_3602ff764f2b4cbfa90bf7e01b8ed369~mv2.png"


def url(name: str, w: int = 0, h: int = 0, q: int = 80) -> str | None:
    """Offentlig URL for et avtalt filnavn, skalert hvis det er et Wix-bilde."""
    u = IMAGES.get(name)
    if not u:
        return None
    if u.startswith(WIX) and w:
        base = name.rsplit(".", 1)[0]
        if h:
            return f"{u}/v1/fill/w_{w},h_{h},al_c,q_{q}/{base}.jpg"
        return f"{u}/v1/fit/w_{w},h_{w},q_{q}/{base}.jpg"
    return u


def has(name: str) -> bool:
    return name in IMAGES


def picture(name: str, alt: str, w: int, h: int, *, cls: str = "", lazy: bool = True,
            motiv: str = "", style: str = "") -> str:
    """<img> hvis bildet finnes, ellers plassholder-div med motiv og filnavn."""
    src = url(name, w, h)
    if src:
        attrs = [f'src="{e(src)}"', f'alt="{e(alt)}"', f'width="{w}"', f'height="{h}"']
        if lazy:
            attrs.append('loading="lazy"')
            attrs.append('decoding="async"')
        else:
            attrs.append('fetchpriority="high"')
        if cls:
            attrs.append(f'class="{e(cls)}"')
        if style:
            attrs.append(f'style="{e(style)}"')
        return f"<img {' '.join(attrs)}>"
    return ph(motiv or alt, name, cls=cls, style=style)


def ph(motiv: str, filnavn: str = "", cls: str = "", style: str = "") -> str:
    """Mørk plassholder for bilde som mangler."""
    txt = motiv
    if filnavn:
        txt += f" ({filnavn})"
    c = "ph" + (f" {cls}" if cls else "")
    st = f' style="{e(style)}"' if style else ""
    return f'<div class="{c}"{st} role="img" aria-label="{e(motiv)}"><span>{e(txt)}</span></div>'

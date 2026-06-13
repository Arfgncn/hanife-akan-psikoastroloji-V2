import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .core_utils import SIGNS, ELEMENT, MODALITY, sign_from_longitude, format_degree

# Chiron, bazı sistemlerde ek ephemeris dosyası (seas_18.se1 vb.) ister.
# Dosya yoksa bütün haritayı sahte/yaklaşık veriye düşürmemek için Chiron şimdilik kapalıdır.
SYMBOL = {
    "Güneş": "☉",
    "Ay": "☽",
    "Merkür": "☿",
    "Venüs": "♀",
    "Mars": "♂",
    "Jüpiter": "♃",
    "Satürn": "♄",
    "Uranüs": "♅",
    "Neptün": "♆",
    "Plüton": "♇",
    "Kuzey Ay Düğümü": "☊",
    "Lilith": "⚸",
}
PLANETS = list(SYMBOL.keys())


def _house_of_longitude(lonp, cusps):
    """Placidus ev cusp'larına göre gezegenin evini bulur."""
    lonp = lonp % 360
    for i in range(12):
        start = cusps[i] % 360
        end = cusps[(i + 1) % 12] % 360
        if start < end:
            if start <= lonp < end:
                return i + 1
        else:
            if lonp >= start or lonp < end:
                return i + 1
    return 1


def natal_chart(d, time_text, lat, lon, utc=3):
    """Swiss Ephemeris ile gerçek doğum haritası üretir.
    Önemli: Hesap başarısız olursa sahte fallback veri üretmez; açık hata verir.
    """
    import swisseph as swe

    hour, minute = [int(x) for x in time_text.split(":")]
    ut_hour = hour + minute / 60 - float(utc)
    jd = swe.julday(d.year, d.month, d.day, ut_hour)

    planet_ids = {
        "Güneş": swe.SUN,
        "Ay": swe.MOON,
        "Merkür": swe.MERCURY,
        "Venüs": swe.VENUS,
        "Mars": swe.MARS,
        "Jüpiter": swe.JUPITER,
        "Satürn": swe.SATURN,
        "Uranüs": swe.URANUS,
        "Neptün": swe.NEPTUNE,
        "Plüton": swe.PLUTO,
        "Kuzey Ay Düğümü": swe.MEAN_NODE,
        "Lilith": swe.MEAN_APOG,
    }

    cusps, ascmc = swe.houses(jd, float(lat), float(lon), b"P")
    asc = ascmc[0] % 360

    rows = []
    for planet in PLANETS:
        lonp = swe.calc_ut(jd, planet_ids[planet], swe.FLG_MOSEPH)[0][0] % 360
        sign, deg = sign_from_longitude(lonp)
        house = _house_of_longitude(lonp, cusps)

        rows.append({
            "Sembol": SYMBOL[planet],
            "Gezegen": planet,
            "Burç": sign,
            "Derece": format_degree(deg),
            "Ev": house,
            "Element": ELEMENT[sign],
            "Modalite": MODALITY[sign],
            "Boylam": round(lonp, 2),
            "Kaynak": "Swiss Ephemeris",
        })

    asc_sign, asc_deg = sign_from_longitude(asc)

    triad = {
        "Güneş": rows[0]["Burç"],
        "Ay": rows[1]["Burç"],
        "Yükselen": asc_sign,
        "Yükselen Derece": format_degree(asc_deg),
        "Hesap": "Swiss Ephemeris",
    }

    return pd.DataFrame(rows), triad


def aspects(chart):
    defs = [
        (0, "Kavuşum", "Yoğun"),
        (60, "Altmışlık", "Destek"),
        (90, "Kare", "Dikkat"),
        (120, "Üçgen", "Destek"),
        (150, "Quincunx", "Ayar"),
        (180, "Karşıt", "Dikkat"),
    ]

    rows = []
    for i in range(len(chart)):
        for j in range(i + 1, len(chart)):
            a = float(chart.iloc[i]["Boylam"])
            b = float(chart.iloc[j]["Boylam"])
            diff = min(abs(a - b), 360 - abs(a - b))

            for deg, name, effect in defs:
                orb = abs(diff - deg)
                if orb <= 5:
                    rows.append({
                        "Gezegen 1": chart.iloc[i]["Gezegen"],
                        "Açı": name,
                        "Gezegen 2": chart.iloc[j]["Gezegen"],
                        "Orb": round(orb, 2),
                        "Güç": round(max(0, 100 - orb * 18), 1),
                        "Etki": effect,
                    })

    if not rows:
        return pd.DataFrame(columns=["Gezegen 1", "Açı", "Gezegen 2", "Orb", "Güç", "Etki"])
    return pd.DataFrame(rows).sort_values("Güç", ascending=False)


def draw_chart(chart, name):
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)

    theta = np.linspace(0, 2 * np.pi, 720)

    for r, lw in [(0.32, 1), (0.58, 1), (0.82, 1.2), (1.0, 2)]:
        ax.plot(theta, np.ones_like(theta) * r, linewidth=lw)

    for i, s in enumerate(SIGNS):
        th = 2 * np.pi * i / 12
        ax.plot([th, th], [0.32, 1.0], linewidth=.8)
        ax.text(th + np.pi / 12, 1.08, s, ha="center", va="center", fontsize=12, fontweight="bold")

    for h in range(12):
        th = 2 * np.pi * h / 12
        ax.plot([th, th], [0.0, .58], linewidth=.5)
        ax.text(th + np.pi / 12, .46, str(h + 1), ha="center", va="center", fontsize=9)

    for _, row in chart.iterrows():
        th = 2 * np.pi * (float(row["Boylam"]) / 360)
        ax.text(th, .72, row["Sembol"], fontsize=20, ha="center", va="center")

    ax.set_title(f"{name or 'Danışan'} Doğum Haritası", fontsize=17, pad=24)
    return fig

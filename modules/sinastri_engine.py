from .core_utils import SIGNS
def synastry_comment(name,ref_name,triad_a,triad_b,relation_type):
    first=name.split()[0] if name else "Danışan"; ref=ref_name.split()[0] if ref_name else "referans kişi"
    moon_distance=abs(SIGNS.index(triad_a["Ay"])-SIGNS.index(triad_b["Ay"])); sun_distance=abs(SIGNS.index(triad_a["Güneş"])-SIGNS.index(triad_b["Güneş"]))
    score=max(35,min(94,82-moon_distance*3-sun_distance*2))
    comment=f"{first}, {relation_type} alanında {ref} ile uyum yalnızca burç benzerliğiyle okunmaz. Duygusal güven: Ana kişinin Ay burcu {triad_a['Ay']}, referans kişinin Ay burcu {triad_b['Ay']}. Kimlik ve irade: Ana kişinin Güneş burcu {triad_a['Güneş']}, referans kişinin Güneş burcu {triad_b['Güneş']}. Dış tepki: Ana kişinin yükseleni {triad_a['Yükselen']}, referans kişinin yükseleni {triad_b['Yükselen']}. Ön uyum puanı %{score}. Bu puan kesin hüküm değil; güven, sınır, beklenti, sorumluluk ve kriz dili ayrıca konuşulmalıdır."
    return score,comment

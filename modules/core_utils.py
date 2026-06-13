from datetime import datetime
SIGNS=["Koç","Boğa","İkizler","Yengeç","Aslan","Başak","Terazi","Akrep","Yay","Oğlak","Kova","Balık"]
ELEMENT={"Koç":"Ateş","Aslan":"Ateş","Yay":"Ateş","Boğa":"Toprak","Başak":"Toprak","Oğlak":"Toprak","İkizler":"Hava","Terazi":"Hava","Kova":"Hava","Yengeç":"Su","Akrep":"Su","Balık":"Su"}
MODALITY={"Koç":"Öncü","Yengeç":"Öncü","Terazi":"Öncü","Oğlak":"Öncü","Boğa":"Sabit","Aslan":"Sabit","Akrep":"Sabit","Kova":"Sabit","İkizler":"Değişken","Başak":"Değişken","Yay":"Değişken","Balık":"Değişken"}
def digital_root(n:int)->int:
    n=abs(int(n or 0))
    while n>9: n=sum(int(d) for d in str(n))
    return n
def parse_date(text):
    if not text: return None
    for fmt in ("%Y/%m/%d","%d.%m.%Y","%Y-%m-%d","%d/%m/%Y"):
        try: return datetime.strptime(text.strip(),fmt).date()
        except Exception: pass
    return None
def sign_from_longitude(lon):
    lon=lon%360; idx=int(lon//30); deg=lon%30
    return SIGNS[idx],deg
def format_degree(deg):
    d=int(deg); m=int((deg-d)*60)
    return f"{d}°{m:02d}'"

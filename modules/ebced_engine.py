import pandas as pd
from .core_utils import digital_root
ABJAD={"ا":1,"أ":1,"إ":1,"آ":1,"ب":2,"ج":3,"د":4,"ه":5,"ة":5,"و":6,"ز":7,"ح":8,"ط":9,"ي":10,"ى":10,"ك":20,"گ":20,"ل":30,"م":40,"ن":50,"س":60,"ع":70,"ف":80,"ص":90,"ق":100,"ر":200,"ش":300,"ت":400,"ث":500,"خ":600,"ذ":700,"ض":800,"ظ":900,"غ":1000}
def calculate_ebced(arabic_text):
    total=0; rows=[]
    for ch in (arabic_text or "").replace(" ",""):
        val=ABJAD.get(ch,0)
        if val:
            total+=val; rows.append({"Harf":ch,"Değer":val,"Toplam":total})
    return {"ebced":total,"core":digital_root(total),"table":pd.DataFrame(rows)}
def birth_matrix(d):
    raw=int(d.strftime("%Y%m%d"))
    return {"Gün kodu":d.day,"Ay kodu":d.month,"Yıl kodu":d.year,"Tarih rakam toplamı":sum(int(x) for x in d.strftime("%Y%m%d")),"Doğum kökü":digital_root(raw),"Gün kökü":digital_root(d.day),"Ay kökü":digital_root(d.month),"Yıl kökü":digital_root(d.year)}

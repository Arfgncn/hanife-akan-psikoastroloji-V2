from datetime import date,timedelta
import pandas as pd
def period_scores(core,days=30):
    rows=[]; start=date.today()
    for i in range(days):
        d=start+timedelta(days=i); base=(d.toordinal()+core*17)%100; destek=40+((base*7)%60); dikkat=35+((base*11)%65); score=round(destek/(destek+dikkat)*100,1)
        if score>=58: konu="imza öncesi görüşme, teklif, hazırlık, sunum"; oneri="Destekli; yine de yazılı teyit alınmalı."
        elif score<=45: konu="gecikme, yanlış anlama, yüksek riskli karar"; oneri="Acele imza yok; ikinci kontrol gerekli."
        else: konu="bekle-gözle, veri toplama, hazırlık"; oneri="Küçük ve geri döndürülebilir adım uygun."
        rows.append({"Tarih":d.isoformat(),"Karar Skoru":score,"Destek":destek,"Dikkat":dikkat,"Ana Tema":konu,"Öneri":oneri})
    return pd.DataFrame(rows)
def hanife_style_period_comment(df):
    best=df.sort_values("Karar Skoru",ascending=False).head(5); risk=df.sort_values("Karar Skoru",ascending=True).head(5)
    lines=["DESTEKLİ ZAMAN KAPILARI"]
    for _,r in best.iterrows(): lines.append(f"{r['Tarih']}: {r['Ana Tema']}. Destek {r['Destek']}, dikkat {r['Dikkat']}. Bu gün görüşme, sunum, niyet netleştirme ve hazırlık için daha verimli çalışır.")
    lines.append("\nDİKKAT VE İKİNCİ KONTROL GÜNLERİ")
    for _,r in risk.iterrows(): lines.append(f"{r['Tarih']}: {r['Ana Tema']}. Destek {r['Destek']}, dikkat {r['Dikkat']}. Sözleşme, para, ilişki ve sağlık düzeni alanlarında acele edilmemeli.")
    lines.append("\nUYGULANABİLİR PROTOKOL\n1. Destekli günlerde görüşme yapılabilir; imza için madde madde kontrol gerekir.\n2. Dikkat günlerinde tartışma, ani para kararı ve belirsiz sözleşmeden kaçınılır.\n3. Her önemli konuda önce veri topla, sonra küçük adım at.")
    return "\n".join(lines)

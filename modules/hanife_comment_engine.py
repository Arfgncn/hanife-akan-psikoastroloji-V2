import json
from pathlib import Path
def load_data(fname):
    return json.loads((Path(__file__).resolve().parents[1]/"data"/fname).read_text(encoding="utf-8"))
def personal_opening(name,triad,main_esma,birth_root):
    first=name.split()[0] if name else "Danışan"
    return f"{first}, bu okuma kesin kader hükmü vermek için değil; benliğinizi ve karar verirken hangi iç sistemle çalıştığınızı anlamak için hazırlanır. Haritanızın temel üçlüsü Güneş {triad['Güneş']}, Ay {triad['Ay']}, Yükselen {triad['Yükselen']} olarak çalışıyor. İsim frekansınızda {main_esma['name']} teması öne çıkıyor. Doğum kökünüz {birth_root}; bu da yaşam olaylarını hangi öğrenme ritmiyle karşıladığınızı gösterir. İlk soru “Bana ne olacak?” değil; “Ben bu enerjiyi nasıl daha bilinçli kullanacağım?” olmalıdır."
def house_comment(chart):
    houses=load_data("ev_yorumlari.json"); planets=load_data("gezegen_yorumlari.json"); out=[]
    for h in range(1,13):
        found=chart[chart["Ev"]==h]; meta=houses[str(h)]
        text=[f"<h4>{h}. Ev — {meta['title']}</h4>",f"Bu ev {meta['meaning']}. Danışmanlıkta özellikle {meta['work']} alanlarında okunur."]
        if len(found):
            for _,r in found.iterrows():
                p=planets.get(r["Gezegen"],{})
                text.append(f"<b>{r['Gezegen']} {r['Burç']}:</b> {p.get('meaning','gezegen alanı')} temasını {r['Burç']} diliyle çalıştırır. Gölge: {p.get('shadow','bilinç ister')}. Öneri: {p.get('advice','ikinci kontrol yap')}")
        else:
            text.append("Bu evde gezegen yok; yorum ev başlangıcı, yöneticisi ve transit tetiklenmeleriyle yapılır.")
        text.append(f"<i>Farkındalık sorusu: {meta['question']}</i>")
        out.append("<br>".join(text))
    return "<hr>".join(out)
def aspect_comment(aspects):
    templates=load_data("aci_yorumlari.json")
    if aspects.empty: return "Belirgin ana açı bulunmadı; harita ev yöneticileri ve transitlerle detaylandırılmalıdır."
    lines=[]
    for _,r in aspects.head(18).iterrows():
        lines.append(f"<b>{r['Gezegen 1']} {r['Açı']} {r['Gezegen 2']}</b> / Orb {r['Orb']} / Güç {r['Güç']}: {templates.get(r['Açı'],'Bu açı bilinçli yorum ister')} Etki: {r['Etki']}.")
    return "<br><br>".join(lines)
def full_report(name,ebced,core,main_esma,support_esma,bm,triad,chart,aspects,period_text,advisor_note=""):
    return f"""HANİFE AKAN PSİKOASTROLOJİ\nPsikoloji • Astroloji • Bilinç\nSeni Kim Yazdı?\n\nDanışan: {name}\nEbced: {ebced}\nÇekirdek: {core}\nAna Esma: {main_esma['name']} — {main_esma['theme']}\nDestek Esma: {support_esma['name']} — {support_esma['theme']}\nDoğum kökü: {bm['Doğum kökü']}\nTemel üçlü: Güneş {triad['Güneş']} / Ay {triad['Ay']} / Yükselen {triad['Yükselen']}\n\n1. BENLİK VE TEKÂMÜL\n{personal_opening(name,triad,main_esma,bm['Doğum kökü'])}\n\n2. ESMA OKUMASI\nAna Esma alanı {main_esma['name']} olduğu için olaylar {main_esma['theme']} penceresinden okunur. Gölge: {main_esma['shadow']} İş/para: {main_esma['career']} İlişki: {main_esma['relationship']}\n\n3. ZAMAN KAPILARI\n{period_text}\n\n4. HANİFE DANIŞMAN NOTU\n{advisor_note or 'Bu alan danışmanın sezgisel ve kişiye özel notları için ayrılmıştır.'}\n\nSONUÇ\nBu rapor kesin gelecek iddiası taşımaz; karar öncesi bilinçli kontrol haritası üretir."""

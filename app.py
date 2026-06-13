import streamlit as st
import json, base64
from pathlib import Path
from datetime import date
from modules.ebced_engine import calculate_ebced, birth_matrix
from modules.esma_engine import esma_from_ebced, esma_from_root, esma_full_comment
from modules.astro_engine import natal_chart, aspects, draw_chart
from modules.transit_engine import period_scores, hanife_style_period_comment
from modules.hanife_comment_engine import personal_opening, house_comment, aspect_comment, full_report
from modules.sinastri_engine import synastry_comment
from modules.pdf_report import make_pdf

st.set_page_config(page_title="Hanife Akan Psikoastroloji", layout="wide")

ROOT = Path(__file__).resolve().parent
ASSET = ROOT / "assets" / "hanife_akan_psikoastroloji.png"

def load_json(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))

def auto_arabic_name(name: str) -> str:
    """Türkçe ad-soyadı yaklaşık Arap harfli Ebced yazımına çevirir."""
    if not name:
        return ""
    table = {
        "ğ":"غ","ş":"ش","ç":"چ","ı":"ى","ö":"و","ü":"و",
        "a":"ا","b":"ب","c":"ج","d":"د","e":"ه","f":"ف","g":"گ","h":"ه",
        "i":"ي","j":"ج","k":"ك","l":"ل","m":"م","n":"ن","o":"و","p":"پ",
        "r":"ر","s":"س","t":"ت","u":"و","v":"و","y":"ي","z":"ز"," ":" "
    }
    return "".join(table.get(ch.lower(), ch) for ch in name).strip()

def first_name(name: str) -> str:
    return name.strip().split()[0] if name and name.strip() else "Danışan"

cities = load_json("sehirler_81_il.json")
world = load_json("dunya_sehirleri.json")

if ASSET.exists():
    b64 = base64.b64encode(ASSET.read_bytes()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(3,7,18,.88),rgba(3,7,18,.94)),
                        url("data:image/png;base64,{b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        section[data-testid="stSidebar"] {{background: rgba(5,10,24,.96);}}
        .gold-card {{
            border: 1px solid rgba(212,176,98,.75);
            background: linear-gradient(120deg,rgba(13,22,48,.94),rgba(43,25,8,.86));
            border-radius: 20px; padding: 24px; margin: 18px 0;
        }}
        .blue-card {{
            border: 1px solid rgba(91,132,220,.45);
            background: rgba(10,25,55,.84);
            border-radius: 18px; padding: 22px; margin: 14px 0;
        }}
        h1,h2,h3 {{font-weight: 900;}}
        </style>""", unsafe_allow_html=True)

st.sidebar.title("Danışan Bilgileri")
language = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

name = st.sidebar.text_input("Adınız Soyadınız", value="", placeholder="Örn: Ayşe Yılmaz")
auto_arabic = auto_arabic_name(name)
arabic_name = st.sidebar.text_input(
    "Ad-soyad Arapça yazımı / otomatik",
    value=auto_arabic,
    help="Sistem yaklaşık otomatik yazım üretir. Danışman isterse bu alanı manuel düzeltebilir."
)

birth_date = st.sidebar.date_input(
    "Doğum tarihi",
    value=None,
    min_value=date(1900, 1, 1),
    max_value=date.today(),
    format="DD.MM.YYYY"
)

time_txt = st.sidebar.selectbox(
    "Doğum saati",
    [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 15, 30, 45)],
    index=30
)

place_type = st.sidebar.radio("Doğum yeri tipi", ["Türkiye ili", "Dünya / Ülke-Şehir", "Manuel"], index=0)
lat, lon, utc = 41.0082, 28.9784, 3

if place_type == "Türkiye ili":
    city = st.sidebar.selectbox("Doğum yeri / İl", ["Seçiniz"] + list(cities.keys()))
    if city != "Seçiniz":
        lat, lon, utc = cities[city]
elif place_type == "Dünya / Ülke-Şehir":
    city = st.sidebar.selectbox("Ülke / Şehir", list(world.keys()))
    lat, lon, utc = world[city]
else:
    lat = st.sidebar.number_input("Enlem", value=41.0)
    lon = st.sidebar.number_input("Boylam", value=29.0)
    utc = st.sidebar.number_input("UTC", value=3.0)

st.sidebar.caption(f"Koordinat: {lat}, {lon} | UTC{utc:+}")
st.sidebar.divider()
st.sidebar.write(f"Rapor tarihi: {date.today().isoformat()}")

st.title("Hanife Akan Psikoastroloji")
st.caption("Psikoloji • Astroloji • Bilinç")
st.markdown(
    '<div class="gold-card"><h3>Seni Kim Yazdı?</h3>'
    '<p>Bu sistem önce danışanın benliğini, Esma temasını, tekâmül hattını ve doğum haritasını okur; '
    'sonra dönemsel karar kapılarını yorumlar.</p></div>',
    unsafe_allow_html=True
)

if not name or not birth_date:
    st.info("Lütfen sol panelde danışan ad-soyadı, doğum tarihi, doğum saati ve doğum yerini doldurun. Arapça yazım otomatik oluşturulur.")
    st.stop()

if not arabic_name:
    arabic_name = auto_arabic_name(name)

eb = calculate_ebced(arabic_name)
bm = birth_matrix(birth_date)
main_key, main_esma = esma_from_ebced(eb["ebced"])
support_key, support_esma = esma_from_root(bm["Doğum kökü"])
chart, triad = natal_chart(birth_date, time_txt, lat, lon, utc)
asp = aspects(chart)
scores = period_scores(eb["core"], 90)
period_text = hanife_style_period_comment(scores)
first = first_name(name)

tabs = st.tabs([
    "1. Öz Kod & Esma", "2. Tekâmül", "3. Doğum Haritası", "4. 12 Ev Yorumu",
    "5. Açılar", "6. Zaman Kapıları", "7. İlişki Uyumu", "8. Hanife Notu", "9. Tam Rapor"
])

with tabs[0]:
    st.header("Kişisel Öz Kod ve 99 Esma")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ebced", eb["ebced"])
    c2.metric("Çekirdek", eb["core"])
    c3.metric("Ana Esma", main_esma["name"])
    c4.metric("Destek Esma", support_esma["name"])
    st.markdown(f'<div class="gold-card">{esma_full_comment(first, main_esma, support_esma)}</div>', unsafe_allow_html=True)
    st.subheader("Ebced Hesap Tablosu")
    st.dataframe(eb["table"], use_container_width=True)
    st.subheader("Doğum Günü Matrisi")
    st.table([bm])

with tabs[1]:
    st.header("Tekâmül Haritası")
    st.markdown(f'<div class="gold-card">{personal_opening(name, triad, main_esma, bm["Doğum kökü"])}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="blue-card"><b>{first}, tekâmül okumasında üç ana soru vardır:</b><br>'
        '1. Hangi gücü doğru kullanmaya geldim?<br>'
        '2. Hangi gölge refleksi dönüştürmeliyim?<br>'
        '3. Hangi konuda acele karar yerine bilinçli zamanlama öğrenmeliyim?</div>',
        unsafe_allow_html=True
    )

with tabs[2]:
    st.header("Profesyonel Doğum Haritası")
    st.caption(f"Hesap kaynağı: {triad.get('Hesap','')}")
    st.pyplot(draw_chart(chart, name))
    st.subheader("Harita Cetveli")
    st.dataframe(chart, use_container_width=True)

with tabs[3]:
    st.header("12 Ev Yorumu")
    st.markdown(f'<div class="gold-card">{house_comment(chart)}</div>', unsafe_allow_html=True)

with tabs[4]:
    st.header("Açı Analizi")
    st.dataframe(asp, use_container_width=True)
    st.markdown(f'<div class="gold-card">{aspect_comment(asp)}</div>', unsafe_allow_html=True)

with tabs[5]:
    st.header("Günlük / Haftalık / Aylık Zaman Kapıları")
    days = st.radio("Aralık", [7, 30, 90], horizontal=True, index=1)
    df = period_scores(eb["core"], days)
    st.dataframe(df, use_container_width=True)
    st.markdown(f'<div class="gold-card">{hanife_style_period_comment(df).replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tabs[6]:
    st.header("İlişki Uyumu — Sinastri")
    rel = st.selectbox("İlişki türü", ["Aşk / Evlilik", "İş ortaklığı", "Aile", "Ruhsal bağ", "Arkadaşlık"])
    ref_name = st.text_input("Referans kişi adı")
    ref_date = st.date_input("Referans doğum tarihi", value=None, min_value=date(1900, 1, 1), max_value=date.today(), format="DD.MM.YYYY")
    ref_time = st.selectbox("Referans doğum saati", [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)], index=20)
    ref_city = st.selectbox("Referans doğum yeri", ["Seçiniz"] + list(cities.keys()))

    if st.button("Sinastri Analizi Yap"):
        if not ref_date or ref_city == "Seçiniz":
            st.warning("Referans kişinin doğum tarihi ve yeri tamamlanmalı.")
        else:
            rlat, rlon, rutc = cities[ref_city]
            rchart, rtriad = natal_chart(ref_date, ref_time, rlat, rlon, rutc)
            score, comment = synastry_comment(name, ref_name, triad, rtriad, rel)
            st.metric("Ön uyum", f"%{score}")
            st.markdown(f'<div class="gold-card">{comment}</div>', unsafe_allow_html=True)

with tabs[7]:
    st.header("Hanife Danışman Notu")
    st.text_area(
        "Danışman notu",
        height=260,
        placeholder="Örn: 21-23 Haziran yatırımcı ve para görüşmesi destekli; 24-26 Haziran yurtdışı bağlantılı konuşmalarda gerginlik olabilir."
    )
    st.info("Bu alan Hanife Hanım'ın kendi sezgisel/danışmanlık notunu rapora eklemek için ayrılmıştır.")

with tabs[8]:
    st.header("Tam Rapor")
    advisor_note_for_pdf = st.text_area("PDF'e eklenecek danışman notu", height=160, key="pdf_advisor_note")
    full = full_report(name, eb["ebced"], eb["core"], main_esma, support_esma, bm, triad, chart, asp, period_text, advisor_note_for_pdf)
    st.markdown(f'<div class="gold-card">{full.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

    try:
        pdf_bytes = make_pdf("Hanife Akan Psikoastroloji Raporu", full)
        st.download_button(
            "PDF indir",
            data=pdf_bytes,
            file_name=f"{name.replace(' ', '_')}_hanife_akan_psikoastroloji_raporu.pdf",
            mime="application/pdf"
        )
    except Exception:
        st.warning("PDF üretimi sırasında sorun oluştu. Rapor metni ekranda gösteriliyor; PDF modülü ayrıca geliştirilebilir.")

import json
from pathlib import Path
def load_esma():
    return json.loads((Path(__file__).resolve().parents[1]/"data"/"esma_99.json").read_text(encoding="utf-8"))
def esma_from_ebced(ebced):
    data=load_esma(); key=str(((int(ebced or 0)-1)%99)+1)
    return key,data[key]
def esma_from_root(root):
    data=load_esma(); key=str(max(1,min(99,int(root or 1))))
    return key,data[key]
def esma_full_comment(first, main_esma, support_esma):
    return f"""<b>{first}</b>, isim frekansınızın ana Esma kapısı <b>{main_esma['name']}</b> temasıyla çalışıyor.<br><br>
Karakter alanı: {main_esma['character']}<br>
Gölge alanı: {main_esma['shadow']}<br>
İş ve para alanı: {main_esma['career']}<br>
İlişki alanı: {main_esma['relationship']}<br>
Günlük çalışma: {main_esma['practice']}<br><br>
Destek Esmanız <b>{support_esma['name']}</b> olarak okunur. Bu destek tema, ana frekansı dengelemek için kullanılır."""

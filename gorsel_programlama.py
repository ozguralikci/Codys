from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from veritabani.baglanti import db
from veritabani.modeller import Proje

gorsel_programlama_blueprint = Blueprint('gorsel_programlama', __name__)

@gorsel_programlama_blueprint.route('/gorsel-programlama')
@login_required
def gorsel_programlama_sayfasi():
    return render_template('gorsel_programlama.html')

@gorsel_programlama_blueprint.route('/kod-olustur', methods=['POST'])
@login_required
def kod_olustur():
    bloklar = request.json['bloklar']
    python_kodu = blokları_koda_cevir(bloklar)
    
    # Oluşturulan kodu veritabanına kaydet
    yeni_proje = Proje(kullanici_id=current_user.id, proje_adi="Görsel Proje", icerik=python_kodu)
    db.session.add(yeni_proje)
    db.session.commit()
    
    return jsonify({"kod": python_kodu, "proje_id": yeni_proje.id})

def blokları_koda_cevir(bloklar):
    kod = ""
    girinti = 0
    for blok in bloklar:
        if blok['tip'] == 'print':
            kod += "    " * girinti + f"print('{blok['deger']}')\n"
        elif blok['tip'] == 'if':
            kod += "    " * girinti + f"if {blok['kosul']}:\n"
            girinti += 1
        elif blok['tip'] == 'for':
            kod += "    " * girinti + f"for {blok['degisken']} in range({blok['baslangic']}, {blok['bitis']}):\n"
            girinti += 1
        elif blok['tip'] == 'while':
            kod += "    " * girinti + f"while {blok['kosul']}:\n"
            girinti += 1
        elif blok['tip'] = 'fonksiyon':
            kod += "    " * girinti + f"def {blok['isim']}({', '.join(blok['parametreler'])}):\n"
            girinti += 1
        elif blok['tip'] == 'end':
            girinti -= 1
    return kod

@gorsel_programlama_blueprint.route('/blok-sablonlari')
@login_required
def blok_sablonlari():
    sablonlar = [
        {"tip": "print", "etiket": "Yazdır", "deger": ""},
        {"tip": "if", "etiket": "Eğer", "kosul": ""},
        {"tip": "for", "etiket": "Döngü", "degisken": "i", "baslangic": 0, "bitis": 10},
        {"tip": "while", "etiket": "Sürekli Döngü", "kosul": ""},
        {"tip": "fonksiyon", "etiket": "Fonksiyon", "isim": "", "parametreler": []},
        {"tip": "end", "etiket": "Bitir"}
    ]
    return jsonify(sablonlar)

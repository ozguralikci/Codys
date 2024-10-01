import os
from dotenv import load_dotenv
from flask import Flask
from veritabani.baglanti import VeritabaniBaglantisi
from web_arayuzu.routes import ana_blueprint
from yapay_zeka.kod_analizi import KodAnalizcisi
from web_arayuzu.gorsel_programlama import gorsel_programlama_blueprint
from ana.cevrimdisi_mod import CevrimdisiMod
from web_tarama.tarayici import WebTarayici
from guvenlik.guvenlik_modulu import GuvenlikModulu
from yapay_zeka.ogrenme_motoru import OgrenmeMotoruAPI

load_dotenv()

class CodyS:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.veritabani = VeritabaniBaglantisi(self.app)
        self.kod_analizcisi = KodAnalizcisi()
        self.cevrimdisi_mod = CevrimdisiMod()
        self.web_tarayici = WebTarayici()
        self.guvenlik = GuvenlikModulu()
        self.ogrenme_motoru = OgrenmeMotoruAPI()

        self.register_blueprints()

    def register_blueprints(self):
        self.app.register_blueprint(ana_blueprint)
        self.app.register_blueprint(gorsel_programlama_blueprint)

    def baslat(self):
        port = int(os.getenv('PORT', 5000))
        self.app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    codys = CodyS()
    codys.baslat()

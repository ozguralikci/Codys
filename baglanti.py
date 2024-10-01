from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

class VeritabaniBaglantisi:
    def __init__(self, app):
        db.init_app(app)
        Migrate(app, db)
        
        from veritabani.modeller import Kullanici, Proje
        with app.app_context():
            db.create_all()

    def kullanici_ekle(self, kullanici_adi, sifre):
        from veritabani.modeller import Kullanici
        yeni_kullanici = Kullanici(kullanici_adi=kullanici_adi, sifre=sifre)
        db.session.add(yeni_kullanici)
        db.session.commit()
        return yeni_kullanici

    def kullanici_dogrula(self, kullanici_adi, sifre):
        from veritabani.modeller import Kullanici
        kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
        if kullanici and kullanici.sifre_kontrol(sifre):
            return kullanici
        return None

    def proje_ekle(self, kullanici_id, proje_adi, icerik):
        from veritabani.modeller import Proje
        yeni_proje = Proje(kullanici_id=kullanici_id, proje_adi=proje_adi, icerik=icerik)
        db.session.add(yeni_proje)
        db.session.commit()
        return yeni_proje

    def projeleri_getir(self, kullanici_id):
        from veritabani.modeller import Proje
        return Proje.query.filter_by(kullanici_id=kullanici_id).all()

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from veritabani.baglanti import db
from veritabani.modeller import Kullanici, Proje
from yapay_zeka.kod_analizi import KodAnalizcisi
from guvenlik.guvenlik_modulu import GuvenlikModulu

ana_blueprint = Blueprint('ana', __name__)
kod_analizcisi = KodAnalizcisi()
guvenlik = GuvenlikModulu()

@ana_blueprint.route('/')
def ana_sayfa():
    return render_template('ana_sayfa.html')

@ana_blueprint.route('/giris', methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        kullanici_adi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
        if kullanici and kullanici.sifre_kontrol(sifre):
            login_user(kullanici)
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('ana.dashboard'))
        flash('Geçersiz kullanıcı adı veya şifre', 'error')
    return render_template('giris.html')

@ana_blueprint.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        kullanici_adi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        if not guvenlik.basit_sifre_kontrolu(sifre):
            flash('Şifre yeterince güçlü değil', 'error')
            return render_template('kayit.html')
        yeni_kullanici = Kullanici(kullanici_adi=kullanici_adi)
        yeni_kullanici.sifre_belirle(sifre)
        db.session.add(yeni_kullanici)
        db.session.commit()
        flash('Hesabınız başarıyla oluşturuldu!', 'success')
        return redirect(url_for('ana.giris'))
    return render_template('kayit.html')

@ana_blueprint.route('/dashboard')
@login_required
def dashboard():
    projeler = Proje.query.filter_by(kullanici_id=current_user.id).all()
    return render_template('dashboard.html', projeler=projeler)

@ana_blueprint.route('/kod-analizi', methods=['POST'])
@login_required
def kod_analizi():
    kod = request.form['kod']
    sonuclar = kod_analizcisi.analiz_et(kod)
    return jsonify(sonuclar)

@ana_blueprint.route('/cikis')
@login_required
def cikis():
    logout_user()
    flash('Başarıyla çıkış yaptınız', 'success')
    return redirect(url_for('ana.ana_sayfa'))

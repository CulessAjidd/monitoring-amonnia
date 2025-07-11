from flask import Blueprint, render_template, flash, redirect, request, url_for, session, jsonify

from app.forms import JadwalForm
from app.models.kecamatan import Kecamatan
from app.services.mail_service import send_email

jadwal_bp = Blueprint('jadwal', __name__)

@jadwal_bp.route('/jadwal')
def lihat_jadwal():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])
    return render_template('jadwal/lihat-jadwal.html',
                           title='Jadwal',
                           subtitle='Jadwal Penyebaran / Lihat Jadwal',
                           )


@jadwal_bp.route('/jadwal/tambah', methods=['GET', 'POST'])
def tambah_jadwal():

    form = JadwalForm()

    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumad', 'Sabtu', 'Minggu']
    kecamatan = Kecamatan.query.filter_by(kabupaten_id=1).order_by(Kecamatan.name.asc()).all()

    if form.validate_on_submit():
        min_val = form.minimal.data
        max_val = form.maximal.data
        print(min_val, max_val)
        print(f"Valid! Minimal: {min_val}, Maksimal: {max_val}", "success")
    else:
        print("Form tidak valid!")
        print(form.errors)  # ← ini cetak semua error dalam bentuk dict
        print("maximal.errors =", form.maximal.errors)
    # result = send_email(
    #     subject="Selamat Datang di Aplikasi Kami",
    #     recipients=["muhajidachmad@gmail.com"],
    #     template_name="emails/info.html",
    #     context={"username": "Ajid"},
    #     bcc=["ajid.developer@gmail.com"]
    # )

    return render_template('jadwal/tambah-jadwal.html',
                           title='Jadwal',
                           subtitle = 'Jadwal Penyebaran / Tambah Jadwal',
                           days = days,
                           kecamatan = kecamatan,
                           form = form)






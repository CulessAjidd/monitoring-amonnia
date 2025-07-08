from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify
from app.services.mail_service import send_email

jadwal_bp = Blueprint('jadwal', __name__)

@jadwal_bp.route('/jadwal')
def lihat_jadwal():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])
    return render_template('jadwal/lihat-jadwal.html')


@jadwal_bp.route('/jadwal/tambah', methods=['GET'])
def tambah_jadwal():

    # result = send_email(
    #     subject="Selamat Datang di Aplikasi Kami",
    #     recipients=["muhajidachmad@gmail.com"],
    #     template_name="emails/info.html",
    #     context={"username": "Ajid"},
    #     bcc=["ajid.developer@gmail.com"]
    # )

    return jsonify({"status": "result"})






import sys

from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from flask_login import login_required, login_user

from app.forms import LoginForm
from app.models.role import Role
from app.models.user import User
from app import db
import pandas as pd

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        else:
            print(form.errors)
            flash("Email atau password salah")
    elif request.method == 'POST':
        print(form.errors)
        flash("Email atau password salah")
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

# optional: untuk membuat user admin
@auth_bp.route('/create-admin')
def create_admin():
    role = Role.query.filter_by(name='admin').first()
    if not role:
        role = Role(name='admin')
        db.session.add(role)
        db.session.commit()

    user = User.query.filter_by(email='admin@gmail.com').first()
    if not user:
        user = User(name='Admin', email='admin@gmail.com', kode_admin='0001', role_id=role.id, kabupaten_id=1)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

    return "User admin berhasil dibuat!"

# @auth_bp.route('/provinsi')
# def create_provinsi():
#     is_empty = Provinsi.query.first() is None
#     if not is_empty:
#         return "Provinsi sudah ada"
#
#     df = pd.read_csv("./data/indonesia-38-provinsi-main/provinsi.csv")
#
#     provinsi = [Provinsi(name=row['name'], kode=row['id']) for _, row in df.iterrows()]
#     db.session.bulk_save_objects(provinsi)
#     db.session.commit()
#     return "Provinsi berhasil dibuat!"
#
# @auth_bp.route('/kabupaten')
# def create_kabupaten():
#     is_empty = Kabupaten.query.first() is None
#     if not is_empty:
#         return "Kabupaten sudah ada"
#
#     df = pd.read_csv("./data/indonesia-38-provinsi-main/kabupaten_kota.csv", dtype={'id': str})
#     kabupaten = []
#     for _, row in df.iterrows():
#         kab_id = str(row['id'])
#         name = row['name']
#         kode = row['id']
#         provinsi_id = str(kab_id[:2])
#
#         provinsi = Provinsi.query.filter_by(kode=provinsi_id).first()
#         if provinsi:
#             kabupaten.append(Kabupaten(kode=kode, name=name, provinsi_id=provinsi.id))
#         else:
#             print(f"Provinsi dengan kode {provinsi_id} tidak ditemukan untuk kabupaten {name}")
#
#     db.session.bulk_save_objects(kabupaten)
#     db.session.commit()
#     return "Kabupaten berhasil dibuat!"
#
# @auth_bp.route('/kecamatan')
# def create_kecamatan():
#     is_empty = Kecamatan.query.first() is None
#     if not is_empty:
#         return "Kecamatan sudah ada"
#
#     df = pd.read_csv("./data/indonesia-38-provinsi-main/kecamatan.csv", dtype={'id': str})
#     kecamatan = []
#     for _, row in df.iterrows():
#         kec_id = str(row['id'])
#         name = row['name']
#         kode = row['id']
#         kabupaten_id = str(kec_id[:5])
#         kabupaten = Kabupaten.query.filter_by(kode=kabupaten_id).first()
#
#         if kabupaten:
#             kecamatan.append(Kecamatan(kode=kode, name=name, kabupaten_id=kabupaten.id))
#         else:
#             print(f"Kabupaten dengan kode {kabupaten_id} tidak ditemukan untuk kabupaten {name}")
#
#     db.session.bulk_save_objects(kecamatan)
#     db.session.commit()
#     return "Kecamatan berhasil dibuat!"
#
# @auth_bp.route('/kelurahan')
# def create_kelurahan():
#     is_empty = Kelurahan.query.first() is None
#     if not is_empty:
#         return "Kelurahan sudah ada"
#
#     find_non_ascii_in_file("./data/indonesia-38-provinsi-main/kelurahan.csv")
#     df = pd.read_csv("./data/indonesia-38-provinsi-main/kelurahan.csv", dtype={'id': str})
#     kelurahan = []
#     for _, row in df.iterrows():
#         kel_id = str(row['id'])
#         name = row['name']
#         kode = row['id']
#         kecamatan_id = str(kel_id[:8])
#         kecamatan = Kecamatan.query.filter_by(kode=kecamatan_id).first()
#
#         if kecamatan:
#             kelurahan.append(Kelurahan(kode=kode, name=name, kecamatan_id=kecamatan.id))
#         else:
#             print(f"Kecamatan dengan kode {kecamatan_id} tidak ditemukan untuk kabupaten {name}")
#
#     db.session.bulk_save_objects(kelurahan)
#     db.session.commit()
#     return "Kelurahan berhasil dibuat!"


def find_non_ascii_in_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, start=1):
            for col_num, char in enumerate(line):
                if ord(char) > 127:
                    print(
                        f"[Baris {line_num}, Posisi {col_num}] Karakter: '{char}' → ASCII: {ord(char)}")
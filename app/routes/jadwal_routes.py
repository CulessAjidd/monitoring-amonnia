from zoneinfo import ZoneInfo

from flask import Blueprint, render_template, flash, redirect, request, url_for, session, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date

from app import db
from app.forms import JadwalForm
from app.models.jadwal import Jadwal
from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan
from app.models.role import Role
from app.models.user import User
from app.services.mail_service import send_email

jadwal_bp = Blueprint('jadwal', __name__)


@jadwal_bp.route('/jadwal')
@login_required
def lihat_jadwal():
    search = request.args.get("search", "", type=str)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = (db.session.query(Jadwal)
             .join(Kecamatan, Jadwal.kecamatan_id == Kecamatan.id)
             .join(Kelurahan, Jadwal.kelurahan_id == Kelurahan.id)
             .filter(Jadwal.deleted_at == None)
             .order_by(Jadwal.id.desc()))

    if search:
        like = f"%{search}%"
        query = query.filter(
            Kelurahan.name.ilike(like) |
            Kecamatan.name.ilike(like) |
            Jadwal.tanggal.ilike(like) |
            Jadwal.status.ilike(like)
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # routes.py (sebelum return render_template)
    current_page = pagination.page
    total_pages = pagination.pages

    # tampilkan range 5 halaman di sekitar current
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, current_page + 2)

    page_range = range(start_page, end_page + 1)

    results = []
    for jadwal in pagination.items:
        dt_mulai = datetime.combine(date.today(), jadwal.jam_mulai)
        dt_selesai = datetime.combine(date.today(), jadwal.jam_selesai)
        durasi = dt_selesai - dt_mulai
        total_menit = durasi.total_seconds() // 60
        jam = int(total_menit // 60)
        menit = int(total_menit % 60)
        results.append({
            "id": jadwal.id,
            "tanggal": jadwal.tanggal,
            "kecamatan": jadwal.kecamatan.name,
            "kelurahan": jadwal.kelurahan.name,
            "jam_mulai": jadwal.jam_mulai,
            "durasi": f"{jam} jam {menit} menit",
            "kadar": f"{jadwal.kadar_min}% - {jadwal.kadar_max}%",
            "kadar_min": jadwal.kadar_min,
            "kadar_max": jadwal.kadar_max,
            "status": jadwal.status,
        })
    return render_template('jadwal/lihat-jadwal.html',
                           title='Jadwal',
                           subtitle='Jadwal Penyebaran / Lihat Jadwal',
                           pagination=pagination,
                           search=search,
                           page_range=page_range,
                           results=results
                           )


@jadwal_bp.route('/jadwal/tambah', methods=['GET', 'POST'])
@login_required
def tambah_jadwal():
    form = JadwalForm()

    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumad', 'Sabtu', 'Minggu']
    kecamatan = Kecamatan.query.filter_by(kabupaten_id=current_user.kabupaten_id).order_by(Kecamatan.name.asc()).all()

    if form.validate_on_submit():
        jadwal = Jadwal(
            title=form.title.data,
            description=form.description.data,
            hari=form.hari.data,
            tanggal=form.tanggal.data,
            jam_mulai=form.jam_mulai.data,
            jam_selesai=form.jam_selesai.data,
            user_id=current_user.id,
            kecamatan_id=form.kecamatan.data,
            kelurahan_id=form.kelurahan.data,
            kadar_min=form.minimal.data,
            kadar_max=form.maximal.data
        )

        db.session.add(jadwal)
        db.session.commit()
        flash('Jadwal berhasil ditambahkan', 'success')
        return redirect(url_for('jadwal.lihat_jadwal'))

    return render_template('jadwal/tambah-jadwal.html',
                           title='Jadwal',
                           subtitle='Jadwal Penyebaran / Tambah Jadwal',
                           days=days,
                           kecamatan=kecamatan,
                           form=form)


@jadwal_bp.route('/jadwal/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jadwal(id):
    jadwal = Jadwal.query.get_or_404(id)
    form = JadwalForm()

    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumad', 'Sabtu', 'Minggu']
    kecamatan = Kecamatan.query.filter_by(kabupaten_id=current_user.kabupaten_id).order_by(Kecamatan.name.asc()).all()

    if form.validate_on_submit():
        jadwal.title = form.title.data
        jadwal.description = form.description.data
        jadwal.hari = form.hari.data
        jadwal.tanggal = form.tanggal.data
        jadwal.kecamatan_id = form.kecamatan.data
        jadwal.kelurahan_id = form.kelurahan.data
        jadwal.kadar_min = form.minimal.data
        jadwal.kadar_max = form.maximal.data
        jadwal.jam_mulai = form.jam_mulai.data
        jadwal.jam_selesai = form.jam_selesai.data
        jadwal.user_id = current_user.id

        db.session.commit()
        flash('Jadwal berhasil diperbahrui', 'success')
        return redirect(url_for('jadwal.lihat_jadwal'))

    form.title.data = jadwal.title
    form.description.data = jadwal.description
    form.hari.data = jadwal.hari
    form.tanggal.data = jadwal.tanggal
    form.minimal.data = jadwal.kadar_min
    form.maximal.data = jadwal.kadar_max
    form.jam_mulai.data = jadwal.jam_mulai
    form.jam_selesai.data = jadwal.jam_selesai
    form.kecamatan.data = jadwal.kecamatan_id
    form.kelurahan.data = jadwal.kelurahan_id

    return render_template('jadwal/edit-jadwal.html',
                           title='Jadwal',
                           subtitle='Jadwal Penyebaran / Edit Jadwal',
                           days=days,
                           kecamatan=kecamatan,
                           form=form,
                           jadwal=jadwal)


@jadwal_bp.route('/jadwal/hapus/<int:id>', methods=['DELETE'])
@login_required
def delete_jadwal(id):
    jadwal = Jadwal.query.get_or_404(id)
    jadwal.user_id = current_user.id
    jadwal.deleted_at = datetime.now(ZoneInfo("Asia/Jakarta"))

    db.session.commit()
    return jsonify({'message': 'Jadwal berhasil dihapus'})


@jadwal_bp.route('/jadwal/notifikasi/<int:id>', methods=['GET'])
@login_required
def send_jadwal(id):
    try:
        jadwal = Jadwal.query.get_or_404(id)

        dt_mulai = datetime.combine(date.today(), jadwal.jam_mulai)
        dt_selesai = datetime.combine(date.today(), jadwal.jam_selesai)
        durasi = dt_selesai - dt_mulai
        total_menit = durasi.total_seconds() // 60
        jam = int(total_menit // 60)
        menit = int(total_menit % 60)

        ctx = {
            "title": jadwal.title,
            "tanggal": jadwal.tanggal.strftime('%d %B %Y'),
            "jam_mulai": jadwal.jam_mulai.strftime('%H:%M'),
            "durasi": f"{jam} jam {menit} menit",
            "kadar": f"{jadwal.kadar_min}% - {jadwal.kadar_max}%",
            "kecamatan": jadwal.kecamatan.name,
            "kelurahan": jadwal.kelurahan.name
        }

        email_list = (
            db.session.query(User.email)
            .join(Role, User.role_id == Role.id)
            .filter(
                Role.name == 'masyarakat',
                User.kelurahan_id == jadwal.kelurahan_id,
                User.status == 'Aktif',
                User.deleted_at == None
            )
            .with_entities(User.email)
            .all()
        )
        bcc_emails = [email[0] for email in email_list]

        send_email(
            subject=jadwal.title + " - Tim Monitoring Amonnia",
            recipients=["muhajidachmad@gmail.com"],
            template_name="emails/info.html",
            context=ctx,
            bcc=bcc_emails,
            jadwal_id=jadwal.id
        )
        flash('Notifikasi sedang dikirim', 'success')
        return redirect(url_for('jadwal.lihat_jadwal'))
    except Exception as e:
        flash('Notifikasi gagal dikirim', 'danger')
        return redirect(url_for('jadwal.lihat_jadwal'))

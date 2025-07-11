import sys
from zoneinfo import ZoneInfo

from flask import Blueprint, render_template, redirect, request, url_for, session, flash, jsonify
from flask_login import login_required, current_user

from app.forms import MasyarakatForm
from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan
from app.models.role import Role
from app.models.user import User
from app import db
import random
from datetime import datetime

masyarakat_bp = Blueprint('masyarakat', __name__)


@masyarakat_bp.route('/masyarakat')
@login_required
def lihat_masyarakat():
    search = request.args.get("search", "", type=str)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = (db.session.query(User)
             .join(Kecamatan, User.kecamatan_id == Kecamatan.id)
             .join(Kelurahan, User.kelurahan_id == Kelurahan.id)
             .join(Role, User.role_id == Role.id)
             .filter(
                Role.name == 'masyarakat',
                User.deleted_at == None
            ).order_by(User.id.desc()))

    if search:
        like = f"%{search}%"
        query = query.filter(
            Kelurahan.name.ilike(like) |
            Kecamatan.name.ilike(like) |
            User.name.ilike(like) |
            User.email.ilike(like)
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # routes.py (sebelum return render_template)
    current_page = pagination.page
    total_pages = pagination.pages

    # tampilkan range 5 halaman di sekitar current
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, current_page + 2)

    page_range = range(start_page, end_page + 1)

    return render_template('masyarakat/lihat-masyarakat.html',
                           title='Masyarakat',
                           subtitle='Masyarakat / Lihat Masyarakat',
                           pagination=pagination,
                           search=search,
                           page_range=page_range
                           )


@masyarakat_bp.route('/masyarakat/tambah', methods=['GET', 'POST'])
@login_required
def tambah_masyarakat():
    form = MasyarakatForm()

    kecamatan = Kecamatan.query.filter_by(kabupaten_id=current_user.kabupaten_id).order_by(Kecamatan.name.asc()).all()

    if form.validate_on_submit():
        code = generate_unique_kode_admin()

        role = Role.query.filter_by(name='masyarakat').first()
        if not role:
            role = Role(name='masyarakat')
            db.session.add(role)
            db.session.commit()

        user = User(
            name=form.name.data,
            email=form.email.data,
            role_id=role.id,
            kecamatan_id=form.kecamatan.data,
            kelurahan_id=form.kelurahan.data,
            kode_admin=code,
            status=form.status.data
        )

        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        flash('Masyarakat berhasil ditambahkan', 'success')
        return redirect(url_for('masyarakat.lihat_masyarakat'))

    return render_template('masyarakat/tambah-masyarakat.html',
                           title='Masyarakat',
                           subtitle='Masyarakat / Tambah Masyarakat',
                           form=form,
                           kecamatan=kecamatan,
                           )

@masyarakat_bp.route('/masyarakat/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_masyarakat(id):

    user = User.query.get_or_404(id)
    form = MasyarakatForm(obj=user)
    form.original_email = user.email

    kecamatan = Kecamatan.query.filter_by(kabupaten_id=current_user.kabupaten_id).order_by(Kecamatan.name.asc()).all()

    if form.validate_on_submit():
        user.name=form.name.data
        user.email=form.email.data
        user.kecamatan_id=form.kecamatan.data
        user.kelurahan_id=form.kelurahan.data
        user.status=form.status.data

        db.session.commit()

        flash('Masyarakat berhasil diperbahrui', 'success')
        return redirect(url_for('masyarakat.lihat_masyarakat'))

    form.name.data = user.name
    form.email.data = user.email
    form.kecamatan.data = user.kecamatan_id
    form.kelurahan.data = user.kelurahan_id
    form.status.data = user.status

    return render_template('masyarakat/edit-masyarakat.html',
                           title='Masyarakat',
                           subtitle='Masyarakat / Edit Masyarakat',
                           form=form,
                           kecamatan=kecamatan,
                           user=user,
                           )

@masyarakat_bp.route('/masyarakat/hapus/<int:id>', methods=['DELETE'])
@login_required
def delete_masyarakat(id):
    user = User.query.get_or_404(id)
    user.deleted_at = datetime.now(ZoneInfo("Asia/Jakarta"))

    db.session.commit()
    return jsonify({'message': 'Masyarakat berhasil dihapus'})


def generate_unique_kode_admin():
    while True:
        code = str(random.randint(1000, 9999))
        is_empty = User.query.filter_by(kode_admin=code).first()
        if not is_empty:
            return code

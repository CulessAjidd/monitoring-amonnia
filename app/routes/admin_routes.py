import sys

from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from flask_login import login_required, current_user

from app.forms import AdminCreateForm, AdminUpdateForm
from app.models.kabupaten import Kabupaten
from app.models.provinsi import Provinsi
from app.models.role import Role
from app.models.user import User
from app import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
def lihat_admin():
    admins = User.query.join(Role).join(Kabupaten).filter(Role.name == 'admin').order_by(User.id.desc()).all()

    return render_template('admin/daftar-admin.html',
                           title='Admin',
                           subtitle='Admin / Lihat Admin',
                           admins=admins)


@admin_bp.route('/admin/tambah', methods=['GET', 'POST'])
@login_required
def tambah_admin():
    form = AdminCreateForm()
    provinsis = Provinsi.query.order_by(Provinsi.name.asc()).all()

    if form.validate_on_submit():

        code = generate_unique_kode_admin()

        role = Role.query.filter_by(name='admin').first()
        if not role:
            role = Role(name='admin')
            db.session.add(role)
            db.session.commit()

        user = User(
            name=form.name.data,
            email=form.email.data,
            kode_admin=code,
            role_id=role.id,
            kabupaten_id=form.kabupaten.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Admin berhasil ditambahkan', 'success')
        return redirect(url_for('admin.lihat_admin'))

    return render_template('admin/tambah-admin.html',
                           title='Admin',
                           subtitle='Admin / Tambah Admin',
                           provinsis=provinsis,
                           form=form
                           )


@admin_bp.route('/admin/edit', methods=['GET', 'POST'])
@login_required
def edit_admin():
    user = User.query.get_or_404(current_user.id)
    form = AdminUpdateForm(obj=user)
    form.original_email = user.email

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        if form.password.data:
            if len(form.password.data) < 6:
                flash("Password minimal 6 karakter", "danger")
                return redirect(url_for('admin.edit_admin'))
            user.set_password(form.password.data)

        db.session.commit()

        flash('Profile berhasil diperbahrui', 'success')
        return redirect(url_for('admin.lihat_admin'))

    form.name.data = user.name
    form.email.data = user.email

    return render_template('admin/edit-admin.html',
                           title='Admin',
                           subtitle='Admin / Perbahrui Profile',
                           form=form,
                           user=user
                           )


def generate_unique_kode_admin():
    user = (db.session.query(User)
            .join(Role, User.role_id == Role.id)
            .filter(
        Role.name == 'admin',
    ).order_by(User.kode_admin.desc()).first())
    angka = int(user.kode_admin) + 1
    kode_baru = f"{angka:04d}"

    return kode_baru

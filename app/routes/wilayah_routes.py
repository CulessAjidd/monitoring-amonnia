import sys

from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_required, current_user

from app.forms import KecamatanForm, KelurahanForm
from app.models.kabupaten import Kabupaten
from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan
from app.models.provinsi import Provinsi
from app.models.user import User
from app import db

wilayah_bp = Blueprint('wilayah', __name__)


@wilayah_bp.route('/wilayah', methods=['GET'])
@login_required
def lihat_kecamatan():
    kabupatens = Kecamatan.query.filter_by(kabupaten_id=current_user.kabupaten_id).order_by(Kecamatan.name.asc()).all()
    return render_template(
        'wilayah/lihat-kecamatan.html',
        title='Wilayah',
        subtitle='Wilayah / Kabupaten',
        wilayahs=kabupatens,
    )


@wilayah_bp.route('/wilayah/kelurahan/<int:id>', methods=['GET'])
@login_required
def lihat_kelurahan(id):
    kelurahans = Kelurahan.query.filter_by(kecamatan_id=id).order_by(Kelurahan.name.asc()).all()
    return render_template(
        'wilayah/lihat-kelurahan.html',
        title='Wilayah',
        subtitle='Wilayah / Kalurahan',
        wilayahs=kelurahans,
        kecamatan_id=id
    )


@wilayah_bp.route('/wilayah/tambah-kecamatan', methods=['GET', 'POST'])
@login_required
def tambah_kecamatan():
    form = KecamatanForm()
    if form.validate_on_submit():
        kecamatan_last = (Kecamatan.query.filter_by(kabupaten_id=current_user.kabupaten_id)
                          .order_by(Kecamatan.kode.desc())
                          .first())

        if kecamatan_last:
            bagian = kecamatan_last.kode.split(".")
            bagian[-1] = str(int(bagian[-1]) + 1)
            kode_baru = ".".join(bagian)
        else:
            kecamatan_kode = current_user.kabupaten.kode
            kode_baru = f"{kecamatan_kode}.01"

        kecamatan = Kecamatan(
            name=form.name.data,
            kabupaten_id=current_user.kabupaten_id,
            kode=kode_baru,
        )
        db.session.add(kecamatan)
        db.session.commit()

        flash('Kecamatan berhasil ditambahkan', 'success')
        return redirect(url_for('wilayah.lihat_kecamatan'))

    return render_template('wilayah/tambah-kecamatan.html',
                           title='Wilayah',
                           subtitle='Wilayah / Tambah Kecamatan',
                           form=form,
                           )
@wilayah_bp.route('/wilayah/edit-kecamatan/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_kecamatan(id):

    kecamatan = Kecamatan.query.get_or_404(id)
    form = KecamatanForm(obj=kecamatan)

    if form.validate_on_submit():
        kecamatan.name=form.name.data
        db.session.commit()

        flash('Kecamatan berhasil diperbahrui', 'success')
        return redirect(url_for('wilayah.lihat_kecamatan'))

    form.name.data = kecamatan.name

    return render_template('wilayah/edit-kecamatan.html',
                           title='Wilayah',
                           subtitle='Wilayah / Edit Kecamatan',
                           form=form,
                           kecamatan=kecamatan
                           )

@wilayah_bp.route('/wilayah/tambah-kelurahan/<int:kecamatan_id>', methods=['GET', 'POST'])
@login_required
def tambah_kelurahan(kecamatan_id):

    kecamatan = Kecamatan.query.get_or_404(kecamatan_id)
    form = KelurahanForm()
    if form.validate_on_submit():
        kelurahan_last = (Kelurahan.query.filter_by(kecamatan_id=form.kecamatan_id.data)
                          .order_by(Kelurahan.kode.desc())
                          .first())

        if kelurahan_last:
            bagian = kelurahan_last.kode.split(".")
            bagian[-1] = str(int(bagian[-1]) + 1)
            kode_baru = ".".join(bagian)
        else:
            kelurahan_kode = kecamatan.kode
            kode_baru = f"{kelurahan_kode}.01"

        kelurahan = Kelurahan(
            name=form.name.data,
            kecamatan_id=form.kecamatan_id.data,
            kode=kode_baru,
        )
        db.session.add(kelurahan)
        db.session.commit()

        flash('Kelurahan berhasil ditambahkan', 'success')
        return redirect(url_for('wilayah.lihat_kelurahan', id=kecamatan.id))

    form.kecamatan_id.data = kecamatan.id

    return render_template('wilayah/tambah-kelurahan.html',
                           title='Wilayah',
                           subtitle='Wilayah / Tambah Kelurahan',
                           form=form,
                           kecamatan=kecamatan
                           )

@wilayah_bp.route('/wilayah/edit-kelurahan/<int:kelurahan_id>', methods=['GET', 'POST'])
@login_required
def edit_kelurahan(kelurahan_id):

    kelurahan = Kelurahan.query.get_or_404(kelurahan_id)
    form = KelurahanForm(obj=kelurahan)

    if form.validate_on_submit():
        kelurahan.name=form.name.data
        db.session.commit()

        flash('Kelurahan berhasil diperbahrui', 'success')
        return redirect(url_for('wilayah.lihat_kelurahan', id=kelurahan.kecamatan_id))

    form.kecamatan_id.data = kelurahan.kecamatan_id
    form.name.data = kelurahan.name

    return render_template('wilayah/edit-kelurahan.html',
                           title='Wilayah',
                           subtitle='Wilayah / Edit Kelurahan',
                           form=form,
                           kelurahan=kelurahan
                           )

@wilayah_bp.route('/ajax/kelurahan/<int:kecamatan_id>', methods=['GET'])
@login_required
def get_ajax_kelurahan(kecamatan_id):
    kelurahan = Kelurahan.query.filter_by(kecamatan_id=kecamatan_id).order_by(Kelurahan.name.asc()).all()
    result = [{"id": k.id, "name": k.name} for k in kelurahan]

    return jsonify(kelurahan=result)

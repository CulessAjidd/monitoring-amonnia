import sys

from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify

from app.models.kabupaten import Kabupaten
from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan
from app.models.provinsi import Provinsi
from app.models.user import User
from app import db

wilayah_bp = Blueprint('wilayah', __name__)

@wilayah_bp.route('/wilayah/provinsi', methods=['GET'])
def lihat_provinsi():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])

    search = request.args.get("search", "", type=str)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = (((db.session.query(Kelurahan, Kecamatan, Kabupaten, Provinsi)
             .join(Kecamatan, Kelurahan.kecamatan_id == Kecamatan.id))
             .join(Kabupaten, Kecamatan.kabupaten_id == Kabupaten.id))
             .join(Provinsi, Kabupaten.provinsi_id == Provinsi.id))

    if search:
        like = f"%{search}%"
        query = query.filter(
            Kelurahan.name.ilike(like) |
            Kecamatan.name.ilike(like) |
            Kabupaten.name.ilike(like) |
            Provinsi.name.ilike(like)
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # routes.py (sebelum return render_template)
    current_page = pagination.page
    total_pages = pagination.pages

    # tampilkan range 5 halaman di sekitar current
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, current_page + 2)

    page_range = range(start_page, end_page + 1)

    return render_template('wilayah/lihat-wilayah.html',
                           title='Wilayah',
                           subtitle='Wilayah / Provinsi',
                           pagination=pagination,
                           search=search,
                           page_range=page_range
                           )

@wilayah_bp.route('/ajax/kelurahan/<int:kecamatan_id>', methods=['GET'])
def get_ajax_kelurahan(kecamatan_id):
    kelurahan = Kelurahan.query.filter_by(kecamatan_id=kecamatan_id).order_by(Kelurahan.name.asc()).all()
    result = [{"id": k.id, "name": k.name} for k in kelurahan]

    return jsonify(kelurahan=result)


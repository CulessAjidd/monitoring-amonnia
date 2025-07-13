import sys
from datetime import datetime, date
from io import BytesIO

import pandas as pd
from flask import Blueprint, render_template, redirect, request, url_for, session, send_file
from flask_login import login_required

from app.models.jadwal import Jadwal
from app.models.kabupaten import Kabupaten
from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan
from app.models.provinsi import Provinsi
from app.models.user import User
from app import db

laporan_bp = Blueprint('laporan', __name__)


@laporan_bp.route('/', methods=['GET'])
@login_required
def laporan():
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
            "status_kadar": jadwal.status_kadar,
        })

    return render_template('laporan/laporan.html',
                           title='Laporan',
                           subtitle='Laporan Penyebaran',
                           pagination=pagination,
                           search=search,
                           page_range=page_range,
                           results=results
                           )


@laporan_bp.route('/jadwal/export-excel')
@login_required
def export_jadwal_excel():
    search = request.args.get("search", "", type=str)

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

    jadwals = query.all()

    rows = []
    for jadwal in jadwals:
        dt_mulai = datetime.combine(date.today(), jadwal.jam_mulai)
        dt_selesai = datetime.combine(date.today(), jadwal.jam_selesai)
        durasi = dt_selesai - dt_mulai
        total_menit = durasi.total_seconds() // 60
        jam = int(total_menit // 60)
        menit = int(total_menit % 60)

        rows.append({
            "Tanggal": jadwal.tanggal.strftime("%Y-%m-%d"),
            "Kecamatan": jadwal.kecamatan.name,
            "Kelurahan": jadwal.kelurahan.name,
            "Jam Mulai": jadwal.jam_mulai.strftime("%H:%M"),
            "Jam Selesai": jadwal.jam_selesai.strftime("%H:%M"),
            "Durasi": f"{jam} jam {menit} menit",
            "Kadar Min": f"{jadwal.kadar_min}%",
            "Kadar Max": f"{jadwal.kadar_max}%",
            "Status Kadar": jadwal.status_kadar
        })

    df = pd.DataFrame(rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Jadwal')

        worksheet = writer.sheets['Jadwal']

        column_widths = {
            'A': 12,  # Tanggal
            'B': 30,  # Kecamatan
            'C': 30,  # Kelurahan
            'D': 10,  # Jam Mulai
            'E': 10,  # Jam Selesai
            'F': 20,  # Durasi
            'G': 12,  # Kadar Min
            'H': 12,  # Kadar Max
            'I': 15,  # Status
            'J': 18,  # Status Kadar
        }

        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width

    output.seek(0)

    return send_file(
        output,
        download_name=f"jadwal_amonia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

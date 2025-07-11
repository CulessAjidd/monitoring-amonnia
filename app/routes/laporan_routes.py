import sys

from flask import Blueprint, render_template, redirect, request, url_for, session

from app.models.kabupaten import Kabupaten
from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan
from app.models.provinsi import Provinsi
from app.models.user import User
from app import db

laporan_bp = Blueprint('laporan', __name__)

@laporan_bp.route('/laporan', methods=['GET'])
def laporan():

    return render_template('laporan/laporan.html',
                           title='Laporan',
                           subtitle='Laporan Penyebaran',
                           )


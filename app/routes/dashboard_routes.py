import sys

from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_login import login_required

from app.models.kabupaten import Kabupaten
from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan
from app.models.provinsi import Provinsi
from app.models.user import User
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')


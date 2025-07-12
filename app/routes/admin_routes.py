import sys

from flask import Blueprint, render_template, redirect, request, url_for, session
from flask_login import login_required

from app.models.kabupaten import Kabupaten
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

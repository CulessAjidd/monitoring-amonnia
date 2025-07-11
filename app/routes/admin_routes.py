import sys

from flask import Blueprint, render_template, redirect, request, url_for, session

from app.models.kabupaten import Kabupaten
from app.models.role import Role
from app.models.user import User
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def lihat_admin():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])

    admins = User.query.join(Role).join(Kabupaten).filter(Role.name == 'admin').order_by(User.id.desc()).all()

    return render_template('admin/daftar-admin.html', admins=admins)

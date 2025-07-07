import sys

from flask import Blueprint, render_template, redirect, request, url_for, session

from app.models.role import Role
from app.models.user import User
from app import db

wilayah_bp = Blueprint('wilayah', __name__)

@wilayah_bp.route('/wilayah')
def lihat_wilayah():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])
    return render_template('wilayah/lihat-wilayah.html')


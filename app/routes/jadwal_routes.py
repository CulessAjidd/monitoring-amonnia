import sys

from flask import Blueprint, render_template, redirect, request, url_for, session

from app.models.role import Role
from app.models.user import User
from app import db

jadwal_bp = Blueprint('jadwal', __name__)

@jadwal_bp.route('/jadwal')
def lihat_jadwal():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])
    return render_template('jadwal/lihat-jadwal.html')


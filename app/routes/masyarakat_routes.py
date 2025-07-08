import sys

from flask import Blueprint, render_template, redirect, request, url_for, session

from app.models.role import Role
from app.models.user import User
from app import db

masyarakat_bp = Blueprint('masyarakat', __name__)

@masyarakat_bp.route('/masyarakat')
def lihat_masyarakat():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])
    return render_template('masyarakat/lihat-masyarakat.html')


import sys

from flask import Blueprint, render_template, redirect, request, url_for, session

from app.models.role import Role
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('auth.dashboard'))
        return "Login gagal", 401
    return render_template('auth/login.html')

@auth_bp.route('/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect(url_for('auth.login'))
    # user = User.query.get(session['user_id'])
    return render_template('dashboard/dashboard.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

# optional: untuk membuat user admin
@auth_bp.route('/create-admin')
def create_admin():
    role = Role.query.filter_by(name='admin').first()
    if not role:
        role = Role(name='admin')
        db.session.add(role)
        db.session.commit()

    user = User.query.filter_by(username='admin').first()
    if not user:
        user = User(username='admin', role_id=role.id)
        user.set_password('1234')
        db.session.add(user)
        db.session.commit()

    return "User admin berhasil dibuat!"

from flask_login import UserMixin

from app import db
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    kode_admin = db.Column(db.String(50), unique=True, nullable=False)
    kabupaten_id = db.Column(db.Integer, db.ForeignKey('kabupaten.id'), nullable=True)
    kecamatan_id = db.Column(db.Integer, db.ForeignKey('kecamatan.id'), nullable=True)
    kelurahan_id = db.Column(db.Integer, db.ForeignKey('kelurahan.id'), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Aktif')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Jakarta")))
    deleted_at = db.Column(db.DateTime, nullable=True)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    kabupaten = db.relationship('Kabupaten', backref='user')
    kecamatan = db.relationship('Kecamatan', backref='user')
    kelurahan = db.relationship('Kelurahan', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def soft_delete(self):
        self.deleted_at = datetime.now(ZoneInfo("Asia/Jakarta"))
        db.session.commit()

    @staticmethod
    def get_all_active():
        return User.query.filter_by(deleted_at=None).all()

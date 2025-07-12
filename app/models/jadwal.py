from flask_login import UserMixin

from app import db
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.kecamatan import Kecamatan
from app.models.kelurahan import Kelurahan


class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    hari = db.Column(db.String(50), unique=True, nullable=False)
    tanggal = db.Column(db.Date, nullable=True)
    jam_mulai = db.Column(db.Time, nullable=True)
    jam_selesai = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kecamatan_id = db.Column(db.Integer, db.ForeignKey('kecamatan.id'), nullable=False)
    kelurahan_id = db.Column(db.Integer, db.ForeignKey('kelurahan.id'), nullable=False)
    kadar_min = db.Column(db.Integer, nullable=False)
    kadar_max = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Jakarta")))
    deleted_at = db.Column(db.DateTime, nullable=True)

    kecamatan = db.relationship("Kecamatan", backref="jadwal_list")
    kelurahan = db.relationship("Kelurahan", backref="jadwal_list")

    def soft_delete(self):
        self.deleted_at = datetime.now(ZoneInfo("Asia/Jakarta"))
        db.session.commit()

    @staticmethod
    def get_all_active():
        return (Jadwal.query
                .join(Kecamatan)
                .join(Kelurahan)
                .filter_by(deleted_at=None).all())

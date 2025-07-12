from zoneinfo import ZoneInfo

from app import db
from datetime import datetime

class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kabupaten_id = db.Column(db.Integer, db.ForeignKey('kabupaten.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    kode = db.Column(db.String(30), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    kelurahans = db.relationship('Kelurahan', backref='kecamatan', lazy=True)

    def soft_delete(self):
        self.deleted_at = datetime.now(ZoneInfo("Asia/Jakarta"))
        db.session.commit()

    @staticmethod
    def get_all_active():
        return Kecamatan.query.filter_by(deleted_at=None).all()

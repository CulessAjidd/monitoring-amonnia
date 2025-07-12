from zoneinfo import ZoneInfo

from app import db
from datetime import datetime

class Kabupaten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provinsi_id = db.Column(db.Integer, db.ForeignKey('provinsi.id'), nullable=False)
    kode = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    kecamatans = db.relationship('Kecamatan', backref='kabupaten', lazy=True)

    def soft_delete(self):
        self.deleted_at = datetime.now(ZoneInfo("Asia/Jakarta"))
        db.session.commit()

    @staticmethod
    def get_all_active():
        return Kabupaten.query.filter_by(deleted_at=None).all()

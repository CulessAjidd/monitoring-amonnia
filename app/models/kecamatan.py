from app import db

class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kabupaten_id = db.Column(db.Integer, db.ForeignKey('kabupaten.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    kode = db.Column(db.String(30), nullable=False)

    kelurahans = db.relationship('Kelurahan', backref='kecamatan', lazy=True)

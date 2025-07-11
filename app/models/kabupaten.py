from app import db

class Kabupaten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provinsi_id = db.Column(db.Integer, db.ForeignKey('provinsi.id'), nullable=False)
    kode = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    kecamatans = db.relationship('Kecamatan', backref='kabupaten', lazy=True)

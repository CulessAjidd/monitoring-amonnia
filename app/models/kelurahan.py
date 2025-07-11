from app import db

class Kelurahan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kecamatan_id = db.Column(db.Integer, db.ForeignKey('kecamatan.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    kode = db.Column(db.String(30), nullable=False)

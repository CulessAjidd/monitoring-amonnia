from app import db

class Provinsi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    kabupatens = db.relationship('Kabupaten', backref='provinsi', lazy=True)
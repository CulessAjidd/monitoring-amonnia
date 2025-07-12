from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Email, Length
from datetime import datetime, date

from app.models.user import User


class JadwalForm(FlaskForm):
    hari = StringField('Hari', validators=[DataRequired(message='Hari harus dipilih')])
    tanggal = DateField('Tanggal',
                        format='%Y-%m-%d',
                        validators=[DataRequired(message='Tanggal harus diisi')])
    jam_mulai = TimeField('Jam Mulai',
                        format='%H:%M',
                        validators=[DataRequired(message='Jam mulai harus diisi')])
    jam_selesai = TimeField('Jam Selesai',
                          format='%H:%M',
                          validators=[DataRequired(message='Jam selesai harus diisi')])
    kecamatan = StringField('Kecamatan',
                            validators=[DataRequired(message='Kecamatan harus diisi')])
    kelurahan = StringField('Kelurahan',
                            validators=[DataRequired(message='Kelurahan harus diisi')])
    minimal = IntegerField('Minimal Kadar',
                            validators=[DataRequired(message='Minimal kadar harus diisi')])
    maximal = IntegerField('Maximal Kadar',
                            validators=[DataRequired(message='Maximal kadar harus diisi')])
    title = StringField('Title', validators=[DataRequired(message='Judul notifikasi harus diisi')])
    description = StringField('Description', validators=[DataRequired(message='Deskripsi notifikasi harus diisi')])

    submit = SubmitField('Tambah')

    def validate_tanggal(self, field):
        if field.data < date.today():
            raise ValidationError('Tanggal tidak boleh di masa lalu.')

    def validate_maximal(self, field):
        if self.minimal.data is not None and field.data is not None:
            if field.data <= self.minimal.data:
                raise ValidationError("Maksimal kadar harus lebih besar dari Minimal kadar.")

    def validate_jam_selesai(self, field):
        if self.jam_mulai.data and field.data:
            if field.data <= self.jam_mulai.data:
                raise ValidationError('Jam selesai harus lebih besar dari jam mulai.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email wajib diisi"),
        Email(message="Format email tidak valid"),
        Length(max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password wajib diisi"),
        Length(min=6, max=100, message="Password minimal 6 karakter")
    ])
    submit = SubmitField('Login')

class KecamatanForm(FlaskForm):
    name = StringField('Nama Kecamatan',
                            validators=[DataRequired(message='Kecamatan harus diisi')])

class KelurahanForm(FlaskForm):
    kecamatan_id = StringField('ID Kecamatan',
                                 validators=[DataRequired(message='Kecamatan harus diisi')])
    name = StringField('Nama Kelurahan',
                       validators=[DataRequired(message='Kelurahan harus diisi')])

class MasyarakatForm(FlaskForm):
    original_email = None

    kecamatan = StringField('Kecamatan',
                            validators=[DataRequired(message='Kecamatan harus diisi')])
    kelurahan = StringField('Kelurahan',
                            validators=[DataRequired(message='Kelurahan harus diisi')])
    status = StringField('Status',
                            validators=[DataRequired(message='Status harus diisi')])
    email = StringField('Email', validators=[
        DataRequired(message="Email wajib diisi"),
        Email(message="Format email tidak valid"),
        Length(max=100)
    ])
    name = StringField('Nama', validators=[DataRequired(message='Nama harus diisi')])

    submit = SubmitField('Tambah')

    def validate_email(self, field):
        if field.data != self.original_email:
            user = User.query.filter(
                User.email == field.data,
                User.deleted_at == None
            ).first()
            if user:
                raise ValidationError('Email sudah digunakan.')
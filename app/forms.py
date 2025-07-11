from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Email, Length


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

    submit = SubmitField('Tambah')

    def validate_maximal(self, field):
        if self.minimal.data is not None and field.data is not None:
            if field.data <= self.minimal.data:
                raise ValidationError("Maksimal kadar harus lebih besar dari Minimal kadar.")


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
import threading
from flask import render_template, current_app
from flask_mail import Message
from app.extensions import mail, db
from app.models.jadwal import Jadwal


def send_async_email(app, msg, jadwal_id=None):
    with app.app_context():
        try:
            mail.send(msg)
            app.logger.info("Email berhasil dikirim ke: %s", msg.recipients)
            if jadwal_id:
                jadwal = Jadwal.query.get(jadwal_id)
                if jadwal:
                    jadwal.status = "Terkirim"
                    db.session.commit()
        except Exception as e:
            app.logger.error("Gagal mengirim email: %s", str(e))

def send_email(subject, recipients, template_name=None, context=None, body=None, bcc=None, jadwal_id=None):
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        recipients=recipients,
        bcc=bcc
    )

    if template_name:
        msg.html = render_template(template_name, **(context or {}))
    elif body:
        msg.body = body
    else:
        msg.body = "Isi kosong"

    thread = threading.Thread(target=send_async_email, args=(app, msg, jadwal_id))
    thread.start()
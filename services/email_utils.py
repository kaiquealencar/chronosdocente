from flask_mail import Message
from flask import current_app,url_for, render_template_string, render_template
from itsdangerous import URLSafeTimedSerializer
from extensions import mail


def send_confirmation_email(user_email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(user_email, salt='email-confirm')

    confirm_url = url_for('confirm_email', token=token, _external=True)

    html_body = render_template('emails/confirm-email.html', link_confirmacao=confirm_url)

    msg = Message(
        'Confirme seu e-mail - Chronos Docente',
        recipients=[user_email],
        html=html_body,
        sender=('ChronosDocente', 'noreply@chronosdocente.com.br')
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Erro ao enviar o email {e}')
        return False
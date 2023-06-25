
import smtplib
from email.mime.text import MIMEText
from core.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT
from resume.models import EmailSend

sender = EMAIL_HOST_USER
password = EMAIL_HOST_PASSWORD


def send_email_my(massage=None, to_send=None, name=None, host=None, subject=None, session_id=None):
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    print('send_email_my')
    # Шифорванный обмен
    server.starttls()

    if not massage:
        massage = f'{name}, ссылка на мое резюме {"http://" + host}'
    msg = MIMEText(massage)
    if not subject:
        msg['Subject'] = 'Автоматическое сообщение в демонстрационных целях'
    else:
        msg['Subject'] = subject
    try:
        server.login(sender, password)
        msg['To'] = to_send
        msg['From'] = sender
        server.sendmail(sender, to_send, msg.as_string())
        EmailSend.objects.get_or_create(
            email=to_send,
            defaults={'name': name}
        )
        return 'Your massage was send successfully!'
    except Exception as error:
        return f"{error} "

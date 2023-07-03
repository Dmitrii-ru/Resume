import smtplib
from email.mime.text import MIMEText
from core.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT, ALLOWED_HOSTS
from resume.models import EmailSend

sender = EMAIL_HOST_USER
password = EMAIL_HOST_PASSWORD


def send_email_my(massage_num, to_send, name, subject):
    try:

        if ALLOWED_HOSTS:
            host = "http://" + ALLOWED_HOSTS[0]
        else:
            host = 'http://127.0.0.1:8000/'

        dict_massages = {
            1: f'{name}, ссылка на мое резюме {host}',
            2: f'{name}, жду от Вас положительно ответа,мое резюме {host}',
        }

        dict_subjects = {
            1: 'Автоматическое сообщение в демонстрационных целях',
            2: 'Непомнине от соискателя'
        }

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)

        # Шифорванный обмен
        server.starttls()

        msg = MIMEText(dict_massages[massage_num])
        msg['To'] = to_send
        msg['From'] = sender
        msg['Subject'] = dict_subjects[subject]

        server.login(sender, password)
        server.sendmail(sender, to_send, msg.as_string())
        EmailSend.objects.get_or_create(
            email=to_send,
            defaults={'name': name}
        )
        print('send_email_my: GOOD')
        return 'Your massage was send successfully!'

    except Exception as error:
        return f"{error} "

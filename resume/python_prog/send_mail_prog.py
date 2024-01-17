import smtplib
from email.mime.text import MIMEText
from core.settings import ALLOWED_HOSTS
from resume.models import EmailSend
from resume.models import EmailSettings


def send_email_my(massage_num, to_send, name, subject):
    is_active_email = EmailSettings.objects.filter(is_active='True').first()
    if is_active_email:
        sender = is_active_email.name_email
        password = is_active_email.password_email
        email_host = is_active_email.host_email
        post = is_active_email.port_email
        print('sens_mail')
        try:
            if ALLOWED_HOSTS:
                host = "http://" + ALLOWED_HOSTS[1]

            else:
                host = 'http://127.0.0.1:8000/'

            dict_massages = {
                1: f'{name}, ссылка на мое резюме {host}',
                2: f'{name}, жду от Вас feedback, мое резюме {host}',
            }

            dict_subjects = {
                1: 'Ссылка на резюме соискателя, данное сообщение сформировано автоматически',
                2: 'Непомнине от соискателя, данное сообщение сформировано автоматически'
            }

            server = smtplib.SMTP(email_host, post)

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
            return 'Your massage was send successfully!'
        except Exception as error:
            return f"{error} "
    else:
        return ValueError('Отправка письма не доступна')
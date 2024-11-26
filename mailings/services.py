from django.core.mail import send_mail
from .models import Mailing, MailingAttempt
from django.utils import timezone


def send_mailing(mailing):
    for recipient in mailing.recipients.all():
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                'lacryk@yandex.ru',
                [recipient.email],
            )
            status = 'Успешно'
            response = 'Message sent successfully.'
        except Exception as e:
            status = 'Не успешно'
            response = str(e)

        # Создаем запись попытки отправки
        MailingAttempt.objects.create(
            mailing=mailing,
            recipient=recipient,
            status=status,
            response=response
        )
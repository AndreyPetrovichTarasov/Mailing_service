from django.db import models
from django.utils import timezone
from clients.models import Client
from messages_list.models import Message


class Mailing(models.Model):
    objects: models.Manager = models.Manager()
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Client)

    def __str__(self):
        return f'Рассылка {self.id} ({self.status})'


class MailingAttempt(models.Model):
    objects: models.Manager = models.Manager()
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response = models.TextField()

    def __str__(self):
        return f'Попытка {self.id} для рассылки {self.mailing.id}'

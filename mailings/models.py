from tkinter.constants import CASCADE

from django.db import models


class MailingRecipient(models.Model):
    email = models.CharField(unique=True, max_length=100, verbose_name='Email')
    personal_details = models.CharField(max_length=100, verbose_name='ФИО')
    commentary = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ['email']


class EmailMessage(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return 'Сообщение клиенту'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    CREATED = 'created'
    SENT = 'sent'
    CLOSED = 'closed'

    MAILING_STATUS_CHOICES = [
    (CREATED, 'Создана'),
    (SENT, 'Запущена'),
    (CLOSED, 'Завершена'),
    ]

    first_sending = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время первой отправки')
    close_sending = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=9, choices=MAILING_STATUS_CHOICES, verbose_name='Статус')
    message = models.ForeignKey(EmailMessage, on_delete=models.CASCADE, related_name='messages', verbose_name='сообщение')
    recipient = models.ManyToManyField(MailingRecipient, related_name='recipients', verbose_name='получатели')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Рассылка сообщения'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['created_at']

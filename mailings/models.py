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
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'Сообщение № {self.pk}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    CREATED = 'Создана'
    SENT = 'Запущена'
    CLOSED = 'Завершена'

    MAILING_STATUS_CHOICES = [
    (CREATED, 'Создана'),
    (SENT, 'Запущена'),
    (CLOSED, 'Завершена'),
    ]

    first_sending = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время первой отправки')
    close_sending = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=9, choices=MAILING_STATUS_CHOICES, verbose_name='Статус')
    message = models.ForeignKey(EmailMessage, on_delete=models.CASCADE, related_name='messages', verbose_name='сообщение')
    recipient = models.ManyToManyField(MailingRecipient, related_name='recipients', verbose_name='получатель')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_related_fields(self):
        return ', '.join([str(related) for related in self.recipient.all()])

    def __str__(self):
        return 'Рассылка сообщения'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['created_at']


class MailingAttempt(models.Model):
    SUCCESSFUL = 'Успешно'
    UNSUCCESSFUL = 'Не успешно'

    MAILING_ATTEMPT_STATUS_CHOICES = [
    (SUCCESSFUL, 'Успешно'),
    (UNSUCCESSFUL, 'Не успешно'),
    ]

    date_time_of_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=MAILING_ATTEMPT_STATUS_CHOICES, verbose_name='Статус')
    server_reply = models.TextField(verbose_name="Ответ почтового сервера", blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailings', verbose_name='рассылка')

    def __str__(self):
        return 'Попытка рассылки'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['date_time_of_attempt']

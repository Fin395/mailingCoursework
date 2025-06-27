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

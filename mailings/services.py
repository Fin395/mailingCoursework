from django.utils import timezone

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt, MailingRecipient


class MailingService:

    @staticmethod
    def send_mailing(pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing_recipients = mailing.get_related_fields().split(', ')
        if mailing.status != 'Завершена':
            for recipient in mailing_recipients:
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient],
                        fail_silently=False)
                    if mailing.status == 'Создана':
                        mailing.status = 'Запущена'
                        mailing.first_sending = timezone.now()
                    attempt_status = MailingAttempt.SUCCESSFUL
                    server_reply = ''
                except Exception as e:
                    server_reply_for_attempt = e
                    attempt_status = MailingAttempt.UNSUCCESSFUL
                    server_reply = server_reply_for_attempt

                MailingAttempt.objects.create(date_time_of_attempt=timezone.now(), status=attempt_status,
                                                     server_reply=server_reply,
                                                     mailing=mailing)
        mailing.save()

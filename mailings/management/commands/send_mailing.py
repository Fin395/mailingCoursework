from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Send mailing'

    def handle(self, *args, **kwargs):
        filtered_mailings = Mailing.objects.filter(status='Создана')
        for mailing in filtered_mailings:
            mailing_recipients = mailing.get_related_fields().split(', ')
            for recipient in mailing_recipients:
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient],
                        fail_silently=False)
                    mailing.status = 'Запущена'
                    mailing.first_sending = timezone.now()
                    attempt_status = MailingAttempt.SUCCESSFUL
                    server_reply = ''
                    self.stdout.write(self.style.SUCCESS('Mailing sent'))
                except Exception as e:
                    server_reply_for_attempt = e
                    attempt_status = MailingAttempt.UNSUCCESSFUL
                    server_reply = server_reply_for_attempt
                    self.stdout.write(self.style.ERROR(f'Failed mailing: {server_reply}'))

                MailingAttempt.objects.create(date_time_of_attempt=timezone.now(), status=attempt_status,
                                              server_reply=server_reply,
                                              mailing=mailing)
            mailing.save()

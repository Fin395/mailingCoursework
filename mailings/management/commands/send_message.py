from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import EmailMessage, MailingRecipient, Mailing


class Command(BaseCommand):
    help = 'Send message'

    def handle(self, *args, **kwargs):
        messages = EmailMessage.objects.filter(is_sent=False)
        for message in messages:
            filtered_mailings = Mailing.objects.filter(message=message)
            for mailing in filtered_mailings:
                    send_mail(
                    subject=message.subject,
                    message=message.body,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=mailing.get_related_fields().split(', '),
                    fail_silently=False)

            message.is_sent = True
            message.save()
            self.stdout.write(self.style.SUCCESS(f'Sent: {message.subject}'))

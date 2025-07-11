from django.contrib import admin
from .models import MailingRecipient, EmailMessage, Mailing, MailingAttempt


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'personal_details', 'commentary')
    search_fields = ('email', 'personal_details',)


@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'body')
    search_fields = ('subject', 'body')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_sending', 'close_sending', 'status', 'message', 'get_related_fields', 'created_at')
    search_fields = ('message', 'recipient')
    list_filter = ('status', 'recipient',)

    def get_related_fields(self, obj):
        return ', '.join([str(related) for related in obj.recipient.all()])

    get_related_fields.short_description = 'Получатель'


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_time_of_attempt', 'status', 'server_reply', 'mailing')

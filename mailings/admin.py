from django.contrib import admin
from .models import MailingRecipient, EmailMessage


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'personal_details', 'commentary')
    search_fields = ('email', 'personal_details',)


@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'body')
    search_fields = ('subject', 'body')

from django.contrib import admin
from .models import MailingRecipient

@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'personal_details', 'commentary')
    search_fields = ('email', 'personal_details',)


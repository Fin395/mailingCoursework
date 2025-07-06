from django import forms

from mailings.mixins import StyleFormMixin
from mailings.models import MailingRecipient, EmailMessage, Mailing, MailingAttempt


# from .models import Product
# from django.core.exceptions import ValidationError


# FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class MailingRecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['email', 'personal_details', 'commentary']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        personal_details = cleaned_data.get('personal_details')

        if email and personal_details and "spam" in personal_details:
            self.add_error('personal_details', 'personal_details не может содержать слово "spam"')


class EmailMessageForm(StyleFormMixin, forms.ModelForm):   # добавить StyleFormMixin
    class Meta:
        model = EmailMessage
        fields = ['subject', 'body']

        def clean(self):
            cleaned_data = super().clean()
            subject = cleaned_data.get('subject')
            body = cleaned_data.get('body')

            if subject and body and "spam" in subject:
                self.add_error('subject', 'subject не может содержать слово "spam"')


class MailingForm(StyleFormMixin, forms.ModelForm):   # добавить StyleFormMixin
    class Meta:
        model = Mailing
        fields = ['status', 'message', 'recipient']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = MailingRecipient.objects.filter(owner=user)

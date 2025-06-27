from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse_lazy
from mailings.forms import MailingRecipientForm, EmailMessageForm
from mailings.models import MailingRecipient, EmailMessage


class MainPageView(TemplateView):
    template_name = 'mailings/main_page.html'


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailingrecipient_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailingrecipient_detail', kwargs={'pk': self.object.pk})


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailings/mailingrecipient_detail.html'


class MailingRecipientListView(ListView):
    model = MailingRecipient
    template_name = 'mailings/mailingrecipient_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['recipients'] = MailingRecipient.objects.all()
        return context


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailingrecipient_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailingrecipient_detail', kwargs={'pk': self.object.pk})


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    success_url = reverse_lazy('mailings:mailingrecipient_list')
    template_name = 'mailings/mailingrecipient_confirm_delete.html'


class EmailMessageCreateView(CreateView):
    model = EmailMessage
    form_class = EmailMessageForm
    template_name = 'mailings/emailmessage_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:emailmessage_detail', kwargs={'pk': self.object.pk})


class EmailMessageDetailView(DetailView):
    model = EmailMessage
    template_name = 'mailings/emailmessage_detail.html'


class EmailMessageListView(ListView):
    model = EmailMessage
    template_name = 'mailings/emailmessage_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['messages'] = EmailMessage.objects.all()
        return context


class EmailMessageUpdateView(UpdateView):
    model = EmailMessage
    form_class = EmailMessageForm
    template_name = 'mailings/emailmessage_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:emailmessage_detail', kwargs={'pk': self.object.pk})


class EmailMessageDeleteView(DeleteView):
    model = EmailMessage
    success_url = reverse_lazy('mailings:emailmessage_list')
    template_name = 'mailings/emailmessage_confirm_delete.html'

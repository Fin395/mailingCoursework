from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse_lazy
from mailings.forms import MailingRecipientForm
from mailings.models import MailingRecipient


class MainPageView(TemplateView):
    template_name = 'mailings/main_page.html'


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailingrecipient_detail', kwargs={'pk': self.object.pk})


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient


class MailingRecipientListView(ListView):
    model = MailingRecipient


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailingrecipient_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailingrecipient_detail', kwargs={'pk': self.object.pk})


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    success_url = reverse_lazy('mailings:mailingrecipient_list')
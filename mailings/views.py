from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from config.settings import EMAIL_HOST_USER
from mailings.forms import MailingRecipientForm, EmailMessageForm, MailingForm
from mailings.models import MailingRecipient, EmailMessage, Mailing
from django.core.mail import send_mail


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


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['mailings'] = Mailing.objects.all()
        return context


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['mailings'] = Mailing.objects.all()
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')
    template_name = 'mailings/mailing_confirm_delete.html'


class SendMailingView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.status == 'Создана':
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[mailing.get_related_fields()])

            mailing.status = 'Запущена'
            mailing.save()

        return redirect('mailings:mailing_detail', pk=pk)
        # if not request.user.has_perm('library.can_review_book'):
        #     return HttpResponseForbidden('У вас нет прав для рецензирования книги.')

        # Логика рецензирования книги
        # book.review = request.POST.get('review')
        # book.save()
        #
        # return redirect('library:book_details', pk=pk)



# from django.urls import reverse_lazy
# from django.views.generic.edit import CreateView
#
# from config.settings import EMAIL_HOST_USER
# from .forms import CustomUserRegistrationForm
# from django.core.mail import send_mail
# from django.contrib.auth import login
#
#
#
# class EmailMessageSendingView(CreateView):
#     form_class = CustomUserRegistrationForm
#     template_name = 'users/register.html'
#     success_url = reverse_lazy('users:login')
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         send_mail(
#             subject='Добро пожаловать в наш сервис',
#             message='Спасибо, что зарегистрировались в нашем сервисе!',
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[user.email]
#         )
#         return super().form_valid(form)

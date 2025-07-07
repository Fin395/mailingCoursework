from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from config.settings import EMAIL_HOST_USER
from mailings.forms import MailingRecipientForm, EmailMessageForm, MailingForm
from mailings.models import MailingRecipient, EmailMessage, Mailing, MailingAttempt
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.utils import timezone
from mailings.services import MailingService
from users.models import CustomUser


class MainPageView(LoginRequiredMixin, TemplateView):
    template_name = 'mailings/main_page.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['total_mailings'] = Mailing.objects.filter(owner=self.request.user).count()
        context['total_active_mailings'] = Mailing.objects.filter(status='Запущена', owner=self.request.user).count()
        context['total_recipients'] = MailingRecipient.objects.filter(owner=self.request.user).count()
        return context


class MailingRecipientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailingrecipient_form.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.add_mailingrecipient'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailingrecipient_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class MailingRecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = 'mailings/mailingrecipient_detail.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_mailingrecipient'


class MailingRecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'mailings/mailingrecipient_list.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_mailingrecipient'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['recipients'] = MailingRecipient.objects.all()
        return context

    def get_queryset(self):
        if not self.request.user.has_perm('mailings.can_cancel_mailing') and not self.request.user.has_perm('users.can_block_user') :
            return MailingRecipient.objects.filter(owner=self.request.user)
        return MailingRecipient.objects.all()


class MailingRecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailings/mailingrecipient_form.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.change_mailingrecipient'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailingrecipient_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingRecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingRecipient
    success_url = reverse_lazy('mailings:mailingrecipient_list')
    template_name = 'mailings/mailingrecipient_confirm_delete.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.delete_mailingrecipient'


class EmailMessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = EmailMessage
    form_class = EmailMessageForm
    template_name = 'mailings/emailmessage_form.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.add_emailmessage'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:emailmessage_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class EmailMessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = EmailMessage
    template_name = 'mailings/emailmessage_detail.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_emailmessage'


class EmailMessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = EmailMessage
    template_name = 'mailings/emailmessage_list.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_emailmessage'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['messages'] = EmailMessage.objects.all()
        return context

    def get_queryset(self):
        if not self.request.user.has_perm('mailings.can_cancel_mailing') and not self.request.user.has_perm(
                'users.can_block_user'):
            return EmailMessage.objects.filter(owner=self.request.user)
        return EmailMessage.objects.all()


class EmailMessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = EmailMessage
    form_class = EmailMessageForm
    template_name = 'mailings/emailmessage_form.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.change_emailmessage'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:emailmessage_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EmailMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = EmailMessage
    success_url = reverse_lazy('mailings:emailmessage_list')
    template_name = 'mailings/emailmessage_confirm_delete.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.delete_emailmessage'


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.add_mailing'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailing_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_mailing'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['mailings'] = Mailing.objects.all()
        return context


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_mailing'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['mailings'] = Mailing.objects.all()
        return context

    def get_queryset(self):
        if not self.request.user.has_perm('mailings.can_cancel_mailing') and not self.request.user.has_perm('users.can_block_user'):
            return Mailing.objects.filter(owner=self.request.user)
        return Mailing.objects.all()


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.change_mailing'

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailings:mailing_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')
    template_name = 'mailings/mailing_confirm_delete.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.delete_mailing'


class SendMailingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_mailing'

    def post(self, request, pk):
        MailingService.send_mailing(pk)
        return redirect('mailings:mailingattempt_list')


class MailingAttemptListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailings/mailingattempt_list.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'mailings.view_mailingattempt'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['mailingattempts'] = MailingAttempt.objects.all()
        return context


class CancelMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if not request.user.has_perm('mailings.can_cancel_mailing'):
            return HttpResponseForbidden("У вас нет прав для отключения рассылки.")

        # Логика отключения рассылки
        mailing.status = "Завершена"
        mailing.close_sending = timezone.now()
        mailing.save()

        return redirect('mailings:mailing_list')

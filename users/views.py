from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, View, DetailView
from config.settings import EMAIL_HOST_USER
from .forms import CustomUserRegistrationForm
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import CustomUser
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
import secrets


class UserRegisterView(CreateView):
    form_class = CustomUserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет! Перейди по ссылке {url} для подтверждения почты!',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'users.view_customuser'

    def get_object(self, queryset=None):
        user_to_view = super().get_object(queryset)
        user = self.request.user
        if user_to_view != user and not user.has_perm('mailings.can_cancel_mailing'):
            raise PermissionDenied
        return user_to_view


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserRegistrationForm
    template_name = 'users/registration.html'
    login_url = reverse_lazy('users:login')

    def get_success_url(self, **kwargs):
        return reverse_lazy('users:user_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/users_list.html'
    login_url = reverse_lazy('users:login')
    permission_required = 'users.view_customuser'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['users'] = CustomUser.objects.all()
        return context


class UserBlockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        if not request.user.has_perm('users.can_block_user'):
            return HttpResponseForbidden("У вас нет прав для блокирования получателя рассылки.")

        # Логика блокирования получателя рассылки
        if not request.user == user.email:
            user.is_active = False
            user.save()
        else:
            return HttpResponseForbidden("Вы не можете заблокировать себя")

        return redirect('users:users')

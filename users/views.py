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
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import PermissionDenied
import secrets
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_not_required, login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


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

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(CustomUser, pk=pk)
        if self.request.user != user:
            raise PermissionDenied
        return CustomUser.objects.filter(pk=self.request.user.pk)

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

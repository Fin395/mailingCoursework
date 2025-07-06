from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, View
from config.settings import EMAIL_HOST_USER
from .forms import CustomUserRegistrationForm
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import CustomUser


class UserRegisterView(CreateView):
    form_class = CustomUserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_mail(
            subject='Добро пожаловать в наш сервис',
            message='Спасибо, что зарегистрировались в нашем сервисе!',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


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
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserRegistrationForm
from django.core.mail import send_mail
from django.contrib.auth import login



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

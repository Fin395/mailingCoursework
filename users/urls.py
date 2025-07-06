from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
from users.views import UserRegisterView, UsersListView, UserBlockView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/users/', UsersListView.as_view(), name='users'),
    path('<int:pk>/user/block/', UserBlockView.as_view(), name='user_block'),

]
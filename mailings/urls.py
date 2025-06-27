from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingRecipientCreateView, MailingRecipientDetailView, MailingRecipientListView, \
    MailingRecipientUpdateView, MailingRecipientDeleteView, MainPageView

app_name = MailingsConfig.name

urlpatterns = [
    path('create/', MailingRecipientCreateView.as_view(), name='mailingrecipient_create'),
    path('<int:pk>/', MailingRecipientDetailView.as_view(), name='mailingrecipient_detail'),
    path('', MailingRecipientListView.as_view(), name='mailingrecipient_list'),
    path('<int:pk>/update/', MailingRecipientUpdateView.as_view(), name='mailingrecipient_update'),
    path('<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='mailingrecipient_delete'),
    path('main/', MainPageView.as_view(), name='mailingrecipient_main'),

]

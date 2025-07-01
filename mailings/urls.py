from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingRecipientCreateView, MailingRecipientDetailView, MailingRecipientListView, \
    MailingRecipientUpdateView, MailingRecipientDeleteView, MainPageView, EmailMessageCreateView, \
    EmailMessageDetailView, EmailMessageListView, EmailMessageUpdateView, EmailMessageDeleteView, MailingCreateView, \
    MailingDetailView, MailingListView, MailingUpdateView, MailingDeleteView, SendMailingView, MailingAttemptListView

app_name = MailingsConfig.name

urlpatterns = [
    path('create/recipient/', MailingRecipientCreateView.as_view(), name='mailingrecipient_create'),
    path('<int:pk>/recipient/', MailingRecipientDetailView.as_view(), name='mailingrecipient_detail'),
    path('recipients/', MailingRecipientListView.as_view(), name='mailingrecipient_list'),
    path('<int:pk>/recipient/update/', MailingRecipientUpdateView.as_view(), name='mailingrecipient_update'),
    path('<int:pk>/recipient/delete/', MailingRecipientDeleteView.as_view(), name='mailingrecipient_delete'),
    path('main/', MainPageView.as_view(), name='main'),
    path('create/message/', EmailMessageCreateView.as_view(), name='emailmessage_create'),
    path('<int:pk>/message/', EmailMessageDetailView.as_view(), name='emailmessage_detail'),
    path('messages/', EmailMessageListView.as_view(), name='emailmessage_list'),
    path('<int:pk>/message/update/', EmailMessageUpdateView.as_view(), name='emailmessage_update'),
    path('<int:pk>/message/delete/', EmailMessageDeleteView.as_view(), name='emailmessage_delete'),
    path('create/mailing/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/mailing/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/mailing/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/mailing/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/mailing/send/', SendMailingView.as_view(), name='mailing_send'),
    path('mailingattempts/', MailingAttemptListView.as_view(), name='mailingattempt_list'),

]

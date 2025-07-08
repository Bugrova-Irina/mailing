from django.urls import path

from sending_messages.apps import SendingMessagesConfig
from sending_messages.views import MailingListRecipientListView, MailingListRecipientDetailView, \
    MailingListRecipientUpdateView, MailingListRecipientDeleteView, MailingListRecipientCreateView, LetterListView, \
    LetterDetailView, LetterUpdateView, LetterCreateView, LetterDeleteView, MailingListView, MailingCreateView, \
    MailingDetailView, MailingUpdateView, MailingDeleteView, MainPageView, AttemptToSendCreateView, \
    AttemptToSendListView, AttemptToSendDetailView

app_name = SendingMessagesConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('recipients/', MailingListRecipientListView.as_view(), name='recipients_list'),
    path('recipients/<int:pk>/', MailingListRecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/create/', MailingListRecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/update/', MailingListRecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', MailingListRecipientDeleteView.as_view(), name='recipient_delete'),
    path('letter/', LetterListView.as_view(), name='letters_list'),
    path('letter/<int:pk>/', LetterDetailView.as_view(), name='letter_detail'),
    path('letter/create/', LetterCreateView.as_view(), name='letter_create'),
    path('letter/<int:pk>/update/', LetterUpdateView.as_view(), name='letter_update'),
    path('letter/<int:pk>/delete/', LetterDeleteView.as_view(), name='letter_delete'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('attempts/create/', AttemptToSendCreateView.as_view(), name='attempt_create'),
    path('attempts/', AttemptToSendListView.as_view(), name='attempts_list'),
    path('attempts/<int:pk>/', AttemptToSendDetailView.as_view(), name='attempt_detail'),
]

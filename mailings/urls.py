from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import (
    AttemptToSendCreateView,
    AttemptToSendDetailView,
    AttemptToSendListView,
    LetterCreateView,
    LetterDeleteView,
    LetterDetailView,
    LetterListView,
    LetterUpdateView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    RecipientsCreateView,
    RecipientsDeleteView,
    RecipientsDetailView,
    RecipientsListView,
    RecipientsUpdateView,
    MailingListView,
    MailingUpdateView,
    MainPageView,
)

app_name = MailingsConfig.name

urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("recipients/", RecipientsListView.as_view(), name="recipients_list"),
    path(
        "recipients/<int:pk>/",
        RecipientsDetailView.as_view(),
        name="recipient_detail",
    ),
    path(
        "recipients/create/",
        RecipientsCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipients/<int:pk>/update/",
        RecipientsUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        RecipientsDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("letter/", LetterListView.as_view(), name="letters_list"),
    path("letter/<int:pk>/", LetterDetailView.as_view(), name="letter_detail"),
    path("letter/create/", LetterCreateView.as_view(), name="letter_create"),
    path("letter/<int:pk>/update/", LetterUpdateView.as_view(), name="letter_update"),
    path("letter/<int:pk>/delete/", LetterDeleteView.as_view(), name="letter_delete"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("attempts/create/", AttemptToSendCreateView.as_view(), name="attempt_create"),
    path("attempts/", AttemptToSendListView.as_view(), name="attempts_list"),
    path(
        "attempts/<int:pk>/", AttemptToSendDetailView.as_view(), name="attempt_detail"
    ),
]

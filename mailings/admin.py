from django.contrib import admin

from mailings.models import AttemptToSend, Letter, Mailing, Recipients


@admin.register(Recipients)
class MailingListRecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "recipient_name", "comment")
    list_filter = ("recipient_name",)
    search_fields = ("email", "recipient_name")


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("start_sending", "end_sending", "status", "letter")
    list_filter = ("start_sending", "end_sending", "status")
    search_fields = ("start_sending", "end_sending", "status", "letter")


@admin.register(AttemptToSend)
class AttemptToSendAdmin(admin.ModelAdmin):
    list_display = ("attempt_date", "status", "mailing", "emails_sent", "owner")
    readonly_fields = ("emails_sent",)
    list_filter = ("status", "mailing")
    search_fields = ("attempt_date", "status", "mailing")

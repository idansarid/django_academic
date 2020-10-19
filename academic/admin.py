from django.contrib import admin

from academic.models import Profile, Bulletin, Sender, Receiver, Message

admin.site.register(Profile)
admin.site.register(Bulletin)
admin.site.register(Sender)
admin.site.register(Receiver)
admin.site.register(Message)
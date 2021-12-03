from django.contrib import admin

from .models import DirectMessage, Transmitter, Pager, Client, NewsChannel

admin.site.register(DirectMessage)
admin.site.register(Transmitter)
admin.site.register(Pager)
admin.site.register(Client)
admin.site.register(NewsChannel)

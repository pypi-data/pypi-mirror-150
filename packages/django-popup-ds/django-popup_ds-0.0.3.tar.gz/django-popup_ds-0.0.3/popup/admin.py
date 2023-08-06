from django.contrib import admin
from .models import NotiPopup, EventPopup, ImagePopup

import django.contrib.auth.models
from django.contrib import auth


class PopupAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'activate')
    search_fields = ['title']


admin.site.register(NotiPopup, PopupAdmin)
admin.site.register(EventPopup, PopupAdmin)
admin.site.register(ImagePopup, PopupAdmin)

try:
    admin.site.unregister(auth.models.User)
    admin.site.unregister(auth.models.Group)
except django.contrib.admin.sites.NotRegistered:
    pass

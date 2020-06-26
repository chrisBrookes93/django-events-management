from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'organiser', 'title', 'date_time')
    ordering = ('date_time',)


admin.site.register(Event, EventAdmin)

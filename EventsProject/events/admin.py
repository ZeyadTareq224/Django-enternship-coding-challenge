from django.contrib import admin

from .models import Event, EventSubscribtion

# Register your models here.
admin.site.register(Event)
admin.site.register(EventSubscribtion)
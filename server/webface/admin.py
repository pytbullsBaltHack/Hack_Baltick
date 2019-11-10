from django.contrib import admin
from .models import StreamSource, UserFace, Visitor, Event

admin.site.register(StreamSource)
admin.site.register(UserFace)
admin.site.register(Visitor)
admin.site.register(Event)

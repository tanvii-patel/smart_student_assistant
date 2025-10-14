from django.contrib import admin
from .models import Timetable, Task, Resource, Notification

admin.site.register(Timetable)
admin.site.register(Task)
admin.site.register(Resource)
admin.site.register(Notification)

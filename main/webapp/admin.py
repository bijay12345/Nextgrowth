from django.contrib import admin
from .models import Task, App, UserProfile

admin.site.register(Task)
admin.site.register(App)
admin.site.register(UserProfile)
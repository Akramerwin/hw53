from django.contrib import admin
from webapp.models import Todo, Status, Type, Projects

admin.site.register(Projects)
admin.site.register(Todo)
admin.site.register(Status)
admin.site.register(Type)

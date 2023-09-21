from django.contrib import admin
from .models import Comment, Blog

admin.site.register(Blog)
admin.site.register(Comment)

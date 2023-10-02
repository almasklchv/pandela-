from django.contrib import admin
from .models import Comment, Blog, Playlist

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Playlist)

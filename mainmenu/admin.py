from django.contrib import admin
from .models import Profile, Course, Video, Review
# Register your models here.

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(Review)
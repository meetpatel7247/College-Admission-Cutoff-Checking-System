from django.contrib import admin
from .models import College, Course, UserProfile

admin.site.register(College)
admin.site.register(Course)
admin.site.register(UserProfile)
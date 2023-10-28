# admin.py
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('num','title', 'company', 'location', 'summary','salary')

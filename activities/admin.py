from django.contrib import admin
from .models import ActivityGroup, Activity, ReportActivity
# Register your models here.

@admin.register(ActivityGroup)
class ActivityGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "until",)

@admin.register(ReportActivity)
class ReportActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "activity", "created_at")
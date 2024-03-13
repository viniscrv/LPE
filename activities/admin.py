from django.contrib import admin
from .models import Activity, ReportActivity
# Register your models here.

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "until",)

@admin.register(ReportActivity)
class ReportActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "activity", "created_at")
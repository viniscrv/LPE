from django.contrib import admin
from .models import ActivityGroup, Activity, ReportActivity
# Register your models here.

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0

@admin.register(ActivityGroup)
class ActivityGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    inlines = [ActivityInline]

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "until",)

@admin.register(ReportActivity)
class ReportActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "activity", "created_at")
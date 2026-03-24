from django.contrib import admin

from apps.moment.models import Moment


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at")
    search_fields = ("title", "details")
    list_filter = ("created_at",)

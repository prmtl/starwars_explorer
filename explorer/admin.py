from django.contrib import admin

from .models import Collection


@admin.register(Collection)
class CollectionsAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    readonly_fields = ("id",)

from django.contrib import admin
from .models import Demand

@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description")

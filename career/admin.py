from django.contrib import admin
from .models import Career, CareerApplication

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "is_active", "created_at")
    list_filter = ("is_active", "location")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "career", "applied_at")
    list_filter = ("career",)
    search_fields = ("name", "email", "phone", "career__title")

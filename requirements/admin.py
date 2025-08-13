from django.contrib import admin
from .models import Requirement


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'requirement_type', 'property_type', 'location', 'budget', 'created_at']
    list_filter = ['requirement_type', 'property_type', 'budget_range', 'created_at']
    search_fields = ['name', 'contact_number', 'email', 'location']
    readonly_fields = ['created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'contact_number', 'email')
        }),
        ('Requirement Details', {
            'fields': ('requirement_type', 'property_type', 'location', 'area_needed')
        }),
        ('Budget Information', {
            'fields': ('budget', 'budget_range')
        }),
        ('Additional Information', {
            'fields': ('specific_requirements', 'agreed_to_terms')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

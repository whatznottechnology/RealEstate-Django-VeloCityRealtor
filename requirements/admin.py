from django.contrib import admin
from .models import Requirement


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'requirement_type', 'property_type', 'enquiry_from', 'location', 'budget_display', 'created_at']
    list_filter = ['requirement_type', 'property_type', 'enquiry_from', 'budget_range', 'agreed_to_terms', 'created_at']
    search_fields = ['name', 'contact_number', 'email', 'location', 'specific_requirements']
    readonly_fields = ['created_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    def budget_display(self, obj):
        """Display budget or budget_range"""
        if obj.budget:
            return obj.budget
        elif obj.budget_range:
            return obj.get_budget_range_display()
        return '-'
    budget_display.short_description = 'Budget'
    budget_display.admin_order_field = 'budget'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'contact_number', 'email', 'enquiry_from'),
            'classes': ('wide',),
        }),
        ('Requirement Details', {
            'fields': ('requirement_type', 'property_type', 'location', 'area_needed'),
            'classes': ('wide',),
        }),
        ('Budget Information', {
            'fields': ('budget', 'budget_range'),
            'classes': ('wide',),
        }),
        ('Property Requirements', {
            'fields': ('specific_requirements',),
            'classes': ('wide',),
        }),
        ('Agreement & Terms', {
            'fields': ('agreed_to_terms',),
            'classes': ('wide',),
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from django.utils.html import format_html
from django.urls import reverse
from .models import Requirement


@admin.register(Requirement)
class RequirementAdmin(ModelAdmin):
    list_display = ['name', 'contact_number', 'requirement_type', 'property_type', 'enquiry_from', 'location', 'budget_display', 'created_at', 'action_buttons']
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
    
    def action_buttons(self, obj):
        return format_html(
            '<div style="display: flex; gap: 5px; flex-wrap: nowrap;">'
            '<a href="{}" style="background: #3b82f6; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 11px; white-space: nowrap; display: inline-block;">✏️ Edit</a>'
            '</div>',
            reverse('admin:requirements_requirement_change', args=[obj.pk])
        )
    action_buttons.short_description = '⚙️ Actions'
    
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


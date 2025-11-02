from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from django.utils.html import format_html
from django.urls import reverse
from .models import InvestmentRequirement


@admin.register(InvestmentRequirement)
class InvestmentRequirementAdmin(ModelAdmin):
    list_display = ['name', 'contact_number', 'budget', 'requirement_type', 'how_did_you_know', 'created_at', 'action_buttons']
    list_filter = ['requirement_type', 'how_did_you_know', 'agreed_to_terms', 'created_at']
    search_fields = ['name', 'contact_number', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def action_buttons(self, obj):
        return format_html(
            '<div style="display: flex; gap: 5px; flex-wrap: nowrap;">'
            '<a href="{}" style="background: #3b82f6; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 11px; white-space: nowrap; display: inline-block;">✏️ Edit</a>'
            '</div>',
            reverse('admin:investment_leads_investmentrequirement_change', args=[obj.pk])
        )
    action_buttons.short_description = '⚙️ Actions'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'contact_number')
        }),
        ('Investment Details', {
            'fields': ('location', 'budget', 'requirement_type', 'how_did_you_know')
        }),
        ('Agreement & Timeline', {
            'fields': ('agreed_to_terms', 'created_at')
        }),
    )


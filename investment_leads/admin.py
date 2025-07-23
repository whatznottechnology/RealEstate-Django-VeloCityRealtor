from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import InvestmentRequirement


@admin.register(InvestmentRequirement)
class InvestmentRequirementAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'budget', 'requirement_type', 'created_at', 'action_buttons']
    list_filter = ['requirement_type', 'property_type', 'enquiry_from', 'agreed_to_terms', 'created_at']
    search_fields = ['name', 'contact_number', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def action_buttons(self, obj):
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="button" style="background: #007cba; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">✏️ Edit</a>'
            '<a href="{}" class="button" style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">👁️ View Details</a>'
            '</div>',
            reverse('admin:investment_leads_investmentrequirement_change', args=[obj.pk]),
            f'/investment-leads/requirement/{obj.pk}/detail/'
        )
    action_buttons.short_description = '⚙️ Actions'
    action_buttons.allow_tags = True
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'contact_number')
        }),
        ('Requirement Details', {
            'fields': ('location', 'budget', 'requirement_type', 'property_type', 'enquiry_from')
        }),
        ('Additional Information', {
            'fields': ('property_details',)
        }),
        ('Agreement & Timeline', {
            'fields': ('agreed_to_terms', 'created_at')
        }),
    )

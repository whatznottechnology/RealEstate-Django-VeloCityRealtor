from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import LandRequirement


@admin.register(LandRequirement)
class LandRequirementAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'budget', 'requirement_type', 'enquiry_from', 'status_badge', 'created_at', 'action_buttons']
    list_filter = ['requirement_type', 'enquiry_from', 'area_unit', 'status', 'agreed_to_terms', 'created_at']
    search_fields = ['name', 'contact_number', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def status_badge(self, obj):
        colors = {
            'new': '#17a2b8',
            'in_progress': '#ffc107',
            'contacted': '#fd7e14',
            'qualified': '#20c997',
            'converted': '#28a745',
            'closed': '#6c757d',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = '📊 Status'
    
    def action_buttons(self, obj):
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="button" style="background: #007cba; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">✏️ Edit</a>'
            '<a href="{}" class="button" style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">👁️ View Details</a>'
            '</div>',
            reverse('admin:land_leads_landrequirement_change', args=[obj.pk]),
            f'/land-leads/requirement/{obj.pk}/detail/'
        )
    action_buttons.short_description = '⚙️ Actions'
    action_buttons.allow_tags = True
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'contact_number', 'enquiry_from')
        }),
        ('Requirement Details', {
            'fields': ('location', 'budget', 'area', 'area_unit', 'requirement_type')
        }),
        ('Status & Agreement', {
            'fields': ('status', 'agreed_to_terms', 'created_at')
        }),
    )

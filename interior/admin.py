from django.contrib import admin
from django.utils.html import format_html
from .models import InteriorInquiry, InquiryStatus, InteriorService, PortfolioWork


# InteriorConfig removed - now using theme.SiteConfig for all contact information


@admin.register(InteriorService)
class InteriorServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'badge_text', 'is_active', 'order', 'image_preview')
    list_filter = ('category', 'is_active', 'badge_text')
    search_fields = ('title', 'description', 'features')
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'description', 'icon_class')
        }),
        ('Visual Elements', {
            'fields': ('image', 'badge_text')
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Enter each feature on a new line'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def image_preview(self, obj):
        """Display image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(PortfolioWork)
class PortfolioWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'work_type', 'location', 'completion_date', 'is_featured', 'is_active', 'order', 'image_preview')
    list_filter = ('work_type', 'is_featured', 'is_active', 'completion_date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('order', 'is_active', 'is_featured')
    date_hierarchy = 'completion_date'
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description', 'work_type')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Additional Details', {
            'fields': ('location', 'completion_date')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    def image_preview(self, obj):
        """Display image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(InteriorInquiry)
class InteriorInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service_type_display', 'status_badge', 'created_at', 'actions_column')
    list_filter = ('status', 'service_type', 'created_at')
    search_fields = ('name', 'email', 'phone', 'project_details', 'location')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Service Details', {
            'fields': ('service_type', 'project_details', 'budget_range', 'timeline', 'location')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'notes', 'contacted_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_contacted', 'mark_as_consultation', 'mark_as_quoted']
    
    def service_type_display(self, obj):
        """Display service type with icon"""
        icons = {
            'residential': '🏠',
            'commercial': '🏢',
            'modular': '📦',
            '3d_visualization': '🎨',
            'furniture': '🛋️',
            'renovation': '🔨',
            'other': '📋'
        }
        icon = icons.get(obj.service_type, '📋')
        return f"{icon} {obj.get_service_type_display()}"
    service_type_display.short_description = 'Service Type'
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'new': '#ef4444',
            'contacted': '#f59e0b',
            'consultation': '#3b82f6',
            'quoted': '#8b5cf6',
            'converted': '#10b981',
            'closed': '#6b7280'
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def actions_column(self, obj):
        """Quick action buttons"""
        return format_html(
            '<a class="button" href="tel:{}" style="margin-right: 5px;">📞 Call</a>'
            '<a class="button" href="mailto:{}">✉️ Email</a>',
            obj.phone,
            obj.email
        )
    actions_column.short_description = 'Actions'
    
    def mark_as_contacted(self, request, queryset):
        """Mark selected inquiries as contacted"""
        updated = queryset.update(status=InquiryStatus.CONTACTED)
        self.message_user(request, f'{updated} inquiries marked as contacted.')
    mark_as_contacted.short_description = "Mark as Contacted"
    
    def mark_as_consultation(self, request, queryset):
        """Mark selected inquiries as consultation scheduled"""
        updated = queryset.update(status=InquiryStatus.CONSULTATION)
        self.message_user(request, f'{updated} inquiries marked as consultation scheduled.')
    mark_as_consultation.short_description = "Mark as Consultation Scheduled"
    
    def mark_as_quoted(self, request, queryset):
        """Mark selected inquiries as quoted"""
        updated = queryset.update(status=InquiryStatus.QUOTED)
        self.message_user(request, f'{updated} inquiries marked as quoted.')
    mark_as_quoted.short_description = "Mark as Quoted"


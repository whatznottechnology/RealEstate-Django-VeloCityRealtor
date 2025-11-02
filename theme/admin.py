from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfig, ContactForm, Developer, Testimonial


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    """Admin configuration for Developer model"""
    
    list_display = ('name', 'is_active', 'order', 'website_url', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Developer Information', {
            'fields': ('name', 'logo', 'website_url', 'description'),
            'classes': ('wide',),
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order'),
            'classes': ('wide',),
            'description': 'Control how this developer appears on the website'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_queryset(self, request):
        """Order by display order then name"""
        return super().get_queryset(request).order_by('order', 'name')


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    """Admin configuration for ContactForm model"""
    
    list_display = ('name', 'email', 'phone', 'subject', 'submitted_at', 'is_read')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'subject')
    readonly_fields = ('submitted_at',)
    list_editable = ('is_read',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject'),
        }),
        ('Message', {
            'fields': ('message',),
        }),
        ('Status', {
            'fields': ('is_read', 'submitted_at'),
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding new contact forms from admin"""
        return False


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    """Admin configuration for SiteConfig model"""
    
    list_display = ('site_title', 'show_social_media', 'updated_at')
    list_filter = ('show_social_media', 'created_at', 'updated_at')
    search_fields = ('site_title', 'site_description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'site_description', 'site_logo', 'contact_email', 'contact_phone', 'sales_phone', 'office_address'),
            'classes': ('wide',),
            'description': 'Contact Phone: Primary contact number | Sales Phone: Number for "Call Us Now" buttons'
        }),
        ('Company Brochure', {
            'fields': ('company_brochure',),
            'classes': ('wide',),
            'description': 'Upload the company brochure PDF file that will be available for download on the homepage.'
        }),
        ('Promotional Popup', {
            'fields': ('promo_popup_image', 'promo_popup_name'),
            'classes': ('wide',),
            'description': 'Upload a square image and set a name/title for the promotional popup.'
        }),
        ('Social Media Links', {
            'fields': (
                'show_social_media',
                'facebook_url',
                'instagram_url', 
                'youtube_url',
                'twitter_url',
                'linkedin_url',
                'whatsapp_number'
            ),
            'classes': ('wide',),
            'description': 'Enter social media URLs. Use # for links you want to disable.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow adding if no SiteConfig exists"""
        return not SiteConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of SiteConfig"""
        return False


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin configuration for Testimonial model"""
    
    list_display = ('name', 'location', 'rating_display', 'project_type', 'is_featured', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'is_featured', 'rating', 'created_at')
    search_fields = ('name', 'location', 'review_text', 'company')
    list_editable = ('is_featured', 'is_active', 'display_order')
    readonly_fields = ('created_at', 'updated_at', 'rating_preview')
    
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'location', 'designation', 'company', 'client_image'),
            'classes': ('wide',),
            'description': 'Enter client details (Bengali names and locations supported)'
        }),
        ('Review Details', {
            'fields': ('rating', 'rating_preview', 'review_text', 'project_type'),
            'classes': ('wide',),
            'description': 'Client review and rating details'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'display_order'),
            'classes': ('wide',),
            'description': 'Control how this testimonial appears on the website. Featured testimonials appear first.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def rating_display(self, obj):
        """Display star rating in list view"""
        full_stars = '⭐' * obj.rating
        empty_stars = '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #fbbf24;">{}</span><span style="color: #d1d5db;">{}</span>',
            full_stars,
            empty_stars
        )
    rating_display.short_description = 'Rating'
    
    def rating_preview(self, obj):
        """Display star rating preview in form"""
        if obj.rating:
            full_stars = '⭐' * obj.rating
            empty_stars = '☆' * (5 - obj.rating)
            return format_html(
                '<div style="font-size: 24px;"><span style="color: #fbbf24;">{}</span><span style="color: #d1d5db;">{}</span></div>',
                full_stars,
                empty_stars
            )
        return "No rating"
    rating_preview.short_description = 'Rating Preview'
    
    def get_queryset(self, request):
        """Order by featured status, display order, then creation date"""
        return super().get_queryset(request).order_by('-is_featured', 'display_order', '-created_at')

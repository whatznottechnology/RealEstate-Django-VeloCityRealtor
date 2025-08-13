from django.contrib import admin
from .models import SiteConfig, ContactForm


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
            'fields': ('site_title', 'site_description', 'contact_email', 'contact_phone', 'office_address'),
            'classes': ('wide',),
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

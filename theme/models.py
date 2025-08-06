from django.db import models


class SiteConfig(models.Model):
    # Promotional Popup
    promo_popup_image = models.ImageField(
        upload_to='site/promo_popup/',
        blank=True,
        null=True,
        verbose_name="Promotional Popup Image",
        help_text="Square image for promotional popup (recommended 1:1 ratio, e.g. 400x400px)"
    )
    promo_popup_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Promotional Popup Name",
        help_text="Name or title for the promotional popup image"
    )
    """Site configuration model for managing social media links and other site settings"""
    
    # Social Media Links
    facebook_url = models.URLField(
        verbose_name="Facebook URL",
        blank=True,
        null=True,
        default="#",
        help_text="Facebook page URL"
    )
    instagram_url = models.URLField(
        verbose_name="Instagram URL",
        blank=True,
        null=True,
        default="#",
        help_text="Instagram profile URL"
    )
    youtube_url = models.URLField(
        verbose_name="YouTube URL",
        blank=True,
        null=True,
        default="#",
        help_text="YouTube channel URL"
    )
    twitter_url = models.URLField(
        verbose_name="X (Twitter) URL",
        blank=True,
        null=True,
        default="#",
        help_text="X (formerly Twitter) profile URL"
    )
    linkedin_url = models.URLField(
        verbose_name="LinkedIn URL",
        blank=True,
        null=True,
        default="#",
        help_text="LinkedIn company page URL"
    )
    whatsapp_number = models.CharField(
        verbose_name="WhatsApp Number",
        max_length=20,
        blank=True,
        null=True,
        help_text="WhatsApp number with country code (e.g., +919876543210)"
    )
    
    # Other site settings
    site_title = models.CharField(
        verbose_name="Site Title",
        max_length=100,
        default="VeloCity Realtor",
        help_text="Website title"
    )
    site_description = models.TextField(
        verbose_name="Site Description",
        blank=True,
        null=True,
        help_text="Website description for SEO"
    )
    contact_email = models.EmailField(
        verbose_name="Contact Email",
        blank=True,
        null=True,
        help_text="Primary contact email"
    )
    contact_phone = models.CharField(
        verbose_name="Contact Phone",
        max_length=20,
        blank=True,
        null=True,
        help_text="Primary contact phone number"
    )
    
    # Settings
    show_social_media = models.BooleanField(
        verbose_name="Show Social Media Icons",
        default=True,
        help_text="Display floating social media icons on the website"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
        
    def __str__(self):
        return f"Site Configuration - {self.site_title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one SiteConfig instance exists
        if not self.pk and SiteConfig.objects.exists():
            raise ValueError("Only one SiteConfig instance is allowed. Please update the existing one.")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Get or create the site configuration"""
        config, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_title': 'VeloCity Realtor',
                'facebook_url': '#',
                'instagram_url': '#',
                'youtube_url': '#',
                'twitter_url': '#',
                'linkedin_url': '#',
                'whatsapp_number': '',
                'show_social_media': True,
            }
        )
        return config

    def get_whatsapp_url(self):
        """Generate WhatsApp URL for web"""
        if self.whatsapp_number:
            # Remove any non-digit characters except +
            clean_number = ''.join(filter(lambda x: x.isdigit() or x == '+', self.whatsapp_number))
            return f"https://wa.me/{clean_number.lstrip('+')}"
        return "#"

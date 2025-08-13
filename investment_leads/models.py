from django.db import models


class InvestmentRequirement(models.Model):
    REQUIREMENT_TYPE_CHOICES = [
        ('commercial', 'Commercial'),
        ('residential', 'Residential'),
    ]
    
    HOW_DID_YOU_KNOW_CHOICES = [
        ('google', 'Google Search'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('referral', 'Friend/Family Referral'),
        ('newspaper', 'Newspaper'),
        ('outdoor_ads', 'Outdoor Advertisements'),
        ('tv_ads', 'Television Ads'),
        ('radio', 'Radio'),
        ('website', 'Our Website'),
        ('email', 'Email Marketing'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(blank=True, null=True, verbose_name="Email Address")
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Location")
    budget = models.CharField(max_length=100, verbose_name="Budget")
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPE_CHOICES, verbose_name="Requirement Type")
    how_did_you_know = models.CharField(max_length=20, choices=HOW_DID_YOU_KNOW_CHOICES, blank=True, null=True, verbose_name="How did you get to know about us?")
    agreed_to_terms = models.BooleanField(default=False, verbose_name="Agreed to Terms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_requirement_type_display()}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Investment Lead'
        verbose_name_plural = 'Investment Leads'

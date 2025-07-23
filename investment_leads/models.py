from django.db import models


class InvestmentRequirement(models.Model):
    REQUIREMENT_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sale', 'Sale'),
        ('want_lease', 'Want Lease'),
        ('for_lease', 'For Lease'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('bar', 'Bar'),
        ('banquet', 'Banquet'),
        ('petrol_pump', 'Petrol Pump'),
        ('land', 'Land'),
        ('showroom', 'Showroom'),
    ]
    
    ENQUIRY_FROM_CHOICES = [
        ('agent', 'Agent'),
        ('owner', 'Owner'),
        ('individual', 'Individual'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255, blank=True, null=True)
    budget = models.CharField(max_length=100)
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    enquiry_from = models.CharField(max_length=20, choices=ENQUIRY_FROM_CHOICES)
    property_details = models.TextField(blank=True, null=True)
    agreed_to_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.contact_number}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Investment Requirement'
        verbose_name_plural = 'Investment Requirements'

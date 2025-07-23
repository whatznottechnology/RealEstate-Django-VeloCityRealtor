from django.db import models


class LandRequirement(models.Model):
    AREA_UNIT_CHOICES = [
        ('bigha', 'Bigha'),
        ('cottah', 'Cottah'),
        ('acre', 'Acre'),
        ('decimal', 'Decimal'),
    ]
    
    REQUIREMENT_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sale', 'Sale'),
        ('joint_venture', 'Joint Venture'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255, blank=True, null=True)
    budget = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area_unit = models.CharField(max_length=20, choices=AREA_UNIT_CHOICES, blank=True, null=True)
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    agreed_to_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.contact_number}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Land Requirement'
        verbose_name_plural = 'Land Requirements'

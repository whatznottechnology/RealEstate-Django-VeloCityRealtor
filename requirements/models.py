from django.db import models


class Requirement(models.Model):
    REQUIREMENT_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sale', 'Sale'),
        ('rent', 'Rent'),
        ('lease', 'Lease'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('land', 'Land'),
        ('office', 'Office Space'),
        ('retail', 'Retail Space'),
        ('warehouse', 'Warehouse'),
    ]
    
    BUDGET_RANGE_CHOICES = [
        ('under_10l', 'Under 10 Lakhs'),
        ('10l_25l', '10 - 25 Lakhs'),
        ('25l_50l', '25 - 50 Lakhs'),
        ('50l_1cr', '50 Lakhs - 1 Crore'),
        ('1cr_2cr', '1 - 2 Crores'),
        ('2cr_5cr', '2 - 5 Crores'),
        ('5cr_plus', '5+ Crores'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255, blank=True, null=True)
    budget = models.CharField(max_length=100)
    budget_range = models.CharField(max_length=20, choices=BUDGET_RANGE_CHOICES, blank=True, null=True)
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    area_needed = models.CharField(max_length=100, blank=True, null=True)
    specific_requirements = models.TextField(blank=True, null=True)
    agreed_to_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_requirement_type_display()} {self.get_property_type_display()}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Property Requirement'
        verbose_name_plural = 'Property Requirements'

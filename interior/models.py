from django.db import models
from django.utils import timezone

class ServiceType(models.TextChoices):
    RESIDENTIAL = 'residential', 'Residential Interior'
    COMMERCIAL = 'commercial', 'Commercial Interior'
    MODULAR = 'modular', 'Modular Solutions'
    VISUALIZATION_3D = '3d_visualization', '3D Visualization'
    FURNITURE = 'furniture', 'Furniture & Decor'
    RENOVATION = 'renovation', 'Renovation & Remodeling'
    OTHER = 'other', 'Other'

class InquiryStatus(models.TextChoices):
    NEW = 'new', 'New'
    CONTACTED = 'contacted', 'Contacted'
    CONSULTATION = 'consultation', 'Consultation Scheduled'
    QUOTED = 'quoted', 'Quote Sent'
    CONVERTED = 'converted', 'Converted to Project'
    CLOSED = 'closed', 'Closed'

class InteriorService(models.Model):
    """Model for interior design services offered"""
    
    CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('modular', 'Modular Solutions'),
        ('3d_visualization', '3D Visualization'),
        ('furniture', 'Furniture & Decor'),
        ('renovation', 'Renovation & Remodeling'),
    ]
    
    BADGE_CHOICES = [
        ('popular', 'Popular'),
        ('professional', 'Professional'),
        ('trending', 'Trending'),
        ('new', 'New'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Service Title")
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Category"
    )
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to='interior/services/',
        verbose_name="Service Image"
    )
    badge_text = models.CharField(
        max_length=50,
        choices=BADGE_CHOICES,
        blank=True,
        verbose_name="Badge Label"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fas fa-home",
        verbose_name="Font Awesome Icon Class",
        help_text="e.g., fas fa-home, fas fa-building"
    )
    features = models.TextField(
        verbose_name="Features (one per line)",
        help_text="Enter each feature on a new line"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Interior Service"
        verbose_name_plural = "Interior Services"
        ordering = ['order', '-created_at']
        
    def __str__(self):
        return self.title
    
    def get_features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class PortfolioWork(models.Model):
    """Model for portfolio/recent work showcase"""
    
    WORK_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('modular', 'Modular'),
        ('renovation', 'Renovation'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    description = models.TextField(verbose_name="Project Description")
    work_type = models.CharField(
        max_length=50,
        choices=WORK_TYPE_CHOICES,
        verbose_name="Work Type"
    )
    image = models.ImageField(
        upload_to='interior/portfolio/',
        verbose_name="Project Image"
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Project Location"
    )
    completion_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Completion Date"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured Project"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Portfolio Work"
        verbose_name_plural = "Portfolio Works"
        ordering = ['order', '-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.get_work_type_display()}"


class InteriorInquiry(models.Model):
    """Model for interior design service inquiries"""
    
    # Personal Information
    name = models.CharField(max_length=200, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    
    # Service Details
    service_type = models.CharField(
        max_length=50,
        choices=ServiceType.choices,
        default=ServiceType.RESIDENTIAL,
        verbose_name="Service Type"
    )
    project_details = models.TextField(
        verbose_name="Project Details",
        help_text="Tell us about your project"
    )
    
    # Additional Information
    budget_range = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Budget Range"
    )
    timeline = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Expected Timeline"
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Project Location"
    )
    
    # Status and Tracking
    status = models.CharField(
        max_length=20,
        choices=InquiryStatus.choices,
        default=InquiryStatus.NEW,
        verbose_name="Status"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Admin Notes"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    contacted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Contacted On"
    )
    
    class Meta:
        verbose_name = "Interior Inquiry"
        verbose_name_plural = "Interior Inquiries"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def mark_as_contacted(self):
        """Mark inquiry as contacted"""
        self.status = InquiryStatus.CONTACTED
        self.contacted_at = timezone.now()
        self.save()


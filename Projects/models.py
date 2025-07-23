from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class City(models.Model):
    """Cities where projects are located"""
    name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    icon = models.ImageField(upload_to='cities/icons/', blank=True, null=True, help_text="City icon/image")
    
    # Metadata fields
    description = models.TextField(blank=True, null=True, help_text="City description for SEO")
    keywords = models.CharField(max_length=500, blank=True, null=True, help_text="SEO keywords, comma separated")
    meta_title = models.CharField(max_length=200, blank=True, null=True, help_text="SEO meta title")
    meta_description = models.TextField(max_length=300, blank=True, null=True, help_text="SEO meta description")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.state}"


class Category(models.Model):
    """Real estate categories: Residential, Commercial"""
    name = models.CharField(max_length=100, unique=True)
    
    # Metadata fields
    description = models.TextField(blank=True, null=True, help_text="Category description for SEO")
    keywords = models.CharField(max_length=500, blank=True, null=True, help_text="SEO keywords, comma separated")
    meta_title = models.CharField(max_length=200, blank=True, null=True, help_text="SEO meta title")
    meta_description = models.TextField(max_length=300, blank=True, null=True, help_text="SEO meta description")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProjectType(models.Model):
    """Project types like Apartment, Villa, Office, etc."""
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='project_types')
    
    # Metadata fields
    description = models.TextField(blank=True, null=True, help_text="Project type description for SEO")
    keywords = models.CharField(max_length=500, blank=True, null=True, help_text="SEO keywords, comma separated")
    meta_title = models.CharField(max_length=200, blank=True, null=True, help_text="SEO meta title")
    meta_description = models.TextField(max_length=300, blank=True, null=True, help_text="SEO meta description")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Tag(models.Model):
    """Tags like Trending, Hot, Ready to Move, Just Launched"""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Amenity(models.Model):
    """Amenities like Pool, Clubhouse, Gym, Security"""
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='amenities/icons/', blank=True, null=True, help_text="Amenity icon/image")
    
    # Metadata fields
    description = models.TextField(blank=True, null=True, help_text="Amenity description for SEO")
    keywords = models.CharField(max_length=500, blank=True, null=True, help_text="SEO keywords, comma separated")
    meta_title = models.CharField(max_length=200, blank=True, null=True, help_text="SEO meta title")
    meta_description = models.TextField(max_length=300, blank=True, null=True, help_text="SEO meta description")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Main Project model with all primary fields"""
    
    STATUS_CHOICES = [
        ('ready_to_move', 'Ready to Move'),
        ('under_construction', 'Under Construction'),
        ('upcoming', 'Upcoming'),
        ('sold_out', 'Sold Out'),
    ]
    
    # Primary Fields
    name = models.CharField(max_length=200)
    project_by = models.CharField(max_length=200, help_text="Company or Brand", blank=True, null=True)
    logo = models.ImageField(upload_to='project/logo/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='project/banner/', blank=True, null=True)
    brochure = models.FileField(upload_to='project/brochure/', blank=True, null=True, help_text="PDF download")
    
    # Location & Details
    location = models.CharField(max_length=300, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='projects', help_text="Select city", null=True, blank=True)
    developers = models.CharField(max_length=200, help_text="Developer name", blank=True, null=True)
    build_up_area = models.CharField(max_length=100, help_text="e.g. 1200 sq ft", blank=True, null=True)
    bhk = models.CharField(max_length=50, help_text="e.g. 2, 3, 4 BHK", blank=True, null=True)
    no_of_blocks = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    no_of_units = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_construction', blank=True, null=True)
    possession_date = models.DateField(blank=True, null=True)
    onwards_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    
    # Map Integration
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    
    # Categorization & Filtering
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='projects')
    
    # Promotional & Marketing Tags
    TRENDING_CHOICES = [
        ('just_launched', 'Just Launched'),
        ('hot', 'Hot'),
        ('premium', 'Premium'),
        ('ultra_luxury', 'Ultra Luxury'),
        ('ready_to_move', 'Ready to Move'),
        ('affordable', 'Affordable'),
    ]
    
    # Marketing & Promotion Fields
    is_most_viewed = models.BooleanField(default=False, help_text="Mark as Most Viewed")
    trending_tag = models.CharField(max_length=20, choices=TRENDING_CHOICES, blank=True, null=True, help_text="Trending status")
    is_nearby_property = models.BooleanField(default=False, help_text="Show in Nearby Properties")
    is_recently_viewed = models.BooleanField(default=False, help_text="Mark as Recently Viewed")
    
    # Additional promotional fields
    is_hot_deal = models.BooleanField(default=False, help_text="Hot Deal Badge")
    is_premium_listing = models.BooleanField(default=False, help_text="Premium Listing")
    is_editors_choice = models.BooleanField(default=False, help_text="Editor's Choice")
    
    # Metadata fields
    description = models.TextField(blank=True, null=True, help_text="Project description for SEO")
    keywords = models.CharField(max_length=500, blank=True, null=True, help_text="SEO keywords, comma separated")
    meta_title = models.CharField(max_length=200, blank=True, null=True, help_text="SEO meta title")
    meta_description = models.TextField(max_length=300, blank=True, null=True, help_text="SEO meta description")
    
    # Tracking
    views = models.PositiveIntegerField(default=0, help_text="For Most Viewed sorting")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'project_type']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['-views']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} by {self.project_by}"
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])


class ProjectOverview(models.Model):
    """One-to-one overview for each project"""
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='overview')
    title = models.CharField(max_length=200, help_text="Project tagline or section title")
    short_description = models.TextField(help_text="Rich or plain text description")
    
    def __str__(self):
        return f"Overview: {self.project.name}"


class GalleryImage(models.Model):
    """Multiple gallery images per project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='project/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
    
    def __str__(self):
        return f"{self.project.name} - Gallery Image {self.id}"


class NearestArea(models.Model):
    """Nearby areas like Schools, Hospitals, Metro"""
    
    AREA_TYPES = [
        ('school', 'School'),
        ('hospital', 'Hospital'),
        ('metro', 'Metro Station'),
        ('mall', 'Shopping Mall'),
        ('restaurant', 'Restaurant'),
        ('park', 'Park'),
        ('airport', 'Airport'),
        ('bus_stop', 'Bus Stop'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='nearest_areas')
    name = models.CharField(max_length=200)
    area_type = models.CharField(max_length=20, choices=AREA_TYPES)
    distance = models.CharField(max_length=50, blank=True, help_text="e.g. 2 km, 5 min walk")
    
    class Meta:
        ordering = ['area_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_area_type_display()})"


class FloorPlan(models.Model):
    """Multiple floor plans per project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='floor_plans')
    name = models.CharField(max_length=100, help_text="e.g. 2BHK East Facing")
    image = models.ImageField(upload_to='project/floor_plans/')
    area = models.CharField(max_length=50, blank=True, help_text="e.g. 1200 sq ft")
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"


class ConstructionUpdate(models.Model):
    """Construction progress updates with images"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='construction_updates')
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='project/construction_updates/')
    description = models.TextField(blank=True)
    update_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-update_date', 'order']
    
    def __str__(self):
        return f"{self.project.name} - Update {self.update_date}"


class WhyChooseUs(models.Model):
    """USPs and selling points for each project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='why_choose_us')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Why Choose Us"
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"


class SpecificationCategory(models.Model):
    """Categories for specifications like Flooring, Fittings, etc."""
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Specification Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class SpecificationItem(models.Model):
    """Individual specification items grouped by category"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='specifications')
    category = models.ForeignKey(SpecificationCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200, help_text="e.g. Bedroom, Kitchen, Door")
    description = models.TextField(help_text="e.g. Wooden flooring, Vitrified tiles")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category__order', 'order', 'name']
        unique_together = ['project', 'category', 'name']
    
    def __str__(self):
        return f"{self.project.name} - {self.category.name}: {self.name}"


class ProjectAmenityImage(models.Model):
    """Images for specific amenities in each project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='amenity_images')
    amenity_name = models.CharField(max_length=100, help_text="e.g. Swimming Pool, Gym, Clubhouse")
    image = models.ImageField(upload_to='project/amenities/', help_text="Upload amenity image")
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['project', 'amenity_name', 'uploaded_at']
        verbose_name = "Project Amenity Image"
        verbose_name_plural = "Project Amenity Images"
    
    def __str__(self):
        return f"{self.project.name} - {self.amenity_name}"

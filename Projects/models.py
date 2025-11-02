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
    feature_image = models.ImageField(upload_to='amenities/images/', blank=True, null=True, help_text="Amenity feature image")
    font_awesome_icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class (e.g., fas fa-swimming-pool)")
    
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
    
    def get_default_icon_class(self):
        """Return default Font Awesome icon class based on amenity name"""
        name_lower = self.name.lower()
        icon_mapping = {
            'swimming pool': 'fas fa-swimmer',
            'pool': 'fas fa-swimmer',
            'gym': 'fas fa-dumbbell',
            'fitness': 'fas fa-dumbbell',
            'parking': 'fas fa-car',
            'security': 'fas fa-shield-alt',
            'playground': 'fas fa-child',
            'garden': 'fas fa-leaf',
            'clubhouse': 'fas fa-building',
            'community hall': 'fas fa-building',
            'lift': 'fas fa-elevator',
            'elevator': 'fas fa-elevator',
            'power backup': 'fas fa-bolt',
            'generator': 'fas fa-bolt',
            'cctv': 'fas fa-video',
            'intercom': 'fas fa-phone',
            'wifi': 'fas fa-wifi',
            'tennis': 'fas fa-table-tennis',
            'badminton': 'fas fa-shuttlecock',
            'basketball': 'fas fa-basketball-ball',
            'jogging': 'fas fa-running',
            'yoga': 'fas fa-meditate',
            'spa': 'fas fa-spa',
            'library': 'fas fa-book',
            'restaurant': 'fas fa-utensils',
            'cafe': 'fas fa-coffee',
        }
        
        # Try to find matching icon
        for key, icon in icon_mapping.items():
            if key in name_lower:
                return icon
        
        return self.font_awesome_icon or 'fas fa-star'


class Project(models.Model):
    """Main Project model with all primary fields"""
    
    STATUS_CHOICES = [
        ('ready_to_move', 'Ready to Move'),
        ('under_construction', 'Under Construction'),
        ('upcoming_project', 'Upcoming Project'),
        ('possession_soon', 'Possession Soon'),
        ('sold_out', 'Sold Out'),
        ('new_launched', 'New Launched'),
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
    total_area = models.CharField(max_length=100, help_text="e.g. 5.2 Acres", blank=True, null=True)
    bhk = models.CharField(max_length=50, help_text="e.g. 2, 3, 4 BHK", blank=True, null=True)
    no_of_blocks = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    tower_count = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True, help_text="Number of towers/blocks")
    no_of_units = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    rera_number = models.CharField(max_length=100, blank=True, null=True, help_text="RERA approval number")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_construction', blank=True, null=True)
    possession_date = models.DateField(blank=True, null=True)
    onwards_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    
    # Contact Information
    contact_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Primary contact number")
    contact_email = models.EmailField(blank=True, null=True, help_text="Contact email")
    sales_office_address = models.TextField(blank=True, null=True, help_text="Sales office address")
    
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
    is_sell = models.BooleanField(default=False, help_text="Available for Sell")
    is_rent = models.BooleanField(default=False, help_text="Available for Rent") 
    is_lease = models.BooleanField(default=False, help_text="Available for Lease")
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
    display_order = models.PositiveIntegerField(default=0, help_text="Display position (lower number = higher priority). Use 0 for default ordering by created date.")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['display_order', '-created_at']),
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

    def approved_reviews_count(self):
        """Return count of approved reviews for this project"""
        return getattr(self, 'reviews', None) and self.reviews.filter(approved=True).count() or 0

    def approved_reviews(self):
        """Return approved reviews (limited to 6 for display)"""
        qs = getattr(self, 'reviews', None)
        if not qs:
            return []
        return qs.filter(approved=True)[:6]

    def average_rating(self):
        """Return average rating (1-5) of approved reviews, or None"""
        qs = getattr(self, 'reviews', None)
        if not qs:
            return None
        approved = qs.filter(approved=True)
        if not approved.exists():
            return None
        return round(approved.aggregate(models.Avg('rating'))['rating__avg'], 1)


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


class AreaType(models.Model):
    """Dynamic Area Types for Nearest Areas"""
    name = models.CharField(max_length=100, unique=True, help_text="e.g. School, Hospital, Metro Station")
    icon = models.ImageField(upload_to='area_types/icons/', blank=True, null=True, help_text="Area type icon")
    font_awesome_icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class (e.g., fas fa-school)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Area Type"
        verbose_name_plural = "Area Types"
    
    def __str__(self):
        return self.name
    
    def get_default_icon_class(self):
        """Return default Font Awesome icon class based on area type name"""
        name_lower = self.name.lower()
        icon_mapping = {
            'school': 'fas fa-graduation-cap',
            'hospital': 'fas fa-hospital',
            'clinic': 'fas fa-clinic-medical',
            'metro': 'fas fa-subway',
            'metro station': 'fas fa-subway',
            'mall': 'fas fa-shopping-bag',
            'shopping mall': 'fas fa-shopping-bag',
            'restaurant': 'fas fa-utensils',
            'park': 'fas fa-tree',
            'airport': 'fas fa-plane',
            'bus stop': 'fas fa-bus',
            'bank': 'fas fa-university',
            'atm': 'fas fa-credit-card',
            'gym': 'fas fa-dumbbell',
            'temple': 'fas fa-pray',
            'church': 'fas fa-cross',
            'mosque': 'fas fa-moon',
            'college': 'fas fa-university',
            'university': 'fas fa-university',
            'pharmacy': 'fas fa-pills',
            'supermarket': 'fas fa-shopping-cart',
            'police station': 'fas fa-shield-alt',
            'fire station': 'fas fa-fire-extinguisher',
            'cinema': 'fas fa-film',
            'theater': 'fas fa-theater-masks',
        }
        
        # Try to find matching icon
        for key, icon in icon_mapping.items():
            if key in name_lower:
                return icon
        
        return self.font_awesome_icon or 'fas fa-map-marker-alt'


class NearestArea(models.Model):
    """Nearby areas like Schools, Hospitals, Metro"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='nearest_areas')
    name = models.CharField(max_length=200)
    area_type = models.ForeignKey('AreaType', on_delete=models.CASCADE, related_name='nearest_areas', help_text="Select area type")
    distance = models.CharField(max_length=50, blank=True, help_text="e.g. 2 km, 5 min walk")
    icon = models.ImageField(upload_to='locations/icons/', blank=True, null=True, help_text="Location type icon (optional, overrides area type icon)")
    
    class Meta:
        ordering = ['area_type__order', 'name']
        verbose_name = "Nearest Area"
        verbose_name_plural = "Nearest Areas"
    
    def __str__(self):
        return f"{self.name} ({self.area_type.name})"
    
    def get_default_icon_class(self):
        """Return default Font Awesome icon class based on area type"""
        if self.area_type:
            return self.area_type.get_default_icon_class()
        return 'fas fa-map-marker-alt'


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


class ProjectReview(models.Model):
    """Admin-managed reviews for projects."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=150, help_text='Name of reviewer')
    rating = models.PositiveSmallIntegerField(default=5, help_text='Rating 1-5')
    comment = models.TextField(blank=True, null=True, help_text='Review comment')
    approved = models.BooleanField(default=True, help_text='Mark true to display on frontend')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Review'
        verbose_name_plural = 'Project Reviews'

    def __str__(self):
        return f"{self.project.name} - {self.reviewer_name} ({self.rating}★)"
    
    def get_star_display(self):
        """Return star rating as visual stars"""
        return '⭐' * self.rating


class ProjectInquiry(models.Model):
    """Track project inquiries and appointment requests"""
    INTEREST_CHOICES = [
        ('buying', 'Buying'),
        ('investment', 'Investment'),
        ('site_visit', 'Schedule Site Visit'),
        ('floor_plans', 'Floor Plans'),
        ('pricing', 'Pricing Details'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    
    # Appointment fields (for site visit)
    appointment_date = models.DateField(blank=True, null=True, help_text="Preferred appointment date")
    appointment_time = models.CharField(max_length=20, blank=True, null=True, help_text="Preferred appointment time")
    
    # Tracking fields
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Status tracking
    is_contacted = models.BooleanField(default=False, help_text="Mark as contacted")
    contacted_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="Admin notes")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project Inquiry"
        verbose_name_plural = "Project Inquiries"
        indexes = [
            models.Index(fields=['project', 'email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_contacted']),
        ]
    
    def __str__(self):
        if self.appointment_date:
            return f"{self.project.name} - {self.name} - Site Visit on {self.appointment_date}"
        return f"{self.project.name} - {self.name} - {self.get_interest_display() if self.interest else 'Inquiry'}"


class FloorPlanAccess(models.Model):
    """Track user contact details for floor plan access"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='floor_plan_accesses')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    accessed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-accessed_at']
        verbose_name = "Floor Plan Access"
        verbose_name_plural = "Floor Plan Accesses"
        # Allow multiple access records per project-email combination for tracking
        indexes = [
            models.Index(fields=['project', 'email']),
            models.Index(fields=['accessed_at']),
        ]
    
    def __str__(self):
        return f"{self.project.name} - {self.email} - {self.accessed_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def has_access(cls, project, email):
        """Check if user has already provided contact details for this project"""
        return cls.objects.filter(project=project, email=email).exists()

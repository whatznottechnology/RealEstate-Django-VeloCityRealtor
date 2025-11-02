from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Project, City, Category, ProjectType, Tag, Amenity, 
    ProjectOverview, GalleryImage, NearestArea, FloorPlan, 
    ConstructionUpdate, WhyChooseUs, SpecificationCategory, 
    SpecificationItem, ProjectAmenityImage, FloorPlanAccess, AreaType,
    ProjectInquiry
)
from django import forms
from django.db import models as dj_models
from .models import ProjectReview


# Inline Admin Classes
class ProjectOverviewInline(StackedInline):
    model = ProjectOverview
    extra = 0
    max_num = 1
    verbose_name = "📝 Project Overview"
    verbose_name_plural = "📝 Project Overview"
    fieldsets = (
        (None, {
            'fields': ('title', 'short_description'),
            'description': 'Main project overview and description for marketing'
        }),
    )


class GalleryImageInline(TabularInline):
    model = GalleryImage
    extra = 1
    verbose_name = "🖼️ Gallery Image"
    verbose_name_plural = "🖼️ Gallery Images"
    fields = ('image_preview', 'image', 'caption', 'order', 'is_active', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


class NearestAreaInline(TabularInline):
    model = NearestArea
    extra = 1
    verbose_name = "📍 Nearby Location"
    verbose_name_plural = "📍 Nearby Locations"


class FloorPlanInline(TabularInline):
    model = FloorPlan
    extra = 1
    verbose_name = "📐 Floor Plan"
    verbose_name_plural = "📐 Floor Plans"
    fields = ('image_preview', 'name', 'image', 'area', 'price', 'order', 'is_active')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


class ConstructionUpdateInline(TabularInline):
    model = ConstructionUpdate
    extra = 1
    verbose_name = "🏗️ Construction Update"
    verbose_name_plural = "🏗️ Construction Updates"
    fields = ('image_preview', 'title', 'image', 'update_date', 'description', 'order')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


class WhyChooseUsInline(TabularInline):
    model = WhyChooseUs
    extra = 1
    verbose_name = "⭐ Why Choose Us"
    verbose_name_plural = "⭐ Why Choose Us Points"
    fields = ('title', 'description', 'icon', 'order')


class SpecificationItemInline(TabularInline):
    model = SpecificationItem
    extra = 1
    verbose_name = "📋 Specification"
    verbose_name_plural = "📋 Specifications"
    fields = ('category', 'name', 'description', 'order')


class ProjectAmenityImageInline(TabularInline):
    model = ProjectAmenityImage
    extra = 1
    verbose_name = "🏊 Amenity Image"
    verbose_name_plural = "🏊 Amenity Images"
    fields = ('image_preview', 'amenity_name', 'image', 'is_active')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


class ProjectReviewInline(TabularInline):
    model = ProjectReview
    extra = 1
    max_num = 10
    fields = ('reviewer_name', 'rating', 'comment', 'approved')
    verbose_name = '📝 Project Review'
    verbose_name_plural = '📝 Project Reviews'


# Main Admin Classes
@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        'project_thumbnail', 'name', 'project_by', 'status_badge', 
        'formatted_price', 'feature_badges', 'edit_button', 'is_active'
    )
    list_display_links = ('project_thumbnail', 'name')
    list_editable = ()  # Removed display_order from inline editing
    list_filter = (
        'status', 'category', 'project_type', 'city', 'is_featured', 
        'is_active', 'is_most_viewed', 'is_nearby_property', 'is_recently_viewed',
        'is_hot_deal', 'is_premium_listing', 'is_editors_choice',
        'trending_tag', 'is_sell', 'is_rent', 'is_lease', 'tags', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'project_by', 'location', 'developers')
    readonly_fields = ('views', 'created_at', 'updated_at', 'project_preview')
    filter_horizontal = ('tags', 'amenities')
    list_per_page = 25
    list_max_show_all = 100
    list_select_related = ('city', 'category', 'project_type')
    prefetch_related = ('tags', 'amenities')  # Optimize feature badges query
    
    # Enable bulk actions and checkboxes
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    
    formfield_overrides = {
        dj_models.DecimalField: {'widget': forms.NumberInput(attrs={'step': '0.01'})},
    }
    
    # Custom display methods
    def project_thumbnail(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" width="300" height="200" style="border-radius: 8px; object-fit: cover; box-shadow: 0 3px 8px rgba(0,0,0,0.15);" />',
                obj.banner_image.url
            )
        return format_html('<div style="width:300px;height:200px;background:#f0f0f0;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#666;">No Image</div>')
    project_thumbnail.short_description = '🖼️ Image'
    project_thumbnail.admin_order_field = 'banner_image'
    project_thumbnail.allow_tags = True
    
    def status_badge(self, obj):
        colors = {
            'ready_to_move': '#28a745',
            'under_construction': '#ffc107', 
            'upcoming_project': '#17a2b8',
            'possession_soon': '#6f42c1',
            'sold_out': '#dc3545',
            'new_launched': '#fd7e14'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; white-space: nowrap;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = '📊 Status'
    status_badge.allow_tags = True
    
    def formatted_price(self, obj):
        if obj.onwards_price:
            price = float(obj.onwards_price)
            if price >= 10000000:  # 1 crore
                formatted = f'₹{price / 10000000:.1f}Cr'
                return format_html('<strong>{}</strong>', formatted)
            elif price >= 100000:  # 1 lakh
                formatted = f'₹{price / 100000:.1f}L'
                return format_html('<strong>{}</strong>', formatted)
            else:
                formatted = f'₹{price:,.0f}'
                return format_html('<strong>{}</strong>', formatted)
        return '-'
    formatted_price.short_description = '💰 Price'
    formatted_price.allow_tags = True
    
    def reviews_count(self, obj):
        total_count = obj.reviews.count()
        approved_count = obj.approved_reviews_count()
        if total_count > 0:
            return format_html(
                '<div style="text-align: center;">'
                '<span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 10px; font-size: 11px; margin-right: 4px;">'
                '✓ {}</span>'
                '<span style="background: #ffc107; color: #333; padding: 2px 6px; border-radius: 10px; font-size: 11px;">'
                '⏳ {}</span>'
                '</div>',
                approved_count,
                total_count - approved_count
            )
        return format_html('<span style="color: #6c757d; font-size: 11px;">No reviews</span>')
    reviews_count.short_description = '⭐ Reviews'
    reviews_count.allow_tags = True
    
    def feature_badges(self, obj):
        badges = []
        
        # Show only primary/most important features (max 4)
        if obj.is_featured:
            badges.append('<span style="background: #3b82f6; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin: 2px;">★ Featured</span>')
        if obj.is_premium_listing:
            badges.append('<span style="background: #f59e0b; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin: 2px;">👑 Premium</span>')
        if obj.is_hot_deal:
            badges.append('<span style="background: #ef4444; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin: 2px;">� Hot Deal</span>')
        if obj.is_editors_choice:
            badges.append('<span style="background: #8b5cf6; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin: 2px;">✨ Editor\'s Choice</span>')
        
        # Count remaining features
        other_features = 0
        if obj.is_most_viewed:
            other_features += 1
        if obj.is_nearby_property:
            other_features += 1
        if obj.is_recently_viewed:
            other_features += 1
        if obj.trending_tag:
            other_features += 1
        
        tags_count = obj.tags.count()
        if tags_count > 0:
            other_features += tags_count
        
        # Show "more" indicator if there are additional features
        if other_features > 0:
            badges.append(f'<span style="background: #6b7280; color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin: 2px;">+{other_features} more</span>')
        
        if badges:
            return mark_safe(f'<div style="max-width: 250px;">{"".join(badges)}</div>')
        return mark_safe('<span style="color: #9ca3af; font-size: 11px;">None</span>')
    feature_badges.short_description = '🏷️ Features'
    feature_badges.allow_tags = True
    
    def project_preview(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />',
                obj.banner_image.url
            )
        return "No banner image"
    project_preview.short_description = 'Project Banner Preview'
    
    def reviews_count(self, obj):
        count = obj.approved_reviews_count()
        avg_rating = obj.average_rating()
        if count > 0 and avg_rating:
            return format_html(
                '<div style="text-align: center;">'
                '<div style="font-weight: bold; color: #dc2626;">{} Reviews</div>'
                '<div style="font-size: 11px; color: #059669;">⭐ {} avg</div>'
                '</div>',
                count, avg_rating
            )
        elif count > 0:
            return format_html(
                '<div style="text-align: center; font-weight: bold; color: #dc2626;">{} Reviews</div>',
                count
            )
        return format_html('<span style="color: #9ca3af;">No reviews</span>')
    reviews_count.short_description = '📝 Reviews'
    reviews_count.allow_tags = True

    def edit_button(self, obj):
        from django.urls import reverse
        # Get public URL using slug
        public_url = obj.get_absolute_url() if obj.slug else '#'
        
        return format_html(
            '<div style="display: flex; gap: 5px; flex-wrap: nowrap;">'
            '<a href="{}" style="background: #3b82f6; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 11px; white-space: nowrap; display: inline-block;">✏️ Edit</a>'
            '<a href="{}" target="_blank" style="background: #10b981; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 11px; white-space: nowrap; display: inline-block;">👁️ View on Site</a>'
            '</div>',
            reverse('admin:Projects_project_change', args=[obj.pk]),
            public_url
        )
    edit_button.short_description = '⚙️ Actions'
    edit_button.allow_tags = True

    # Form organization
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('name', 'slug', 'project_by', 'logo', 'banner_image', 'project_preview', 'brochure'),
            'classes': ('wide',),
            'description': 'Core project details and media files'
        }),
        ('📍 Location & Map', {
            'fields': ('location', 'city', 'developers', 'latitude', 'longitude'),
            'classes': ('wide',),
            'description': 'Location details and map coordinates for project location'
        }),
        ('🏗️ Project Specifications', {
            'fields': (
                ('build_up_area', 'total_area'),
                ('bhk', 'no_of_blocks', 'tower_count'),
                ('no_of_units', 'rera_number'),
                ('status', 'possession_date'),
                'onwards_price'
            ),
            'classes': ('wide',),
            'description': 'Technical specifications and project details'
        }),
        ('📞 Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'sales_office_address'),
            'classes': ('wide',),
            'description': 'Contact details for project inquiries'
        }),
        ('🏷️ Categorization & Features', {
            'fields': (
                ('category', 'project_type'),
                'tags',
                'amenities'
            ),
            'classes': ('wide',),
            'description': 'Project category, type, tags and amenities'
        }),
        ('🎯 Marketing & Promotional Tags', {
            'fields': (
                ('is_sell', 'is_rent', 'is_lease'),
                ('is_featured', 'is_hot_deal', 'is_premium_listing'),
                ('is_editors_choice', 'is_most_viewed'),
                ('trending_tag',),
                ('is_nearby_property', 'is_recently_viewed')
            ),
            'classes': ('wide',),
            'description': 'Enable promotional badges and marketing features that appear on project cards in the frontend'
        }),
        ('📊 SEO & Metadata', {
            'fields': ('description', 'meta_title', 'meta_description', 'keywords'),
            'classes': ('wide', 'collapse'),
            'description': 'Search Engine Optimization fields for better discoverability in search results'
        }),
        ('📈 Display Settings & Tracking', {
            'fields': (
                ('display_order', 'is_active'),
                ('views',),
                ('created_at', 'updated_at')
            ),
            'classes': ('wide', 'collapse'),
            'description': 'Display order controls project position (lower numbers appear first). Use 0 for default ordering by date.'
        }),
    )
    
    # Inline models for related data
    inlines = [
        ProjectOverviewInline,
        GalleryImageInline,
        NearestAreaInline,
        FloorPlanInline,
        ConstructionUpdateInline,
        WhyChooseUsInline,
        SpecificationItemInline,
        ProjectAmenityImageInline,
        ProjectReviewInline,
    ]


@admin.register(ProjectReview)
class ProjectReviewAdmin(ModelAdmin):
    list_display = ('project', 'reviewer_name', 'rating_stars', 'approved', 'created_at')
    list_filter = ('approved', 'rating', 'created_at', 'project')
    search_fields = ('reviewer_name', 'comment', 'project__name')
    readonly_fields = ('created_at',)
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html(f'{stars} ({obj.rating}/5)')
    rating_stars.short_description = 'Rating'


# Continue with other admin classes...
@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ('city_icon', 'name', 'state', 'country', 'project_count', 'status_badge', 'created_at')
    list_display_links = ('city_icon', 'name')
    list_filter = ('country', 'state', 'is_active', 'created_at')
    search_fields = ('name', 'state', 'country', 'description', 'keywords')
    readonly_fields = ('created_at', 'icon_preview')
    list_per_page = 25
    
    fieldsets = (
        ('📍 Basic Information', {
            'fields': ('name', 'state', 'country', 'icon', 'icon_preview', 'is_active'),
            'classes': ('wide',),
        }),
        ('📊 SEO & Metadata', {
            'fields': ('description', 'meta_title', 'meta_description', 'keywords'),
            'classes': ('wide', 'collapse'),
            'description': 'Search Engine Optimization fields for better discoverability'
        }),
        ('📅 Timestamps', {
            'fields': ('created_at',),
            'classes': ('wide', 'collapse'),
        }),
    )
    
    def city_icon(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.icon.url
            )
        return format_html('<div style="width:40px;height:40px;background:#f0f0f0;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;color:#666;">🏙️</div>')
    city_icon.short_description = '🖼️ Icon'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; border-radius: 8px;" />',
                obj.icon.url
            )
        return "No icon uploaded"
    icon_preview.short_description = 'Icon Preview'


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'project_count', 'project_type_count', 'created_at')
    search_fields = ('name', 'description', 'keywords')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('📁 Basic Information', {
            'fields': ('name',),
            'classes': ('wide',),
        }),
        ('📊 SEO & Metadata', {
            'fields': ('description', 'meta_title', 'meta_description', 'keywords'),
            'classes': ('wide', 'collapse'),
            'description': 'Search Engine Optimization fields for better discoverability'
        }),
        ('📅 Timestamps', {
            'fields': ('created_at',),
            'classes': ('wide', 'collapse'),
        }),
    )
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'
    
    def project_type_count(self, obj):
        return obj.project_types.count()
    project_type_count.short_description = 'Project Types'


@admin.register(ProjectType)
class ProjectTypeAdmin(ModelAdmin):
    list_display = ('name', 'category', 'project_count', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name', 'description', 'keywords')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('🏠 Basic Information', {
            'fields': ('name', 'category'),
            'classes': ('wide',),
        }),
        ('📊 SEO & Metadata', {
            'fields': ('description', 'meta_title', 'meta_description', 'keywords'),
            'classes': ('wide', 'collapse'),
            'description': 'Search Engine Optimization fields for better discoverability'
        }),
        ('📅 Timestamps', {
            'fields': ('created_at',),
            'classes': ('wide', 'collapse'),
        }),
    )
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('tag_preview', 'name', 'project_count', 'status_badge', 'created_at')
    list_display_links = ('tag_preview', 'name')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    
    def tag_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            obj.color, obj.name
        )
    tag_preview.short_description = '🏷️ Preview'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


@admin.register(Amenity)
class AmenityAdmin(ModelAdmin):
    list_display = ('amenity_icon', 'name', 'project_count', 'status_badge', 'created_at')
    list_display_links = ('amenity_icon', 'name')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'keywords')
    readonly_fields = ('created_at', 'icon_preview')
    list_per_page = 25
    
    fieldsets = (
        ('🏊 Basic Information', {
            'fields': ('name', 'icon', 'icon_preview', 'is_active'),
            'classes': ('wide',),
        }),
        ('📊 SEO & Metadata', {
            'fields': ('description', 'meta_title', 'meta_description', 'keywords'),
            'classes': ('wide', 'collapse'),
            'description': 'Search Engine Optimization fields for better discoverability'
        }),
        ('📅 Timestamps', {
            'fields': ('created_at',),
            'classes': ('wide', 'collapse'),
        }),
    )
    
    def amenity_icon(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.icon.url
            )
        return format_html('<div style="width:40px;height:40px;background:#f0f0f0;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;color:#666;">🏊</div>')
    amenity_icon.short_description = '🖼️ Icon'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; border-radius: 8px;" />',
                obj.icon.url
            )
        return "No icon uploaded"
    icon_preview.short_description = 'Icon Preview'


# Register all other models with basic admin
@admin.register(ProjectOverview)
class ProjectOverviewAdmin(ModelAdmin):
    list_display = ('project', 'title')
    search_fields = ('project__name', 'title')


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    list_display = ('image_thumbnail', 'project', 'caption', 'order', 'status_badge', 'uploaded_at')
    list_display_links = ('image_thumbnail', 'caption')
    list_filter = ('is_active', 'uploaded_at', 'project')
    search_fields = ('project__name', 'caption')
    readonly_fields = ('uploaded_at', 'image_preview')
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = '🖼️ Thumbnail'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = 'Image Preview'


@admin.register(FloorPlan)
class FloorPlanAdmin(ModelAdmin):
    list_display = ('plan_thumbnail', 'project', 'name', 'area', 'formatted_price', 'order', 'status_badge')
    list_display_links = ('plan_thumbnail', 'name')
    list_filter = ('is_active', 'project')
    search_fields = ('project__name', 'name', 'area')
    readonly_fields = ('image_preview',)
    
    def plan_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    plan_thumbnail.short_description = '📐 Plan'
    
    def formatted_price(self, obj):
        if obj.price:
            price = float(obj.price)
            if price >= 10000000:  # 1 crore
                formatted = f'₹{price / 10000000:.1f}Cr'
                return format_html('<strong>{}</strong>', formatted)
            elif price >= 100000:  # 1 lakh
                formatted = f'₹{price / 100000:.1f}L'
                return format_html('<strong>{}</strong>', formatted)
            else:
                formatted = f'₹{price:,.0f}'
                return format_html('<strong>{}</strong>', formatted)
        return '-'
    formatted_price.short_description = '💰 Price'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 300px; border-radius: 8px;" />',
                obj.image.url
            )
        return "No floor plan image uploaded"
    image_preview.short_description = 'Floor Plan Preview'


@admin.register(NearestArea)
class NearestAreaAdmin(ModelAdmin):
    list_display = ('project', 'name', 'area_type', 'distance')
    list_filter = ('area_type', 'project')
    search_fields = ('project__name', 'name')


@admin.register(ConstructionUpdate)
class ConstructionUpdateAdmin(ModelAdmin):
    list_display = ('project', 'title', 'update_date', 'order')
    list_filter = ('update_date', 'project')
    search_fields = ('project__name', 'title')
    date_hierarchy = 'update_date'


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(ModelAdmin):
    list_display = ('project', 'title', 'icon', 'order')
    list_filter = ('project',)
    search_fields = ('project__name', 'title')


@admin.register(SpecificationCategory)
class SpecificationCategoryAdmin(ModelAdmin):
    list_display = ('name', 'order', 'item_count', 'status_badge')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order', 'name')
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(SpecificationItem)
class SpecificationItemAdmin(ModelAdmin):
    list_display = ('project', 'category', 'name', 'order')
    list_filter = ('category', 'project')
    search_fields = ('project__name', 'name', 'description')


@admin.register(ProjectAmenityImage)
class ProjectAmenityImageAdmin(ModelAdmin):
    list_display = ('image_thumbnail', 'project', 'amenity_name', 'status_badge', 'uploaded_at')
    list_display_links = ('image_thumbnail', 'amenity_name')
    list_filter = ('is_active', 'uploaded_at', 'project')
    search_fields = ('project__name', 'amenity_name')
    readonly_fields = ('uploaded_at', 'image_preview')
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = '🖼️ Thumbnail'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = 'Image Preview'


@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(ModelAdmin):
    list_display = ('project_name', 'name', 'phone', 'interest_badge', 'appointment_info', 'status_badge', 'created_at')
    list_display_links = ('project_name', 'name')
    list_filter = ('interest', 'is_contacted', 'created_at', 'project', 'appointment_date')
    search_fields = ('project__name', 'name', 'email', 'phone', 'message')
    readonly_fields = ('ip_address', 'user_agent', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ()
    
    fieldsets = (
        ('📋 Project & Contact Information', {
            'fields': ('project', 'name', 'email', 'phone', 'interest')
        }),
        ('💬 Inquiry Details', {
            'fields': ('message',),
        }),
        ('📅 Appointment Details', {
            'fields': ('appointment_date', 'appointment_time'),
            'classes': ('collapse',),
            'description': 'Only filled when interest is "Schedule Site Visit"'
        }),
        ('✅ Status & Follow-up', {
            'fields': ('is_contacted', 'contacted_at', 'notes'),
        }),
        ('🔍 Technical Details', {
            'fields': ('ip_address', 'user_agent', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def project_name(self, obj):
        """Display project name in a cleaner format"""
        if obj.project:
            return format_html(
                '<div style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{}">{}</div>',
                obj.project.name,
                obj.project.name
            )
        return '-'
    project_name.short_description = 'Project'
    project_name.admin_order_field = 'project__name'
    
    def interest_badge(self, obj):
        colors = {
            'buying': '#28a745',
            'investment': '#ffc107',
            'site_visit': '#dc2626',
            'floor_plans': '#007bff',
            'pricing': '#6f42c1',
        }
        if obj.interest:
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; white-space: nowrap;">{}</span>',
                colors.get(obj.interest, '#6c757d'),
                obj.get_interest_display()
            )
        return format_html('<span style="color: #999;">-</span>')
    interest_badge.short_description = '🎯 Interest'
    interest_badge.allow_tags = True
    
    def appointment_info(self, obj):
        if obj.appointment_date and obj.appointment_time:
            return format_html(
                '<div style="text-align: center;">'
                '<div style="font-weight: bold; color: #dc2626;">📅 {}</div>'
                '<div style="font-size: 11px; color: #059669;">🕐 {}</div>'
                '</div>',
                obj.appointment_date.strftime('%b %d, %Y'),
                obj.appointment_time
            )
        return format_html('<span style="color: #999;">-</span>')
    appointment_info.short_description = '📅 Appointment'
    appointment_info.allow_tags = True
    
    def status_badge(self, obj):
        if obj.is_contacted:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Contacted</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">⏳ Pending</span>'
        )
    status_badge.short_description = '📊 Status'
    status_badge.allow_tags = True
    
    actions = ['mark_as_contacted', 'mark_as_pending']
    
    def mark_as_contacted(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_contacted=True, contacted_at=timezone.now())
        self.message_user(request, f'{updated} inquiry(ies) marked as contacted.')
    mark_as_contacted.short_description = "✓ Mark selected as contacted"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(is_contacted=False, contacted_at=None)
        self.message_user(request, f'{updated} inquiry(ies) marked as pending.')
    mark_as_pending.short_description = "⏳ Mark selected as pending"


@admin.register(FloorPlanAccess)
class FloorPlanAccessAdmin(ModelAdmin):
    list_display = ('project', 'name', 'email', 'phone', 'accessed_at', 'access_count')
    list_display_links = ('name', 'email')
    list_filter = ('accessed_at', 'project')
    search_fields = ('project__name', 'name', 'email', 'phone')
    readonly_fields = ('ip_address', 'user_agent', 'accessed_at')
    date_hierarchy = 'accessed_at'
    ordering = ('-accessed_at',)
    
    fieldsets = (
        ('📞 Contact Information', {
            'fields': ('project', 'name', 'email', 'phone')
        }),
        ('💬 Message', {
            'fields': ('message',),
            'classes': ('collapse',)
        }),
        ('🔍 Technical Details', {
            'fields': ('ip_address', 'user_agent', 'accessed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def access_count(self, obj):
        count = FloorPlanAccess.objects.filter(project=obj.project, email=obj.email).count()
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{} times</span>',
            count
        )
    access_count.short_description = '🔄 Access Count'
    
    def has_add_permission(self, request):
        # Usually floor plan access records are created through the website
        return False


@admin.register(AreaType)
class AreaTypeAdmin(ModelAdmin):
    list_display = ('area_icon', 'name', 'nearest_area_count', 'status_badge', 'order', 'created_at')
    list_display_links = ('area_icon', 'name')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'font_awesome_icon')
    readonly_fields = ('created_at', 'icon_preview')
    list_per_page = 25
    ordering = ('order', 'name')
    
    fieldsets = (
        ('📍 Basic Information', {
            'fields': ('name', 'icon', 'icon_preview', 'font_awesome_icon', 'order', 'is_active'),
            'classes': ('wide',),
        }),
        ('📅 Timestamps', {
            'fields': ('created_at',),
            'classes': ('wide', 'collapse'),
        }),
    )
    
    def area_icon(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.icon.url
            )
        icon_class = obj.get_default_icon_class()
        return format_html('<div style="width:40px;height:40px;background:#f0f0f0;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;color:#666;"><i class="{}"></i></div>', icon_class)
    area_icon.short_description = '🖼️ Icon'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Inactive</span>')
    status_badge.short_description = '📊 Status'
    
    def nearest_area_count(self, obj):
        return obj.nearest_areas.count()
    nearest_area_count.short_description = 'Used in'
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; border-radius: 8px;" />',
                obj.icon.url
            )
        return "No icon uploaded"
    icon_preview.short_description = 'Icon Preview'


# Jazzmin Admin Site Configuration
admin.site.site_header = "VeloCity"
admin.site.site_title = "VeloCity"
admin.site.index_title = "VeloCity"

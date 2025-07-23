from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Project, City, Category, ProjectType, Tag, Amenity, 
    ProjectOverview, GalleryImage, NearestArea, FloorPlan, 
    ConstructionUpdate, WhyChooseUs, SpecificationCategory, 
    SpecificationItem, ProjectAmenityImage
)


# Inline Admin Classes
class ProjectOverviewInline(admin.StackedInline):
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


class GalleryImageInline(admin.TabularInline):
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


class NearestAreaInline(admin.TabularInline):
    model = NearestArea
    extra = 1
    verbose_name = "📍 Nearby Location"
    verbose_name_plural = "📍 Nearby Locations"


class FloorPlanInline(admin.TabularInline):
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


class ConstructionUpdateInline(admin.TabularInline):
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


class WhyChooseUsInline(admin.TabularInline):
    model = WhyChooseUs
    extra = 1
    verbose_name = "⭐ Why Choose Us"
    verbose_name_plural = "⭐ Why Choose Us Points"
    fields = ('title', 'description', 'icon', 'order')


class SpecificationItemInline(admin.TabularInline):
    model = SpecificationItem
    extra = 1
    verbose_name = "📋 Specification"
    verbose_name_plural = "📋 Specifications"
    fields = ('category', 'name', 'description', 'order')


class ProjectAmenityImageInline(admin.TabularInline):
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


# Main Admin Classes
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_thumbnail', 'name', 'project_by', 'city', 'status_badge', 
        'bhk', 'formatted_price', 'views', 'feature_badges', 'edit_button', 'is_active', 'created_at'
    )
    list_display_links = ('project_thumbnail', 'name')
    list_filter = (
        'status', 'category', 'project_type', 'city', 'is_featured', 
        'is_active', 'is_most_viewed', 'is_nearby_property', 'is_recently_viewed',
        'is_hot_deal', 'is_premium_listing', 'is_editors_choice',
        'trending_tag', 'tags', 'created_at', 'updated_at'
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
    
    # Add custom CSS classes for columns
    def get_list_display(self, request):
        return super().get_list_display(request)
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
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
            'upcoming': '#17a2b8',
            'sold_out': '#dc3545'
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
    
    def feature_badges(self, obj):
        badges = []
        
        # Primary feature badges
        if obj.is_featured:
            badges.append('<span class="badge badge-featured">★ Featured</span>')
        if obj.is_most_viewed:
            badges.append('<span class="badge badge-most-viewed">👁️ Most Viewed</span>')
        if obj.is_hot_deal:
            badges.append('<span class="badge badge-hot-deal">🔥 Hot Deal</span>')
        if obj.is_premium_listing:
            badges.append('<span class="badge badge-premium">👑 Premium</span>')
        if obj.is_editors_choice:
            badges.append('<span class="badge badge-editors-choice">✨ Editor\'s Choice</span>')
        
        # Secondary feature badges
        if obj.is_nearby_property:
            badges.append('<span class="badge badge-nearby">📍 Nearby</span>')
        if obj.is_recently_viewed:
            badges.append('<span class="badge badge-recent">⏰ Recent</span>')
        
        # Trending tag badge
        if obj.trending_tag:
            trend_class = f'badge-trend-{obj.trending_tag.replace("_", "-")}'
            badges.append(f'<span class="badge {trend_class}">🎯 {obj.get_trending_tag_display()}</span>')
        
        # Tags from ManyToMany field
        for tag in obj.tags.all()[:3]:  # Limit to first 3 tags to avoid overcrowding
            badges.append(f'<span class="badge badge-tag" style="background-color: {tag.color};">🏷️ {tag.name}</span>')
        
        if obj.tags.count() > 3:
            badges.append(f'<span class="badge badge-more">+{obj.tags.count() - 3} more</span>')
        
        if badges:
            html_content = f'<div class="feature-badges-container">{"".join(badges)}</div>'
            return mark_safe(html_content)
        return mark_safe('<span class="no-features">No features</span>')
    feature_badges.short_description = '🏷️ Features & Tags'
    feature_badges.allow_tags = True
    
    def project_preview(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />',
                obj.banner_image.url
            )
        return "No banner image"
    project_preview.short_description = 'Project Banner Preview'
    
    def edit_button(self, obj):
        from django.urls import reverse
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="button" style="background: #007cba; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">✏️ Edit</a>'
            '<a href="{}" class="button" style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">👁️ View Details</a>'
            '</div>',
            reverse('admin:Projects_project_change', args=[obj.pk]),
            f'/projects/project/{obj.pk}/detail/'
        )
    edit_button.short_description = '⚙️ Actions'
    edit_button.allow_tags = True

    # Form organization
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('name', 'project_by', 'logo', 'banner_image', 'project_preview', 'brochure'),
            'classes': ('wide',),
        }),
        ('📍 Location Details', {
            'fields': ('location', 'city', 'developers', 'latitude', 'longitude'),
            'classes': ('wide',),
        }),
        ('🏗️ Project Specifications', {
            'fields': ('build_up_area', 'bhk', 'no_of_blocks', 'no_of_units', 'status', 'possession_date', 'onwards_price'),
            'classes': ('wide',),
        }),
        ('🏷️ Categorization', {
            'fields': ('category', 'project_type', 'tags', 'amenities'),
            'classes': ('wide',),
        }),
        ('🎯 Marketing & Promotion', {
            'fields': (
                ('is_featured', 'is_most_viewed', 'is_hot_deal'),
                ('is_premium_listing', 'is_editors_choice', 'trending_tag'),
                ('is_nearby_property', 'is_recently_viewed')
            ),
            'classes': ('wide',),
        }),
        ('📊 SEO & Metadata', {
            'fields': ('description', 'meta_title', 'meta_description', 'keywords'),
            'classes': ('wide', 'collapse'),
            'description': 'Search Engine Optimization fields for better discoverability'
        }),
        ('📈 Tracking', {
            'fields': ('views', 'is_active', 'created_at', 'updated_at'),
            'classes': ('wide', 'collapse'),
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
    ]


# Continue with other admin classes...
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
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
class CategoryAdmin(admin.ModelAdmin):
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
class ProjectTypeAdmin(admin.ModelAdmin):
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
class TagAdmin(admin.ModelAdmin):
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
class AmenityAdmin(admin.ModelAdmin):
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
class ProjectOverviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'title')
    search_fields = ('project__name', 'title')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
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
class FloorPlanAdmin(admin.ModelAdmin):
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
class NearestAreaAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'area_type', 'distance')
    list_filter = ('area_type', 'project')
    search_fields = ('project__name', 'name')


@admin.register(ConstructionUpdate)
class ConstructionUpdateAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'update_date', 'order')
    list_filter = ('update_date', 'project')
    search_fields = ('project__name', 'title')
    date_hierarchy = 'update_date'


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'icon', 'order')
    list_filter = ('project',)
    search_fields = ('project__name', 'title')


@admin.register(SpecificationCategory)
class SpecificationCategoryAdmin(admin.ModelAdmin):
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
class SpecificationItemAdmin(admin.ModelAdmin):
    list_display = ('project', 'category', 'name', 'order')
    list_filter = ('category', 'project')
    search_fields = ('project__name', 'name', 'description')


@admin.register(ProjectAmenityImage)
class ProjectAmenityImageAdmin(admin.ModelAdmin):
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


# Jazzmin Admin Site Configuration
admin.site.site_header = "VeloCity"
admin.site.site_title = "VeloCity"
admin.site.index_title = "VeloCity"

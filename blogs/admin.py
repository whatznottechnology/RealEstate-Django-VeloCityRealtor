from django.contrib import admin
from .models import Blog, Tag

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "created_at", "is_published")
    search_fields = ("title", "tags__name")
    list_filter = ("is_published", "tags")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'feature_image', 'tags', 'is_published')
        }),
        ('Meta Data', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)

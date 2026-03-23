"""
Admin configuration for the Storybook application.
Customizes the Django admin interface for managing stories.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Story, ReadingProgress


def reextract_text(modeladmin, request, queryset):
    """Admin action to re-extract text from PDFs."""
    from .views import extract_pdf_content
    for story in queryset:
        extract_pdf_content(story)
    modeladmin.message_user(request, f"Successfully re-extracted text from {queryset.count()} story(ies).")

reextract_text.short_description = "Re-extract text from selected stories"


def regenerate_moral_lessons(modeladmin, request, queryset):
    """Admin action to regenerate moral lessons."""
    from .views import generate_moral_lesson
    for story in queryset:
        generate_moral_lesson(story)
    modeladmin.message_user(request, f"Successfully regenerated moral lessons for {queryset.count()} story(ies).")

regenerate_moral_lessons.short_description = "Regenerate moral lessons for selected stories"


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Story model.
    Allows admins to manage storybook PDFs.
    """
    
    list_display = [
        'title',
        'category',
        'total_pages',
        'is_featured',
        'uploaded_at',
        'view_story_link'
    ]
    
    list_filter = [
        'category',
        'is_featured',
        'uploaded_at'
    ]
    
    search_fields = [
        'title',
        'description',
        'category'
    ]
    
    readonly_fields = [
        'uploaded_at',
        'total_pages',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'is_featured')
        }),
        ('Files', {
            'fields': ('pdf_file', 'cover_image')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'total_pages'),
            'classes': ('collapse',)
        }),
        ('AI Generated', {
            'fields': ('extracted_text', 'moral_lesson'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [reextract_text, regenerate_moral_lessons]
    
    def view_story_link(self, obj):
        """Add a link to view the story on the site."""
        if obj.pk:
            return format_html(
                '<a href="/read/{}/" target="_blank" class="btn btn-sm btn-primary">View Story</a>',
                obj.pk
            )
        return '-'
    view_story_link.short_description = 'Actions'
    
    def has_add_permission(self, request):
        """Only superusers can add stories."""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can change stories."""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete stories."""
        return request.user.is_superuser


@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    """
    Admin interface for ReadingProgress model.
    Read-only view of user reading progress.
    """
    
    list_display = [
        'user',
        'story',
        'last_page',
        'is_completed',
        'last_read'
    ]
    
    list_filter = [
        'is_completed',
        'last_read'
    ]
    
    search_fields = [
        'user__username',
        'story__title'
    ]
    
    readonly_fields = [
        'user',
        'story',
        'last_page',
        'last_read'
    ]
    
    def has_add_permission(self, request):
        """Reading progress is tracked automatically."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Reading progress is read-only."""
        return False

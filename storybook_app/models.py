"""
Models for the Storybook application.
Defines the Story model for storing PDF storybooks.
"""

from django.db import models
from django.utils import timezone


class Story(models.Model):
    """
    Model representing a storybook PDF.
    Admin users can upload PDFs which are then available for all users to read.
    """
    
    title = models.CharField(
        max_length=200,
        help_text="Enter the title of the storybook"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Brief description of the story"
    )
    
    pdf_file = models.FileField(
        upload_to='pdfs/',
        help_text="Upload the PDF storybook file"
    )
    
    cover_image = models.ImageField(
        upload_to='covers/',
        blank=True,
        null=True,
        help_text="Optional cover image for the storybook"
    )
    
    uploaded_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the story was uploaded"
    )
    
    moral_lesson = models.TextField(
        blank=True,
        help_text="AI-generated moral lesson from the story"
    )
    
    total_pages = models.IntegerField(
        default=0,
        help_text="Total number of pages in the PDF"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as featured story"
    )
    
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Story category (e.g., Fables, Fairy Tales, Adventure)"
    )
    
    extracted_text = models.TextField(
        blank=True,
        help_text="Full text extracted from PDF for text-to-speech"
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        """Delete associated files when model is deleted."""
        if self.pdf_file:
            self.pdf_file.delete()
        if self.cover_image:
            self.cover_image.delete()
        super().delete(*args, **kwargs)


class ReadingProgress(models.Model):
    """
    Tracks user's reading progress for each story.
    Allows users to resume reading from where they left off.
    """
    
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='reading_progress'
    )
    
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='reading_progress'
    )
    
    last_page = models.IntegerField(default=0)
    last_read = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'story']
        ordering = ['-last_read']
    
    def __str__(self):
        return f"{self.user.username} - {self.story.title} (Page {self.last_page})"

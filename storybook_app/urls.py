"""
URL patterns for the Storybook application.
Maps URLs to views for the storybook web app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page - list all stories
    path('', views.StoryListView.as_view(), name='story-list'),
    
    # Story detail page
    path('story/<int:pk>/', views.StoryDetailView.as_view(), name='story-detail'),
    
    # Story viewer page (with flipbook/scroll reader)
    path('read/<int:pk>/', views.story_viewer, name='story-viewer'),
    
    # Create new story (admin only)
    path('story/create/', views.StoryCreateView.as_view(), name='story-create'),
    
    # Update story (admin only)
    path('story/<int:pk>/update/', views.StoryUpdateView.as_view(), name='story-update'),
    
    # Delete story (admin only)
    path('story/<int:pk>/delete/', views.StoryDeleteView.as_view(), name='story-delete'),
    
    # Save reading progress (authenticated users)
    path('save-progress/', views.save_reading_progress, name='save-progress'),
    
    # Get story text for text-to-speech
    path('api/story/<int:pk>/text/', views.get_story_text, name='story-text'),
    
    # User profile page
    path('accounts/profile/', views.profile_view, name='profile'),
    
    # About page
    path('about/', views.about_page, name='about'),
]

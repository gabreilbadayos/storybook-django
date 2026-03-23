"""
Forms for the Storybook application.
Handles form validation for story creation and updates.
"""

from django import forms
from .models import Story


class StoryForm(forms.ModelForm):
    """Form for creating and updating stories."""
    
    class Meta:
        model = Story
        fields = ['title', 'description', 'pdf_file', 'cover_image', 'category', 'is_featured']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter story title',
                'autofocus': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the story...'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Fables, Fairy Tales, Adventure'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_pdf_file(self):
        """Validate that the uploaded file is a PDF."""
        pdf_file = self.cleaned_data.get('pdf_file')
        
        if pdf_file:
            if not pdf_file.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            
            # Check file size (max 50MB)
            if pdf_file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 50MB.')
        
        return pdf_file

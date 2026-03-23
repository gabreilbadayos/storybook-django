"""
Views for the Storybook application.
Handles all HTTP requests for the storybook web app.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Story, ReadingProgress
from .forms import StoryForm
import PyPDF2
import pdfplumber
import os
from django.conf import settings
from io import BytesIO


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin/superuser access."""
    
    def test_func(self):
        return self.request.user.is_superuser


class StoryListView(ListView):
    """Display all available stories in a responsive grid."""
    model = Story
    template_name = 'storybook_app/home.html'
    context_object_name = 'stories'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Story.objects.all()
        
        # Filter by search query
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        # Filter by category
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category__iexact=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Story.objects.values_list('category', flat=True).distinct()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class StoryDetailView(DetailView):
    """Display story details and provide reading access."""
    model = Story
    template_name = 'storybook_app/story_detail.html'
    context_object_name = 'story'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Track reading progress for logged-in users
        if self.request.user.is_authenticated:
            progress, created = ReadingProgress.objects.get_or_create(
                user=self.request.user,
                story=self.object
            )
            context['reading_progress'] = progress
        
        return context


class StoryCreateView(AdminRequiredMixin, CreateView):
    """Allow admins to upload new stories."""
    model = Story
    form_class = StoryForm
    template_name = 'storybook_app/story_form.html'
    success_url = reverse_lazy('story-list')
    
    def form_valid(self, form):
        """Process the form and extract PDF content."""
        response = super().form_valid(form)
        
        story = self.object
        
        # Extract PDF information
        extract_pdf_content(story)
        
        # Generate moral lesson
        generate_moral_lesson(story)
        
        messages.success(self.request, f'Story "{story.title}" has been uploaded successfully!')
        return response


class StoryUpdateView(AdminRequiredMixin, UpdateView):
    """Allow admins to update stories."""
    model = Story
    form_class = StoryForm
    template_name = 'storybook_app/story_form.html'
    success_url = reverse_lazy('story-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Story "{form.instance.title}" has been updated!')
        return super().form_valid(form)


class StoryDeleteView(AdminRequiredMixin, DeleteView):
    """Allow admins to delete stories."""
    model = Story
    template_name = 'storybook_app/story_confirm_delete.html'
    success_url = reverse_lazy('story-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Story "{self.get_object().title}" has been deleted!')
        return super().delete(request, *args, **kwargs)


def about_page(request):
    """Display the about page."""
    return render(request, 'storybook_app/about.html')


def extract_pdf_content(story):
    """
    Extract text and page count from PDF.
    This is used for text-to-speech and moral lesson generation.
    """
    if not story.pdf_file:
        return
    
    pdf_path = story.pdf_file.path
    full_text = ""
    page_count = 0
    
    # Try PyPDF2 first
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page_count = len(pdf_reader.pages)
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n"
    except Exception as e:
        print(f"PyPDF2 extraction failed: {e}")
    
    # If PyPDF2 didn't get text, try pdfplumber
    if not full_text.strip():
        try:
            with pdfplumber.open(pdf_path) as pdf:
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n\n"
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
    
    # Generate cover image from first page if not provided
    if not story.cover_image:
        try:
            cover_image_path = generate_pdf_cover_image(pdf_path)
            if cover_image_path:
                from django.core.files import File
                with open(cover_image_path, 'rb') as f:
                    story.cover_image.save(
                        f'cover_{story.pk}.png',
                        File(f),
                        save=True
                    )
                os.remove(cover_image_path)
        except Exception as e:
            print(f"Cover image generation failed: {e}")
    
    # Update story
    story.total_pages = page_count or 1
    story.extracted_text = full_text[:50000] if full_text else "Text extraction not available for this PDF."
    story.save()


def generate_pdf_cover_image(pdf_path):
    """Extract first page of PDF as an image for cover."""
    try:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(pdf_path)
        page = pdf[0]
        pil_image = page.render(
            scale=2,
            rotation=0,
        ).to_pil()
        
        output = BytesIO()
        pil_image.save(output, format='PNG')
        output.seek(0)
        
        temp_path = pdf_path + '_cover.png'
        with open(temp_path, 'wb') as f:
            f.write(output.getvalue())
        return temp_path
    except Exception as e:
        print(f"pypdfium2 failed: {e}")
    
    return None


def generate_moral_lesson(story):
    """
    Generate a moral lesson from the story text.
    Uses OpenAI API if available, otherwise uses a template.
    """
    if not story.extracted_text:
        story.moral_lesson = "Read this wonderful story to discover its moral lesson!"
        story.save()
        return
    
    # Try to use OpenAI API if key is available
    api_key = getattr(settings, 'OPENAI_API_KEY', '')
    
    if api_key:
        try:
            import openai
            openai.api_key = api_key
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts moral lessons from children's stories. Provide a brief, child-friendly moral lesson."
                    },
                    {
                        "role": "user",
                        "content": f"Read this story and provide a moral lesson in 2-3 sentences:\n\n{story.extracted_text[:3000]}"
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            story.moral_lesson = response.choices[0].message.content.strip()
            story.save()
            return
            
        except Exception as e:
            print(f"Error generating moral lesson with OpenAI: {e}")
    
    # Fallback: Basic moral lesson generator
    story.moral_lesson = generate_fallback_moral_lesson(story.extracted_text)
    story.save()


def generate_fallback_moral_lesson(text):
    """Generate a basic moral lesson without AI."""
    text_lower = text.lower()
    
    # Simple keyword-based moral lesson generation
    if any(word in text_lower for word in ['honest', 'lie', 'truth']):
        return "Always be honest and tell the truth. Honesty is the best policy and builds trust with others."
    elif any(word in text_lower for word in ['kind', 'kindness', 'nice', 'helpful']):
        return "Being kind to others makes the world a better place. Small acts of kindness can make a big difference!"
    elif any(word in text_lower for word in ['brave', 'courage', 'fear']):
        return "Be brave and face your fears! Courage doesn't mean you're not scared, but rather that you do the right thing even when you're afraid."
    elif any(word in text_lower for word in ['friend', 'friendship', 'share']):
        return "True friends are precious. Share, cooperate, and support each other - that's what friendship is all about!"
    elif any(word in text_lower for word in ['hard work', '努力', 'never give up', 'persist']):
        return "Never give up! With hard work and determination, you can achieve your goals."
    elif any(word in text_lower for word in ['family', 'parent', 'love']):
        return "Family loves you unconditionally. Appreciate and care for your loved ones every day."
    else:
        return "Every story teaches us something valuable. Think about what the characters learned and how you can apply it to your own life!"


@login_required
def save_reading_progress(request):
    """Save the user's reading progress via AJAX."""
    if request.method == 'POST':
        story_id = request.POST.get('story_id')
        page = request.POST.get('page', 0)
        completed = request.POST.get('completed', 'false') == 'true'
        
        story = get_object_or_404(Story, id=story_id)
        
        progress, created = ReadingProgress.objects.update_or_create(
            user=request.user,
            story=story,
            defaults={
                'last_page': page,
                'is_completed': completed
            }
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


def story_viewer(request, pk):
    """Dedicated story viewer page with flipbook/scroll reader."""
    story = get_object_or_404(Story, pk=pk)
    
    context = {
        'story': story,
        'pdf_url': story.pdf_file.url,
        'story_text': story.extracted_text or '',
    }
    
    return render(request, 'storybook_app/story_viewer.html', context)


def get_story_text(request, pk):
    """API endpoint to get extracted text for text-to-speech."""
    story = get_object_or_404(Story, pk=pk)
    
    if story.extracted_text:
        return JsonResponse({'text': story.extracted_text})
    
    return JsonResponse({'text': ''})

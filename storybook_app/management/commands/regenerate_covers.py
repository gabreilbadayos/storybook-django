from django.core.management.base import BaseCommand
from storybook_app.models import Story
from storybook_app.views import generate_pdf_cover_image
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Regenerate cover images from PDF first pages for stories without covers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Regenerate all covers (including existing ones)',
        )

    def handle(self, *args, **options):
        if options['all']:
            stories = Story.objects.all()
        else:
            stories = Story.objects.filter(cover_image__isnull=True)

        if not stories.exists():
            self.stdout.write(self.style.WARNING('No stories found to process'))
            return

        total = stories.count()
        self.stdout.write(self.style.SUCCESS(f'Processing {total} stories...'))

        for story in stories:
            if not story.pdf_file:
                self.stdout.write(self.style.WARNING(f'Skipping "{story.title}": no PDF file'))
                continue

            try:
                pdf_path = story.pdf_file.path
                cover_image_path = generate_pdf_cover_image(pdf_path)

                if cover_image_path:
                    with open(cover_image_path, 'rb') as f:
                        story.cover_image.save(
                            f'cover_{story.pk}.png',
                            File(f),
                            save=True
                        )
                    os.remove(cover_image_path)
                    self.stdout.write(f'Success: {story.title}')
                else:
                    self.stdout.write(self.style.WARNING(f'Failed to generate cover for: {story.title}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error with {story.title}: {e}'))

        self.stdout.write(self.style.SUCCESS('Done!'))

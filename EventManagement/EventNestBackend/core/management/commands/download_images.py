import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Event
from django.conf import settings

class Command(BaseCommand):
    help = 'Downloads images from image_url and saves them to the ImageField'

    def handle(self, *args, **options):
        events = Event.objects.all()
        total = events.count()
        self.stdout.write(f"Processing {total} events...")

        for i, event in enumerate(events):
            if event.image:
                # self.stdout.write(f"[{i+1}/{total}] Skipping '{event.title}' - already has an image.")
                continue

            if not event.image_url:
                self.stdout.write(self.style.WARNING(f"[{i+1}/{total}] Skipping '{event.title}' - no image_url."))
                continue

            # Case 1: External URL
            if event.image_url.startswith(('http://', 'https://')):
                self.stdout.write(f"[{i+1}/{total}] Downloading image for '{event.title}' from {event.image_url}...")
                try:
                    response = requests.get(event.image_url, timeout=15)
                    response.raise_for_status()
                    
                    filename = event.image_url.split('/')[-1].split('?')[0]
                    if not filename or '.' not in filename:
                        filename = f"event_{event.id}.jpg"
                    
                    event.image.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f"Successfully saved image for '{event.title}'"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to download image for '{event.title}': {e}"))

            # Case 2: Local path (Static)
            elif event.image_url.startswith(('core/static/', 'static/', 'core/images/')):
                self.stdout.write(f"[{i+1}/{total}] Processing local image for '{event.title}': {event.image_url}")
                
                possible_paths = [
                    os.path.join(settings.BASE_DIR, event.image_url),
                    os.path.join(settings.BASE_DIR, 'core', 'static', event.image_url.replace('static/', '')),
                ]
                
                if event.image_url.startswith('core/'):
                     possible_paths.append(os.path.join(settings.BASE_DIR, 'core', 'static', event.image_url))

                found = False
                for path in possible_paths:
                    if os.path.exists(path):
                        self.stdout.write(f"Found file at {path}")
                        with open(path, 'rb') as f:
                            event.image.save(os.path.basename(path), ContentFile(f.read()), save=True)
                        self.stdout.write(self.style.SUCCESS(f"Successfully linked local image for '{event.title}'"))
                        found = True
                        break
                
                if not found:
                    self.stdout.write(self.style.ERROR(f"Could not find local file for '{event.title}' at any of {possible_paths}"))
            
            else:
                 # Try to see if it's just a filename in core/images/events
                 path = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'images', 'events', event.image_url)
                 if os.path.exists(path):
                     self.stdout.write(f"Found file at {path}")
                     with open(path, 'rb') as f:
                         event.image.save(os.path.basename(path), ContentFile(f.read()), save=True)
                     self.stdout.write(self.style.SUCCESS(f"Successfully linked local image for '{event.title}'"))
                 else:
                     self.stdout.write(self.style.WARNING(f"[{i+1}/{total}] Unrecognized image_url format for '{event.title}': {event.image_url}"))

        self.stdout.write(self.style.SUCCESS("Image processing complete."))

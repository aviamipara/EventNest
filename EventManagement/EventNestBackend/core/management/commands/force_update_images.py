from django.core.management.base import BaseCommand
from core.models import Event

class Command(BaseCommand):
    help = 'Force updates event images to local paths'

    def handle(self, *args, **kwargs):
        # Map of specific titles to new images
        updates = {
            'Standup Comedy Night': '/static/core/images/events/zakir_khan_1770217435338.png',
            'Comedy Night': '/static/core/images/events/vir_das_1770217460198.png', # Partial match for "City Comedy Night"
            'Campus Hackathon 2026': '/static/core/images/events/tech_talk_collab_1770217535203.png',
            'AI & Robotics Workshop': '/static/core/images/events/tech_gadget_show_1770217635954.png',
            'Inter-College Gaming Tournament': '/static/core/images/events/electro_night_1770217353527.png',
            'Music & Arts Festival': '/static/core/images/events/open_mic_1770217478198.png',
            'Career Fair 2026': '/static/core/images/events/tech_talk_collab_1770217535203.png',
            'Debate Championship': '/static/core/images/events/tech_gadget_show_1770217635954.png',
            'Campus Movie Night': '/static/core/images/events/modern_art_expo_1770217618451.png',
            'Photography Walk': '/static/core/images/events/modern_art_expo_1770217618451.png',
            'Student Startup Pitch': '/static/core/images/events/tech_talk_collab_1770217535203.png',
            'Battle of Bands': '/static/core/images/events/rock_band_clash_1770217376122.png',
            'Coding Bootcamp': '/static/core/images/events/tech_gadget_show_1770217635954.png',
            'Literature Fest': '/static/core/images/events/digital_art_class_1770217515606.png',
            'Fitness Bootcamp': '/static/core/images/events/city_marathon_1770217575845.png',
        }

        # Update Student Events exact matches
        for title, img in updates.items():
            events = Event.objects.filter(title=title)
            for event in events:
                event.image_url = img
                event.save()
                self.stdout.write(self.style.SUCCESS(f'Updated {title}'))

        # Update City Events (suffix match)
        # "Comedy Night" suffix
        city_events = Event.objects.filter(title__endswith='Comedy Night')
        for event in city_events:
            # Avoid updating the "Standup Comedy Night" (Student) if it was caught, 
            # though exact match handled handled it.
            if "Standup Comedy Night" not in event.title: 
                 event.image_url = '/static/core/images/events/vir_das_1770217460198.png'
                 event.save()
                 self.stdout.write(self.style.SUCCESS(f'Updated City Event: {event.title}'))

        # Other city templates
        city_updates = {
            'Music Festival': '/static/core/images/events/arijit_singh_1770217310301.png',
            'Tech Summit': '/static/core/images/events/tech_talk_collab_1770217535203.png',
            'Food Carnival': '/static/core/images/events/vegan_food_fest_1770217652000.png',
        }

        for suffix, img in city_updates.items():
            events = Event.objects.filter(title__endswith=suffix)
            for event in events:
                event.image_url = img
                event.save()
                self.stdout.write(self.style.SUCCESS(f'Updated City Event: {event.title}'))

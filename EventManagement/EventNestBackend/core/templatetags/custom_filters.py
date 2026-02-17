from django import template
from django.templatetags.static import static

register = template.Library()

# Consolidated list of all high-quality static images
ALL_IMAGES = [
    'core/images/event_tech_summit.png',
    'core/images/event_comedy_show.png',
    'core/images/event_yoga_outdoor.png',
    'core/images/event_music_concert.png',
    'core/images/event_movie_night.png',
    'core/images/event_standup_comedy.png',
    'core/images/event_music_festival.png',
    'core/images/event_kids_workshop.png',
    'core/images/cat_social.png',
    'core/images/cat_music.png',
    'core/images/cat_corporate.png',
    'core/images/cat_wedding.png',
    'core/images/cat_birthday.png',
    'core/images/cat_sports.png',
]

@register.filter
def get_random_image(event_id):
    """
    Returns a deterministic random image path based on the event ID.
    Usage: {{ event.id|get_random_image }}
    """
    try:
        # Ensure event_id is an integer
        idx = int(event_id) % len(ALL_IMAGES)
        image_path = ALL_IMAGES[idx]
        # Return the actual relative path, static tag will be used in template or we can return static url here?
        # Better to return the string to be used with 'static' tag or just return the static url directly if we import static
        # But templatetags static is for usage IN template.
        # Let's return just the name and use logic in template or simpler: return the full static path.
        # Using `static` from django.templatetags.static inside a filter is possible but `static` is usually a tag.
        # Actually `from django.templatetags.static import static` allows getting the URL.
        return static(image_path)
    except (ValueError, TypeError):
        return static(ALL_IMAGES[0])

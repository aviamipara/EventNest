from django.contrib import admin
from .models import (Booking, CustomEvent, Event, GalleryItem,
                     HeroSlide, Service, Package, Review, Statistic, Inquiry, NewsletterSubscriber)


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'name', 'event_type', 'event_date', 'status', 'created_at')
    list_filter = ('status', 'event_type', 'event_date')
    search_fields = ('name', 'email', 'phone')
    list_editable = ('status',)
@admin.register(CustomEvent)
class CustomEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_type', 'event_date', 'status', 'total_cost', 'created_at')
    list_filter = ('status', 'event_type', 'event_date')
    search_fields = ('event_name', 'email', 'location')
    list_editable = ('status',)
admin.site.register(Event)
admin.site.register(GalleryItem)

# Website Dynamic Content
admin.site.register(HeroSlide)
admin.site.register(Service)
admin.site.register(Package)
admin.site.register(Review)
admin.site.register(Statistic)
admin.site.register(Inquiry)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)


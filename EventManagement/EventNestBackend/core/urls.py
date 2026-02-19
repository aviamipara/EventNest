from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import (ReviewViewSet)


router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'custom-events', views.CustomEventViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.events, name='services'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('booking/', views.booking, name='booking'),
    path('custom-event/', views.custom_event, name='custom_event'),
    path('student-events/', views.student_events, name='student_events'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('api/verify-otp/', views.verify_otp_api, name='verify_otp_api'),
    path('api/resend-otp/', views.resend_otp_api, name='resend_otp_api'),
    
    # Forgot Password
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp_view, name='verify_reset_otp'),
    path('api/verify-reset-otp/', views.verify_reset_otp_api, name='verify_reset_otp_api'),
    path('api/resend-reset-otp/', views.resend_reset_otp_api, name='resend_reset_otp_api'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    
    # User Profile & Authentication
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # API Endpoints
    path('api/', include(router.urls)),
    path('api/custom-event-legacy', views.custom_event_api, name='custom_event_api'),
    
    # Management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket/<str:ticket_type>/<int:ticket_id>/', views.view_ticket, name='view_ticket'),
    


    
    # Liked Events
    path('liked-events/', views.liked_events, name='liked_events'),
    path('api/toggle-like/<int:event_id>/', views.toggle_like, name='toggle_like'),
    
    # Contact
    path('contact-submit/', views.contact_submit, name='contact_submit'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),

    # Search Suggestions API
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
]


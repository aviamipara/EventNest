from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.models import User
from django.contrib import messages
import json
from .models import (Booking, CustomEvent, Event, LikedEvent,
                     HeroSlide, Service, Package, Review, GalleryItem, Statistic, Inquiry, NewsletterSubscriber)

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
from django.template import loader
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
import random
from .models import UserProfile

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import EventSerializer, CustomEventSerializer, BookingSerializer, CustomEventSubmissionSerializer
from .utils import send_html_email, set_otp_for_user

# API ViewSets
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CustomEventViewSet(viewsets.ModelViewSet):
    queryset = CustomEvent.objects.all()
    serializer_class = CustomEventSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

@require_http_methods(["GET"])
def index(request):
    # Fetch all dynamic content for the homepage with optimized queries
    
    # 1. Hero Slides
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    
    # 2. Services
    services = Service.objects.all()
    
    # 3. Packages: Optimized sorting via DB annotation to avoid full table load
    # Convert string price (e.g. "$500") to float for sorting
    # Note: For SQLite, we might still need some python help or complex raw SQL, 
    # but let's try to keep it optimized for common cases. 
    # Ideally, price should be a DecimalField. Since it's CharField, we'll strip non-digit chars.
    from django.db.models import F, FloatField, Value
    from django.db.models.functions import Cast, Replace
    
    # Simple Python sort for now as data is small, but restrict fields
    # If moving to Postgres, we would cast in DB.
    # All packages with needed fields
    all_packages = Package.objects.filter(is_active=True).only('name', 'price_start', 'image', 'features', 'description').all()
    
    import re
    def get_price(pkg):
        try:
            # Extract only digits and decimal point using regex
            val = re.sub(r'[^\d.]', '', pkg.price_start)
            return float(val) if val else 99999999.0
        except:
            return 99999999.0

    packages = sorted(all_packages, key=get_price)[:3] 
    
    # 4. Reviews: Limit fields and count
    reviews = Review.objects.filter(is_active=True).order_by('-created_at')[:10]  # Limit to 10 latest
    
    # 5. Stats
    stats = Statistic.objects.all().order_by('order')
    
    # 6. Recommended Events: Optimize random selection
    # For large tables, order_by('?') is slow. For <1000 items, it's fine.
    # We fetch specifics to avoid joining everything if not needed.
    recommended_events = Event.objects.filter(date__gte=timezone.now()).order_by('?')[:10]
    
    # 7. Concerts
    concerts = Event.objects.filter(category__iexact='Concert', date__gte=timezone.now()).order_by('date')[:10]

    # 8. Gallery: Fetch limited fields
    gallery_items = GalleryItem.objects.all().order_by('-created_at')[:6]

    # Diagnostic Prints for Terminal
    print(f"DEBUG: Index view loaded. Slides: {hero_slides.count()}, Packages: {len(packages)}, Recommended: {len(recommended_events)}")
    
    context = {
        'hero_slides': hero_slides,
        'services': services,
        'packages': packages,
        'reviews': reviews,
        'stats': stats,
        'gallery_items': gallery_items,
        'recommended_events': recommended_events,
        'concerts': concerts,
    }
    return render(request, 'core/index.html', context)

@require_POST
def contact_submit(request):
    try:
        # Get data from POST
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Create Inquiry
        Inquiry.objects.create(name=name, email=email, message=message)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Thank you! We will contact you soon.'})
        
        messages.success(request, "Thank you! We've received your inquiry.")
        return redirect('index')

    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        messages.error(request, f"Error: {str(e)}")
        return redirect('index')

def student_events(request):
    # Fetch events with category 'student' (case-insensitive)
    events_list = Event.objects.filter(category__iexact='student').order_by('date')
    
    # --- Pagination ---
    from django.core.paginator import Paginator
    paginator = Paginator(events_list, 12) # Pagination increased to 12 to fill grid
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_event_ids = []
    if request.user.is_authenticated:
        liked_event_ids = list(LikedEvent.objects.filter(user=request.user).values_list('event_id', flat=True))
        
    return render(request, 'core/student_events.html', {
        'events': page_obj, 
        'page_obj': page_obj, 
        'liked_event_ids': liked_event_ids,
        'custom_page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    })

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if email:
            email = email.strip().lower()
            # Detect common typos
            if '@gamil.com' in email:
                email = email.replace('@gamil.com', '@gmail.com')
                messages.warning(request, "We corrected 'gamil.com' to 'gmail.com' for you.")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect(request.path_info + '?mode=register')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect(request.path_info + '?mode=register')

        # Strong Password Validation using AUTH_PASSWORD_VALIDATORS
        try:
            validate_password(password, user=User(username=email, email=email, first_name=first_name, last_name=last_name))
        except DjangoValidationError as e:
            messages.error(request, ' '.join(e.messages))
            return redirect(request.path_info + '?mode=register')

        try:
            # Create Inactive User
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            user.is_active = False # Deactivate until verified
            user.save()

            # Generate & Set OTP

            verification_code = set_otp_for_user(user)
            user.profile.is_verified = False
            user.profile.save()

            # Send Email (HTML)
            send_html_email(
                'Your EventNest Verification Code',
                'core/verification_code_email.html',
                {'user': user, 'verification_code': verification_code},
                email
            )

            messages.success(request, f"Verification code sent to {email}")
            response = redirect('verify_email')
            # Use Signed Cookie instead of Session
            response.set_signed_cookie('verification_email', email, salt='verify_email', max_age=600)
            return response
            
        except Exception as e:
            messages.error(request, str(e))
            return redirect(request.path_info + '?mode=register')

    return render(request, 'core/login.html')

def verify_email_view(request):
    """
    Renders the verification page.
    Actual verification is handled via AJAX at /api/verify-otp/
    """
    email = request.get_signed_cookie('verification_email', salt='verify_email', default=None)
    if not email:
        messages.error(request, "Session expired. Please register again.")
        return redirect('register')
    return render(request, 'core/verify_email.html', {'email': email})

@csrf_exempt
@require_POST
def verify_otp_api(request):
    """
    AJAX API for verifying OTP
    """
    try:
        data = json.loads(request.body)
        code = data.get('code')
        email = request.get_signed_cookie('verification_email', salt='verify_email', default=None)

        if not email:
             return JsonResponse({'status': 'error', 'message': 'Session expired. Please register again.'}, status=400)

        user = User.objects.get(email=email)
        profile = user.profile

        # Check OTP
        if profile.verification_code == code:
            # Check Expiry
            if profile.verification_code_expires_at and profile.verification_code_expires_at < timezone.now():
                 return JsonResponse({'status': 'error', 'message': 'OTP has expired. Please resend.'}, status=400)

            # Activate User
            user.is_active = True
            user.save()
            
            # Clear OTP
            profile.verification_code = None 
            profile.verification_code_expires_at = None
            profile.is_verified = True
            profile.save()
            
            # Login User
            login(request, user)
            
            # Send Welcome Email (Async recommended but Sync for now)
            try:

                send_html_email(
                    'Welcome to EventNest! 🚀',
                    'core/welcome_email.html',
                    {'user': user, 'site_url': request.build_absolute_uri('/')},
                    user.email
                )
            except:
                pass # Don't block verification on email fail

            messages.success(request, "Email verified successfully! Welcome to EventNest.")
            response = JsonResponse({'status': 'success', 'message': 'Verified', 'redirect_url': '/'})
            response.delete_cookie('verification_email')
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP. Please try again.'}, status=400)

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
def resend_otp_api(request):
    """
    AJAX API for resending OTP
    """
    try:
        email = request.get_signed_cookie('verification_email', salt='verify_email', default=None)
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Session expired. Please register again.'}, status=400)

        user = User.objects.get(email=email)
        
        # Generate & Set OTP

        new_code = set_otp_for_user(user, duration_minutes=5)
        
        # Send Email (HTML)
        send_html_email(
            'Resend: Your EventNest Verification Code',
            'core/verification_code_email.html',
            {'user': user, 'verification_code': new_code},
            email
        )
        
        return JsonResponse({'status': 'success', 'message': 'OTP sent successfully!'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
    except Exception as e:
         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate & Set OTP

            reset_code = set_otp_for_user(user)
            
            # Send Email (HTML)
            send_html_email(
                'Reset Your Password - EventNest',
                'core/reset_password_email.html',
                {'user': user, 'verification_code': reset_code},
                email
            )
            
            messages.success(request, f"OTP sent to {email}")
            response = redirect('verify_reset_otp')
            response.set_signed_cookie('reset_email', email, salt='reset_email', max_age=600)
            return response
            
        except User.DoesNotExist:
            # Security: Don't reveal if user exists, but for UX simulate success or generic invalid
            messages.error(request, "Email not found.")
            
    return render(request, 'core/forgot_password.html')

def verify_reset_otp_view(request):
    if not request.get_signed_cookie('reset_email', salt='reset_email', default=None):
        return redirect('forgot_password')
    return render(request, 'core/verify_reset_otp.html')

@csrf_exempt
@require_POST
def verify_reset_otp_api(request):
    try:
        data = json.loads(request.body)
        code = data.get('code')
        email = request.get_signed_cookie('reset_email', salt='reset_email', default=None)
        
        if not email:
             return JsonResponse({'status': 'error', 'message': 'Session expired.'}, status=400)
             
        user = User.objects.get(email=email)
        profile = user.profile
        
        if profile.verification_code == code:
             if profile.verification_code_expires_at < timezone.now():
                 return JsonResponse({'status': 'error', 'message': 'OTP Expired'}, status=400)
                 
             # Success - Mark session as allowed to reset
             response = JsonResponse({'status': 'success', 'message': 'Verified!', 'redirect_url': '/reset-password/'})
             response.set_signed_cookie('can_reset_password', 'true', salt='reset_auth', max_age=600)
             return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP'}, status=400)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
def resend_reset_otp_api(request):
    try:
        email = request.get_signed_cookie('reset_email', salt='reset_email', default=None)
        if not email:
             return JsonResponse({'status': 'error', 'message': 'Session expired.'}, status=400)
             
        user = User.objects.get(email=email)
        
        # Generate & Set OTP

        new_code = set_otp_for_user(user)
        
        # Send Email
        send_html_email(
            'Resend: Reset Your Password',
            'core/reset_password_email.html',
            {'user': user, 'verification_code': new_code},
            email
        )
        
        return JsonResponse({'status': 'success', 'message': 'OTP Resent'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def reset_password_view(request):
    if not request.get_signed_cookie('can_reset_password', salt='reset_auth', default=None):
        messages.error(request, "Unauthorized access. Verify OTP first.")
        return redirect('forgot_password')
        
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')
            
        email = request.get_signed_cookie('reset_email', salt='reset_email', default=None)
        if not email:
            messages.error(request, "Session expired. Please start over.")
            return redirect('forgot_password')
            
        try:
            user = User.objects.get(email=email)
            
            # Strong Password Validation
            try:
                validate_password(new_password, user=user)
            except DjangoValidationError as e:
                messages.error(request, ' '.join(e.messages))
                return redirect('reset_password')

            user.set_password(new_password)
            user.is_active = True # Activate if they reset via OTP
            user.save()
            
            # Clear OTP
            user.profile.verification_code = None
            user.profile.save()
            
            messages.success(request, "Password reset successfully. Please Login.")
            response = redirect('login')
            response.delete_cookie('reset_email')
            response.delete_cookie('can_reset_password')
            return response
            
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('reset_password')
        
    return render(request, 'core/reset_password.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f"Thank you for your email confirmation. Now you can login your account.")
        return redirect('index')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            username = username.strip().lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
             login(request, user)
             
             # Send Login Alert Email
             try:
 
                 send_html_email(
                     'New Login to EventNest',
                     'core/login_alert_email.html',
                     {
                        'user': user,
                        'time': timezone.now().strftime('%I:%M %p'),
                        'date': timezone.now().strftime('%Y-%m-%d')
                     },
                     user.email
                 )
             except:
                 pass

             messages.success(request, f"Welcome back, {user.first_name}!")
             return redirect('index')
        else:
             # Check if user exists but is inactive
             check_user = User.objects.filter(username=username).first()
             if check_user and not check_user.is_active:
                 messages.error(request, "Your account is not activated. Please verify your email or contact support.")
             else:
                 messages.error(request, "Invalid email or password")
             return render(request, 'core/login.html')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

def events(request):
    # Fetch all future events from DB
    events_list = Event.objects.filter(date__gte=timezone.now())
    
    # --- SEARCH ---
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        events_list = events_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(category__icontains=search_query)
        )

    # --- FILTERS ---

    # 1. City Filter (Removed legacy City filter)


    # 2. Category Filter (Support multiple selection)
    # request.GET.getlist('categories') will get all values for ?categories=Music&categories=Comedy
    category_filters = request.GET.getlist('categories') 
    if category_filters:
        # If 'All' is in the list, we ignore it or treat as no filter, but usually checkbox 'All' isn't sent
        if 'All' not in category_filters:
            events_list = events_list.filter(category__in=category_filters)
    
    # 3. Date Filter
    date_filter = request.GET.get('date_filter')
    today = timezone.now().date()
    if date_filter == 'Today':
        events_list = events_list.filter(date=today)
    elif date_filter == 'Tomorrow':
        tomorrow = today + timezone.timedelta(days=1)
        events_list = events_list.filter(date=tomorrow)
    elif date_filter == 'Weekend':
        # Find next Saturday/Sunday
        weekday = today.weekday()
        days_to_saturday = (5 - weekday) % 7
        this_saturday = today + timezone.timedelta(days=days_to_saturday)
        this_sunday = this_saturday + timezone.timedelta(days=1)
        events_list = events_list.filter(date__range=[this_saturday, this_sunday])

    # 4. Price Filter (Simple Ranges)
    price_filter = request.GET.get('price_filter')
    if price_filter == 'Free':
        # Assuming price is stored as string 'Rs. 0' or similar, strict check might be hard.
        # Ideally, clean up DB to use DecimalField. For now, we try our best or skip if too complex for string.
        pass # implementation depends on DB clean up

    # --- Sorting ---
    sort_by = request.GET.get('sort', 'date')
    if sort_by == 'price_low':
         events_list = events_list.extra(select={'price_int': "CAST(REPLACE(REPLACE(REPLACE(price, 'Rs. ', ''), '₹', ''), ',', '') AS INTEGER)"}).order_by('price_int')
    elif sort_by == 'price_high':
         events_list = events_list.extra(select={'price_int': "CAST(REPLACE(REPLACE(REPLACE(price, 'Rs. ', ''), '₹', ''), ',', '') AS INTEGER)"}).order_by('-price_int')
    else:
        events_list = events_list.order_by('date')

    # --- Pagination ---
    from django.core.paginator import Paginator
    paginator = Paginator(events_list, 12) # 12 events per page for better grid alignment
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- Context Data for Sidebar ---
    # 1. Categories
    db_categories = Event.objects.values_list('category', flat=True).distinct()
    all_categories = sorted(list(set([c for c in db_categories if c])))
    
    # 2. Languages (Mock for now, or fetch if added to model)
    languages = ['English', 'Hindi', 'Marathi', 'Punjabi', 'Gujarati']
    



    context = {
        'events_list': page_obj, 
        'page_obj': page_obj,
        'liked_event_ids': [], # Add auth check back if needed
        'all_categories': all_categories,
        'languages': languages,
        'selected_categories': category_filters,
        'selected_date': date_filter,
        'current_sort': sort_by,
        'total_events': events_list.count(), # for "X Events" counter
        'custom_page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    }
    
    if request.user.is_authenticated:
        context['liked_event_ids'] = list(LikedEvent.objects.filter(user=request.user).values_list('event_id', flat=True))

    return render(request, 'core/events.html', context)

def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return render(request, 'core/events.html')

    return render(request, 'core/event_detail.html', {
        'event': event,

        'reviews': Review.objects.filter(is_active=True).order_by('?')[:3]
    })

def gallery(request):
    from .models import GalleryItem
    from django.core.paginator import Paginator
    
    # Base Query
    items = GalleryItem.objects.all().order_by('-created_at')
    
    # 1. Filter by Category
    category = request.GET.get('category')
    if category and category != 'all':
        items = items.filter(category=category)
        
    # 2. Search
    search_query = request.GET.get('q')
    if search_query:
        items = items.filter(title__icontains=search_query)

    # 3. Pagination
    paginator = Paginator(items, 12) # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/gallery.html', {
        'gallery_items': page_obj, 
        'page_obj': page_obj,
        'current_category': category or 'all',
        'search_query': search_query,
        'custom_page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    })

def booking(request):
    # Get event from query param if available
    prefilled_event = request.GET.get('event', '')
    
    # 1. Try match by ID if numeric (from GET or logic)
    event_instance = None
    package_instance = None
    
    if prefilled_event:
        if str(prefilled_event).isdigit():
            event_instance = Event.objects.filter(id=prefilled_event).first()
        if not event_instance:
            event_instance = Event.objects.filter(title__iexact=prefilled_event).first()
        
        # If no event found, check if it's a package
        if not event_instance:
            package_instance = Package.objects.filter(name__iexact=prefilled_event).first()

    if request.method == 'POST':
        # Security: Require login for submission
        if not request.user.is_authenticated:
             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                  return JsonResponse({'status': 'error', 'message': 'Please login to book an event.'}, status=401)
             messages.error(request, "Please login to book an event.")
             return redirect('login')

        try:
            # Handle JSON data or Form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            # Extract data
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            event_type = data.get('event_type')
            event_date_str = data.get('event_date') or None
            guest_count = int(data.get('guest_count') or 0)
            budget = data.get('budget', '')
            venue_preference = data.get('venue', '')
            vision = data.get('vision', '')

            # Backend Validation
            if not name or not email:
                 if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                      return JsonResponse({'status': 'error', 'message': 'Name and Email are required.'}, status=400)
                 return render(request, 'core/booking.html', {
                     'error': 'Name and Email are required', 
                     'prefilled_event': prefilled_event,
                     'event': event_instance,
                     'package': package_instance
                 })


            services = data.getlist('services[]') if hasattr(data, 'getlist') else data.get('services', [])
            if isinstance(services, list):
                services = ", ".join(services)

            if event_instance:
                # CHECK AVAILABILITY
                if event_instance.available_tickets < guest_count:
                     raise Exception(f"Sold Out! Only {event_instance.available_tickets} tickets left for {event_instance.title}.")
                
                # DEDUCT INVENTORY
                event_instance.available_tickets -= guest_count
                event_instance.save()
            
            # Use package name as event_name if package link
            event_name_val = None
            if package_instance:
                event_name_val = f"Package: {package_instance.name}"

            # Create Booking
            booking = Booking.objects.create(
                name=name,
                email=email,
                phone=phone,
                event=event_instance, # Link FK
                event_name=event_name_val,
                event_type=event_type,
                event_date=event_date_str,
                guest_count=guest_count,
                budget=budget,
                venue_preference=venue_preference,
                services=services,
                vision=vision,
                status='Confirmed' if event_instance else 'Pending'
            )
            
            # If AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f'Booking Confirmed! Tickets: {guest_count}'})
            
            # Standard form post redirect
            return render(request, 'core/booking.html', {
                'success': True,
                'prefilled_event': prefilled_event,
                'event': event_instance,
                'package': package_instance,
                'booking_name': name,
                'booking_email': email,
                'booking_guests': guest_count,
                'booking_date': event_date_str 
            })

        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            # Handle error in standard form
            return render(request, 'core/booking.html', {
                'error': str(e), 
                'prefilled_event': prefilled_event,
                'event': event_instance,
                'package': package_instance
            })
            
    return render(request, 'core/booking.html', {
        'prefilled_event': prefilled_event,
        'event': event_instance,
        'package': package_instance
    })


def custom_event(request):
    if request.method == 'POST':
        # Security: Require login for submission
        if not request.user.is_authenticated:
             messages.error(request, "Please login to plan an event.")
             return redirect('login')

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        event_type = request.POST.get('event_type')
        # Check if 'Other' was selected and a custom type was provided
        if event_type == 'Other':
             other_type = request.POST.get('other_event_type')
             if other_type:
                 event_type = other_type
        
        message = request.POST.get('message')
        event_name = request.POST.get('event_name')
        

        # New fields
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        guest_count = request.POST.get('guest_count')
        budget = request.POST.get('budget')

        location = request.POST.get('location')

        # Additional Details
        theme = request.POST.get('theme')
        food_type = request.POST.get('food_type')
        photography = request.POST.get('photography')
        plate_cost = request.POST.get('plate_cost') or 0.00
        
        # Checkboxes
        stage_decor = request.POST.get('stage_decor') == 'on'
        flower_decor = request.POST.get('flower_decor') == 'on'
        lighting_style = request.POST.get('lighting_style') == 'on'


        if name and email:
            from .models import CustomEvent
            
            try:
                CustomEvent.objects.create(
                    event_name=event_name,
                    event_type=event_type,
                    event_date=event_date,
                    guests=guest_count,
                    location=location,
                    email=email,
                    phone=phone,
                    total_cost=budget,
                    
                    # New Fields
                    theme=theme,
                    food_type=food_type,
                    plate_cost=plate_cost,
                    photography=photography,
                    stage_decor=stage_decor,
                    flower_decor=flower_decor,
                    lighting_style=lighting_style,

                    notes=f"Time: {event_time}\nDetails: {message}"
                )
                return render(request, 'core/custom_event.html', {'success': True})
            except Exception as e:
                print(f"Error creating custom event: {e}")
                return render(request, 'core/custom_event.html', {'error': str(e)})
            
    return render(request, 'core/custom_event.html')


@api_view(['POST'])
@permission_classes([permissions.AllowAny]) # Public submission allowed, but validated
def custom_event_api(request):
    serializer = CustomEventSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            event = serializer.save()
            return Response({'status': 'success', 'id': event.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@login_required
def dashboard(request):
    # Retrieve bookings and custom events for the logged-in user only
    email = request.user.email
    bookings = Booking.objects.filter(email=email).order_by('-created_at')
    custom_events = CustomEvent.objects.filter(email=email).order_by('-created_at')
    
    return render(request, 'core/dashboard.html', {
        'bookings': bookings,
        'custom_events': custom_events
    })

@login_required
def liked_events(request):
    liked_events = LikedEvent.objects.filter(user=request.user).select_related('event')
    events = [like.event for like in liked_events]
    return render(request, 'core/liked_events.html', {'events': events})

@csrf_exempt
@require_POST
def newsletter_signup(request):
    try:
        # Check if JSON or Form
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email')
        else:
            email = request.POST.get('email')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email is required.'}, status=400)

        # Check if already subscribed
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return JsonResponse({'status': 'success', 'message': 'You are already subscribed!'})

        # Save subscriber
        NewsletterSubscriber.objects.create(email=email)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing to our newsletter!'})
        
        messages.success(request, "Thank you for subscribing!")
        return redirect('index')

    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        messages.error(request, f"Error: {str(e)}")
        return redirect('index')

@login_required
def toggle_like(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        liked_event, created = LikedEvent.objects.get_or_create(user=request.user, event=event)
        
        if not created:
            # If it already existed, the user is un-liking
            liked_event.delete()
            is_liked = False
        else:
            is_liked = True
            
        return JsonResponse({'status': 'success', 'is_liked': is_liked})
    except Event.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# ============= User Profile Views =============

def profile_view(request):
    from .models import UserProfile
    
    if not request.user.is_authenticated:
        return redirect('login')
        
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update User fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Update Profile fields
        profile.phone_number = request.POST.get('phone_number')
        profile.gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
             profile.date_of_birth = date_of_birth
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.address = request.POST.get('address')
        profile.aadhaar_number = request.POST.get('aadhaar_number')
        profile.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
        
    return render(request, 'core/profile.html', {'user': request.user, 'profile': profile})



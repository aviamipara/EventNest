from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    # Link to specific event for inventory tracking (New)
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    event_name = models.CharField(max_length=200, null=True, blank=True, help_text="Custom Event Name if applicable")
    event_type = models.CharField(max_length=50) # Kept for backward compatibility/custom events
    event_date = models.DateField(null=True, blank=True)
    guest_count = models.IntegerField(null=True, blank=True)
    budget = models.CharField(max_length=50, null=True, blank=True)
    venue_preference = models.CharField(max_length=50, null=True, blank=True)
    services = models.TextField(null=True, blank=True, help_text="Comma separated list of services")
    vision = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.name} - {self.event_type} ({self.status})"

class CustomEvent(models.Model):
    # Basic Details
    event_name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    guests = models.IntegerField()
    location = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Theme & Decor
    theme = models.CharField(max_length=100, null=True, blank=True)
    stage_decor = models.BooleanField(default=False)
    flower_decor = models.BooleanField(default=False)
    lighting_style = models.BooleanField(default=False)
    
    # Catering
    food_type = models.CharField(max_length=50, null=True, blank=True)
    plate_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Media
    photography = models.CharField(max_length=50, null=True, blank=True) # yes/no
    videography = models.CharField(max_length=50, null=True, blank=True) # 4k/none
    drone_shoot = models.CharField(max_length=50, null=True, blank=True) # yes/no
    
    # Setup
    seating_style = models.CharField(max_length=100, null=True, blank=True)
    security = models.BooleanField(default=False)
    
    # Other
    notes = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    total_cost = models.CharField(max_length=50, null=True, blank=True) # Stored as string to keep currency symbol if needed, or parse later
    
    created_at = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Custom: {self.event_name} ({self.created_at.date()}) - {self.status}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, db_index=True) # Index for category filtering
    image_url = models.CharField(max_length=500, help_text="URL to image (external or static)")
    image = models.ImageField(upload_to='events/', null=True, blank=True, help_text="Upload local image file")
    price = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True, db_index=True) # Index for date filtering
    
    # Inventory Management (New)
    total_tickets = models.PositiveIntegerField(default=100)
    available_tickets = models.PositiveIntegerField(default=100)
    
    def __str__(self):
        return self.title

    @property
    def get_clean_price(self):
        """Returns a clean numeric price string, handling 'k' shorthand and currency symbols."""
        if not self.price:
            return "Free"
        
        price_str = str(self.price).lower()
        import re
        # Find the first number in the string
        match = re.search(r'\d+(\.\d+)?', price_str)
        if match:
            val = float(match.group())
            # Handle 'k' multiplier
            if 'k' in price_str and val < 100:
                val *= 1000
            
            # Format with comma separators (Indian style)
            try:
                import locale
                # locale.setlocale(locale.LC_ALL, 'en_IN') # Might fail on some systems
                # Manual formatting if locale fails
                from django.contrib.humanize.templatetags.humanize import intcomma
                return f"\u20B9{intcomma(int(val))}"
            except:
                return f"\u20B9{int(val)}"
        
        return self.price

    @property
    def get_image_url(self):
        """Returns a clean absolute URL for the event image, prioritizing the uploaded file."""
        # 1. Check if an image is uploaded via ImageField
        if self.image:
            try:
                return self.image.url
            except:
                pass

        if not self.image_url:
            return ""
        
        # 2. If it's an external link
        if self.image_url.startswith(('http://', 'https://')):
            return self.image_url
        
        # 3. If it's a relative path to static files
        if self.image_url.startswith('/static/'):
            return self.image_url
        
        if self.image_url.startswith('core/'):
            return f"/static/{self.image_url}"
        
        if self.image_url.startswith('static/'):
            return f"/{self.image_url}"

        # Standard case: append static prefix if missing
        return f"/static/{self.image_url.lstrip('/')}"






class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('wedding', 'Weddings'),
        ('corporate', 'Corporate'),
        ('concert', 'Concerts'),
        ('parties', 'Parties'),
    ]

    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=100, help_text="Short title or caption")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            if self.image.name.startswith('http'):
                return self.image.name
            return self.image.url
        return ''

class LikedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} likes {self.event.title}"

# ============= Dynamic Homepage Models =============

class HeroSlide(models.Model):
    """Slides for the Homepage Hero Carousel"""
    image = models.ImageField(upload_to='hero_slides/')
    title = models.CharField(max_length=200, help_text="Main heading")
    subtitle = models.CharField(max_length=200, help_text="Subtitle above heading")
    description = models.TextField(blank=True, help_text="Text below heading")
    button_text = models.CharField(max_length=50, default="Explore Events")
    button_link = models.CharField(max_length=200, default="events")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            if self.image.name.startswith('http'):
                return self.image.name
            return self.image.url
        return ''

class Service(models.Model):
    """Services offered (e.g. Weddings, Corporate)"""
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class e.g. 'fas fa-glass-cheers'")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Package(models.Model):
    """Event Packages"""
    name = models.CharField(max_length=100) # e.g. Royal Wedding
    price_start = models.CharField(max_length=50, help_text="e.g. $2,500")
    image = models.ImageField(upload_to='packages/')
    description = models.TextField()
    features = models.TextField(help_text="Comma separated list of features")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    
    def get_features_list(self):
        return [x.strip() for x in self.features.split(',')]
        
    @property
    def get_image_url(self):
        if not self.image:
            return ""
        
        # If it's a URL in the ImageField
        if self.image.name.startswith(('http://', 'https://')):
            return self.image.name
            
        # If the path looks like it belongs to static (e.g. starts with 'core/')
        if self.image.name.startswith('core/'):
            return f"/static/{self.image.name}"
            
        # Standard media URL access
        try:
            return self.image.url
        except:
            return ""

class Review(models.Model):
    """Client Reviews (formerly Testimonials)"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100, help_text="e.g. Wedding Client, CEO TechCorp", blank=True, null=True)
    client_image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    quote = models.TextField()
    is_active = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"

    @property
    def get_image_url(self):
        if self.client_image and hasattr(self.client_image, 'url'):
            if self.client_image.name.startswith('http'):
                return self.client_image.name
            return self.client_image.url
        return ''

class Statistic(models.Model):
    """Counter Stats (e.g. 500+ Events)"""
    number = models.CharField(max_length=50) # e.g. 500+
    label = models.CharField(max_length=50) # e.g. Events Completed
    icon_class = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.number} {self.label}"

class Inquiry(models.Model):
    """Contact Form Submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry from {self.name} - {self.created_at.date()}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_expires_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class CustomSession(models.Model):
    """
    Custom Session model to replace django_session.
    REMOVED session_data column.
    Adds a `created_at` timestamp.
    """
    session_key = models.CharField(max_length=40, primary_key=True)
    expire_date = models.DateTimeField(db_index=True)
    start_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @classmethod
    def get_session_store_class(cls):
        from core.session_backend import SessionStore
        return SessionStore

    def __str__(self):
        return f"{self.session_key} (Started: {self.start_date})"

from django.core.mail import EmailMessage
from django.template import loader
from django.utils import timezone
from datetime import timedelta
import random
import logging

logger = logging.getLogger(__name__)

def send_html_email(subject, template_name, context, to_email):
    """
    Helper to send HTML emails.
    """
    try:
        html_message = loader.render_to_string(template_name, context)
        email_msg = EmailMessage(
            subject, 
            html_message, 
            to=[to_email]
        )
        email_msg.content_subtype = "html"
        email_msg.send(fail_silently=True)
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False

def generate_otp(length=6):
    """Generates a numeric OTP of given length."""
    range_start = 10**(length-1)
    range_end = (10**length) - 1
    return str(random.randint(range_start, range_end))

def set_otp_for_user(user, duration_minutes=10):
    """
    Generates OTP, sets it on user profile, and saves.
    Returns the code.
    """
    code = generate_otp()
    expiry = timezone.now() + timedelta(minutes=duration_minutes)
    
    # Ensure profile exists
    if not hasattr(user, 'profile'):
        from .models import UserProfile
        UserProfile.objects.create(user=user)
        
    user.profile.verification_code = code
    user.profile.verification_code_expires_at = expiry
    user.profile.save()
    
    return code


def crop_to_circle(image_path, output_path):
    """
    Crops an image to a circle and saves it to output_path.
    Requires Pillow (PIL) library.
    """
    try:
        from PIL import Image, ImageDraw, ImageOps
        import os
        
        img = Image.open(image_path).convert("RGBA")
        
        # Create a circular mask
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        
        # Apply the mask
        result = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        result.putalpha(mask)
        
        # Save
        result.save(output_path)
        logger.info(f"Successfully created rounded image at {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error cropping image to circle: {e}")
        return False

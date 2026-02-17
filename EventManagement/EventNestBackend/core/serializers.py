from rest_framework import serializers
from .models import (
    Event, CustomEvent, Booking, Review
)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'client_name', 'client_role', 'rating', 'quote', 'created_at']
        read_only_fields = ['is_active', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
            if not validated_data.get('client_name'):
                validated_data['client_name'] = user.get_full_name() or user.username
        return super().create(validated_data)




class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'category', 'image_url', 
            'price', 'location', 'date', 'total_tickets', 'available_tickets'
        ]

class CustomEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomEvent
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class CustomEventSubmissionSerializer(serializers.Serializer):
    """
    Serializer to handle the nested JSON structure from the frontend custom event form
    and map it to the flat CustomEvent model.
    """
    eventName = serializers.CharField(source='event_name')
    eventType = serializers.CharField(source='event_type')
    eventDate = serializers.DateField(source='event_date')
    guests = serializers.IntegerField()
    location = serializers.CharField()
    theme = serializers.CharField(required=False, allow_blank=True)
    
    # Nested dictionaries
    decor = serializers.DictField(required=False)
    catering = serializers.DictField(required=False)
    media = serializers.DictField(required=False)
    setup = serializers.DictField(required=False)
    
    notes = serializers.CharField(required=False, allow_blank=True)
    payment = serializers.CharField(source='payment_method', required=False, allow_blank=True)
    totalCost = serializers.CharField(source='total_cost', required=False, allow_blank=True)

    def create(self, validated_data):
        decor = validated_data.pop('decor', {}) or {}
        catering = validated_data.pop('catering', {}) or {}
        media = validated_data.pop('media', {}) or {}
        setup = validated_data.pop('setup', {}) or {}

        # Extract flat fields
        event_data = {
            'event_name': validated_data.get('event_name'),
            'event_type': validated_data.get('event_type'),
            'event_date': validated_data.get('event_date'),
            'guests': validated_data.get('guests'),
            'location': validated_data.get('location'),
            'theme': validated_data.get('theme'),
            'notes': validated_data.get('notes'),
            'payment_method': validated_data.get('payment_method'),
            'total_cost': validated_data.get('total_cost'),
            'email': self.context['request'].user.email if 'request' in self.context and self.context['request'].user.is_authenticated else None,
            
            # Map nested fields to model attributes
            'stage_decor': decor.get('stage', False),
            'flower_decor': decor.get('flowers', False),
            'lighting_style': decor.get('lighting', False),
            
            'food_type': catering.get('type'),
            'plate_cost': catering.get('cost', 0),
            
            'photography': media.get('photo'),
            'videography': media.get('video'),
            'drone_shoot': media.get('drone'),
            
            'seating_style': setup.get('seating'),
            'security': setup.get('security', False),
        }
        
        return CustomEvent.objects.create(**event_data)

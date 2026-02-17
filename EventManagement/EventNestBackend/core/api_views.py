from rest_framework import viewsets, permissions
from .models import Event, Review
from .serializers import (
    EventSerializer, ReviewSerializer
)

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone




class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone to submit, but we'll link to user in serializer if logged in
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(is_active=True)

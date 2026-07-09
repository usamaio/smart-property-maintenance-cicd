import uuid
from django.conf import settings
from django.db import models


class Property(models.Model):
    PROPERTY_TYPES = (
        ('house', 'House'),
        ('flat', 'Flat'),
        ('apartment', 'Apartment'),
        ('studio', 'Studio'),
        ('commercial', 'Commercial'),
    )

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        limit_choices_to={'role': 'landlord'}
    )

    name = models.CharField(max_length=255)
    address = models.TextField()
    postcode = models.CharField(max_length=20, blank=True, default='')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    is_active = models.BooleanField(default=True)

    property_qr_code = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPES = (
        ('kitchen', 'Kitchen'),
        ('living_room', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('bathroom', 'Bathroom'),
        ('garage', 'Garage'),
        ('utility', 'Utility Room'),
        ('other', 'Other'),
    )

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=30, choices=ROOM_TYPES, default='other')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ('property', 'name')
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f"{self.name} - {self.property.name}"
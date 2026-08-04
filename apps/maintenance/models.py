import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.appliances.models import Appliance
from apps.properties.models import Property, Room


class MaintenanceRequest(models.Model):
    CATEGORY_CHOICES = (
        ('heating', 'Heating'),
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('appliance', 'Appliance'),
        ('structural', 'Structural'),
        ('safety', 'Safety'),
        ('general', 'General'),
        ('other', 'Other'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='maintenance_requests',
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='maintenance_requests',
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        related_name='maintenance_requests',
        blank=True,
        null=True,
    )

    appliance = models.ForeignKey(
        Appliance,
        on_delete=models.SET_NULL,
        related_name='maintenance_requests',
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=150,
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='general',
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
    )

    target_date = models.DateField(
        blank=True,
        null=True,
    )

    resolution_notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Maintenance Request'
        verbose_name_plural = 'Maintenance Requests'

    def __str__(self):
        return f'{self.title} - {self.property.name}'

    def clean(self):
        errors = {}

        if (
            self.room_id
            and self.property_id
            and self.room.property_id != self.property_id
        ):
            errors['room'] = (
                'The selected room does not belong to the selected property.'
            )

        if (
            self.appliance_id
            and self.property_id
            and self.appliance.property_id != self.property_id
        ):
            errors['appliance'] = (
                'The selected appliance does not belong to the '
                'selected property.'
            )

        if (
            self.room_id
            and self.appliance_id
            and self.appliance.room_id
            and self.appliance.room_id != self.room_id
        ):
            errors['appliance'] = (
                'The selected appliance is not assigned to the '
                'selected room.'
            )

        if errors:
            raise ValidationError(errors)
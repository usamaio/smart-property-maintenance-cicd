import uuid

from django.db import models
from django.utils import timezone

from apps.properties.models import Property, Room


class Appliance(models.Model):
    APPLIANCE_TYPES = (
        ('boiler', 'Boiler'),
        ('washing_machine', 'Washing Machine'),
        ('dishwasher', 'Dishwasher'),
        ('refrigerator', 'Refrigerator'),
        ('freezer', 'Freezer'),
        ('oven', 'Oven'),
        ('microwave', 'Microwave'),
        ('heating_system', 'Heating System'),
        ('air_conditioner', 'Air Conditioner'),
        ('smoke_alarm', 'Smoke Alarm'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('under_maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out of Service'),
        ('retired', 'Retired'),
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='appliances',
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        related_name='appliances',
        blank=True,
        null=True,
    )

    name = models.CharField(max_length=150)

    appliance_type = models.CharField(
        max_length=30,
        choices=APPLIANCE_TYPES,
        default='other',
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
    )

    model_number = models.CharField(
        max_length=100,
        blank=True,
    )

    serial_number = models.CharField(
        max_length=100,
        blank=True,
    )

    installation_date = models.DateField(
        blank=True,
        null=True,
    )

    purchase_date = models.DateField(
        blank=True,
        null=True,
    )

    # Temporary compatibility field.
    # This can be removed after the standalone Warranty model
    # is fully integrated throughout the application.
    warranty_expiry_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='active',
    )

    has_individual_qr = models.BooleanField(
        default=False,
        help_text=(
            'Enable this for high-value or frequently serviced appliances.'
        ),
    )

    appliance_qr_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Appliance'
        verbose_name_plural = 'Appliances'

    def __str__(self):
        return f'{self.name} - {self.property.name}'


class Warranty(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    appliance = models.OneToOneField(
        Appliance,
        on_delete=models.CASCADE,
        related_name='warranty',
    )

    provider = models.CharField(
        max_length=150,
    )

    policy_number = models.CharField(
        max_length=100,
        blank=True,
    )

    start_date = models.DateField()

    expiry_date = models.DateField()

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-expiry_date']
        verbose_name = 'Warranty'
        verbose_name_plural = 'Warranties'

    def __str__(self):
        return f'{self.provider} - {self.appliance.name}'

    @property
    def is_active(self):
        return self.expiry_date >= timezone.localdate()
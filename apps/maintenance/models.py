import builtins
import uuid

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

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


class ServiceRecord(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    appliance = models.ForeignKey(
        Appliance,
        on_delete=models.CASCADE,
        related_name='service_records',
    )

    maintenance_request = models.ForeignKey(
        MaintenanceRequest,
        on_delete=models.SET_NULL,
        related_name='service_records',
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_records_created',
    )

    service_date = models.DateField()

    service_provider = models.CharField(
        max_length=150,
    )

    technician_name = models.CharField(
        max_length=150,
        blank=True,
    )

    work_performed = models.TextField()

    parts_replaced = models.TextField(
        blank=True,
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    next_service_date = models.DateField(
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
        ordering = ['-service_date', '-created_at']
        verbose_name = 'Service Record'
        verbose_name_plural = 'Service Records'

    def __str__(self):
        return f'{self.appliance.name} - {self.service_date}'

    def clean(self):
        errors = {}

        if (
            self.maintenance_request_id
            and self.maintenance_request.appliance_id
            and self.maintenance_request.appliance_id != self.appliance_id
        ):
            errors['maintenance_request'] = (
                'The selected maintenance request is linked to a '
                'different appliance.'
            )

        if (
            self.next_service_date
            and self.service_date
            and self.next_service_date <= self.service_date
        ):
            errors['next_service_date'] = (
                'The next service date must be after the service date.'
            )

        if self.cost is not None and self.cost < 0:
            errors['cost'] = 'Cost cannot be negative.'

        if errors:
            raise ValidationError(errors)


class MaintenanceSchedule(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('six_monthly', 'Every Six Months'),
        ('annually', 'Annually'),
    )

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='maintenance_schedules',
    )

    appliance = models.ForeignKey(
        Appliance,
        on_delete=models.SET_NULL,
        related_name='maintenance_schedules',
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='maintenance_schedules_created',
    )

    task_name = models.CharField(
        max_length=150,
    )

    description = models.TextField(
        blank=True,
    )

    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='annually',
    )

    next_due_date = models.DateField()

    last_completed_date = models.DateField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['next_due_date', 'task_name']
        verbose_name = 'Maintenance Schedule'
        verbose_name_plural = 'Maintenance Schedules'

    def __str__(self):
        return f'{self.task_name} - {self.property.name}'

    def clean(self):
        errors = {}

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
            self.last_completed_date
            and self.next_due_date
            and self.next_due_date <= self.last_completed_date
        ):
            errors['next_due_date'] = (
                'The next due date must be after the last completed date.'
            )

        if errors:
            raise ValidationError(errors)

    @builtins.property
    def is_overdue(self):
        return (
            self.is_active
            and self.next_due_date < timezone.localdate()
        )

    @builtins.property
    def is_due_soon(self):
        today = timezone.localdate()
        due_soon_limit = today + relativedelta(days=30)

        return (
            self.is_active
            and today <= self.next_due_date <= due_soon_limit
        )

    def calculate_next_due_date(self, from_date=None):
        base_date = from_date or timezone.localdate()

        frequency_map = {
            'daily': relativedelta(days=1),
            'weekly': relativedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'quarterly': relativedelta(months=3),
            'six_monthly': relativedelta(months=6),
            'annually': relativedelta(years=1),
        }

        return base_date + frequency_map[self.frequency]

    def mark_completed(self, completed_date=None):
        completed_date = completed_date or timezone.localdate()

        self.last_completed_date = completed_date
        self.next_due_date = self.calculate_next_due_date(
            from_date=completed_date,
        )

        self.save(
            update_fields=[
                'last_completed_date',
                'next_due_date',
                'updated_at',
            ]
        )
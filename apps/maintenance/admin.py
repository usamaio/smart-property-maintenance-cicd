from django.contrib import admin

from .models import MaintenanceRequest, ServiceRecord


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'property',
        'category',
        'priority',
        'status',
        'requested_by',
        'created_at',
    )

    list_filter = (
        'category',
        'priority',
        'status',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'property__name',
        'room__name',
        'appliance__name',
        'requested_by__username',
    )

    readonly_fields = (
        'public_id',
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = (
        'appliance',
        'service_date',
        'service_provider',
        'technician_name',
        'cost',
        'next_service_date',
    )

    list_filter = (
        'service_date',
        'service_provider',
        'next_service_date',
    )

    search_fields = (
        'appliance__name',
        'appliance__property__name',
        'service_provider',
        'technician_name',
        'work_performed',
    )

    readonly_fields = (
        'public_id',
        'created_at',
        'updated_at',
    )

    ordering = (
        '-service_date',
    )
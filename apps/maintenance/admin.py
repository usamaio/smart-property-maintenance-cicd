from django.contrib import admin

from .models import MaintenanceRequest


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
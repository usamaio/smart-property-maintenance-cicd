from django.contrib import admin

from .models import Appliance


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'property',
        'room',
        'appliance_type',
        'brand',
        'status',
        'has_individual_qr',
    )

    search_fields = (
        'name',
        'brand',
        'model_number',
        'serial_number',
        'property__name',
        'property__postcode',
    )

    list_filter = (
        'appliance_type',
        'status',
        'has_individual_qr',
        'created_at',
    )

    readonly_fields = (
        'public_id',
        'appliance_qr_code',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (
            'Appliance Location',
            {
                'fields': (
                    'property',
                    'room',
                )
            },
        ),
        (
            'Appliance Information',
            {
                'fields': (
                    'name',
                    'appliance_type',
                    'brand',
                    'model_number',
                    'serial_number',
                    'status',
                    'notes',
                )
            },
        ),
        (
            'Dates and Warranty',
            {
                'fields': (
                    'purchase_date',
                    'installation_date',
                    'warranty_expiry_date',
                )
            },
        ),
        (
            'Hybrid QR Configuration',
            {
                'fields': (
                    'has_individual_qr',
                    'appliance_qr_code',
                )
            },
        ),
        (
            'System Information',
            {
                'fields': (
                    'public_id',
                    'created_at',
                    'updated_at',
                ),
                'classes': ('collapse',),
            },
        ),
    )
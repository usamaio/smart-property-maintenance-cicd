from django.contrib import admin

from .models import Property, Room


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'property_type',
        'postcode',
        'is_active',
        'created_at',
    )

    search_fields = (
        'name',
        'postcode',
        'owner__username',
        'public_id',
    )

    list_filter = (
        'property_type',
        'is_active',
        'created_at',
    )

    readonly_fields = (
        'public_id',
        'property_qr_code',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (
            'Property Information',
            {
                'fields': (
                    'owner',
                    'name',
                    'property_type',
                    'address',
                    'postcode',
                    'is_active',
                )
            },
        ),
        (
            'System Information',
            {
                'fields': (
                    'public_id',
                    'property_qr_code',
                    'created_at',
                    'updated_at',
                ),
                'classes': ('collapse',),
            },
        ),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'property',
        'room_type',
        'created_at',
    )

    search_fields = (
        'name',
        'property__name',
    )

    list_filter = (
        'room_type',
        'created_at',
    )

    readonly_fields = (
        'public_id',
        'created_at',
        'updated_at',
    )
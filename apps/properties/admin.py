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
    search_fields = ('name', 'postcode', 'owner__username')
    list_filter = ('property_type', 'is_active', 'created_at')
    readonly_fields = ('public_id', 'created_at', 'updated_at')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'room_type', 'created_at')
    search_fields = ('name', 'property__name')
    list_filter = ('room_type', 'created_at')
    readonly_fields = ('public_id', 'created_at', 'updated_at')
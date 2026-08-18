from django.urls import path

from . import views


app_name = 'properties'


urlpatterns = [
    path(
        '',
        views.property_list,
        name='property_list'
    ),
    path(
        'add/',
        views.property_create,
        name='property_create'
    ),

    path(
        'qr/<uuid:public_id>/',
        views.property_qr_preview,
        name='property_qr_preview'
    ),

    path(
        '<uuid:public_id>/',
        views.property_detail,
        name='property_detail'
    ),
    path(
        '<uuid:public_id>/edit/',
        views.property_update,
        name='property_update'
    ),
    path(
        '<uuid:public_id>/delete/',
        views.property_delete,
        name='property_delete'
    ),

    path(
        '<uuid:property_public_id>/rooms/add/',
        views.room_create,
        name='room_create'
    ),
    path(
        'rooms/<uuid:room_public_id>/edit/',
        views.room_update,
        name='room_update'
    ),
    path(
        'rooms/<uuid:room_public_id>/delete/',
        views.room_delete,
        name='room_delete'
    ),
]
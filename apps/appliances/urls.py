from django.urls import path

from . import views


app_name = 'appliances'


urlpatterns = [
    path(
        'property/<uuid:property_public_id>/add/',
        views.appliance_create,
        name='appliance_create'
    ),
    path(
        '<uuid:public_id>/',
        views.appliance_detail,
        name='appliance_detail'
    ),
    path(
        '<uuid:public_id>/edit/',
        views.appliance_update,
        name='appliance_update'
    ),
    path(
        '<uuid:public_id>/delete/',
        views.appliance_delete,
        name='appliance_delete'
    ),

    path(
        '<uuid:appliance_public_id>/warranties/add/',
        views.warranty_create,
        name='warranty_create'
    ),
    path(
        'warranties/<uuid:public_id>/edit/',
        views.warranty_update,
        name='warranty_update'
    ),
    path(
        'warranties/<uuid:public_id>/delete/',
        views.warranty_delete,
        name='warranty_delete'
    ),
]
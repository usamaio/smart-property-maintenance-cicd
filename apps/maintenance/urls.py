from django.urls import path

from . import views


app_name = 'maintenance'


urlpatterns = [
    path(
        '',
        views.maintenance_request_list,
        name='maintenance_request_list',
    ),
    path(
        'add/',
        views.maintenance_request_create,
        name='maintenance_request_create',
    ),
    path(
        '<uuid:public_id>/',
        views.maintenance_request_detail,
        name='maintenance_request_detail',
    ),
    path(
        '<uuid:public_id>/edit/',
        views.maintenance_request_update,
        name='maintenance_request_update',
    ),
    path(
        '<uuid:public_id>/delete/',
        views.maintenance_request_delete,
        name='maintenance_request_delete',
    ),
]
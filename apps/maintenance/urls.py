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
        'service-records/',
        views.service_record_list,
        name='service_record_list',
    ),
    path(
        'service-records/add/',
        views.service_record_create,
        name='service_record_create',
    ),
    path(
        'service-records/<uuid:public_id>/',
        views.service_record_detail,
        name='service_record_detail',
    ),
    path(
        'service-records/<uuid:public_id>/edit/',
        views.service_record_update,
        name='service_record_update',
    ),
    path(
        'service-records/<uuid:public_id>/delete/',
        views.service_record_delete,
        name='service_record_delete',
    ),

    path(
        'schedules/',
        views.maintenance_schedule_list,
        name='maintenance_schedule_list',
    ),
    path(
        'schedules/add/',
        views.maintenance_schedule_create,
        name='maintenance_schedule_create',
    ),
    path(
        'schedules/<uuid:public_id>/',
        views.maintenance_schedule_detail,
        name='maintenance_schedule_detail',
    ),
    path(
        'schedules/<uuid:public_id>/edit/',
        views.maintenance_schedule_update,
        name='maintenance_schedule_update',
    ),
    path(
        'schedules/<uuid:public_id>/delete/',
        views.maintenance_schedule_delete,
        name='maintenance_schedule_delete',
    ),
    path(
        'schedules/<uuid:public_id>/complete/',
        views.maintenance_schedule_complete,
        name='maintenance_schedule_complete',
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
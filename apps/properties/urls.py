from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('add/', views.property_create, name='property_create'),
    path('<uuid:public_id>/', views.property_detail, name='property_detail'),
    path('<uuid:public_id>/edit/', views.property_update, name='property_update'),
    path('<uuid:public_id>/delete/', views.property_delete, name='property_delete'),
]
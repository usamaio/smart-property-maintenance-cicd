from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_redirect(request):
    return redirect('properties:property_list')


urlpatterns = [
    path('', home_redirect, name='home'),

    path('admin/', admin.site.urls),

    path(
        'accounts/',
        include('apps.accounts.urls', namespace='accounts'),
    ),

    path(
        'properties/',
        include('apps.properties.urls', namespace='properties'),
    ),

    path(
        'appliances/',
        include('apps.appliances.urls', namespace='appliances'),
    ),
]
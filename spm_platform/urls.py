from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path(
        '',
        RedirectView.as_view(
            pattern_name='accounts:dashboard',
            permanent=False,
        ),
        name='home',
    ),

    path(
        'admin/',
        admin.site.urls,
    ),

    path(
        'accounts/',
        include(
            'apps.accounts.urls',
            namespace='accounts',
        ),
    ),

    path(
        'properties/',
        include(
            'apps.properties.urls',
            namespace='properties',
        ),
    ),

    path(
        'appliances/',
        include(
            'apps.appliances.urls',
            namespace='appliances',
        ),
    ),

    path(
        'maintenance/',
        include(
            'apps.maintenance.urls',
            namespace='maintenance',
        ),
    ),
]
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'properties/',
        include('apps.properties.urls', namespace='properties')
    ),
]
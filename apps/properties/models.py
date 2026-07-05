from django.db import models
from django.conf import settings

class Property(models.Model):
    PROPERTY_TYPE = (
        ('house', 'House'),
        ('flat', 'Flat'),
        ('apartment', 'Apartment'),
        ('studio', 'Studio'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'landlord'}
    )

    name = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
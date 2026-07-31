from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.appliances.models import Appliance, Warranty
from apps.properties.models import Property


class WarrantyModelTests(TestCase):
    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username='testuser',
            password='TestPassword123!',
        )

        self.property = Property.objects.create(
            owner=self.user,
            name='Test Property',
            address='1 Test Street',
        )

        self.appliance = Appliance.objects.create(
            property=self.property,
            name='Test Boiler',
        )

    def test_warranty_is_active_when_expiry_date_is_in_future(self):
        today = timezone.localdate()

        warranty = Warranty.objects.create(
            appliance=self.appliance,
            provider='Test Provider',
            start_date=today,
            expiry_date=today + timedelta(days=365),
        )

        self.assertTrue(warranty.is_active)

    def test_warranty_is_expired_when_expiry_date_is_in_past(self):
        today = timezone.localdate()

        warranty = Warranty.objects.create(
            appliance=self.appliance,
            provider='Test Provider',
            start_date=today - timedelta(days=365),
            expiry_date=today - timedelta(days=1),
        )

        self.assertFalse(warranty.is_active)


class WarrantyViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username='testuser',
            password='TestPassword123!',
        )

        self.property = Property.objects.create(
            owner=self.user,
            name='Test Property',
            address='1 Test Street',
        )

        self.appliance = Appliance.objects.create(
            property=self.property,
            name='Test Boiler',
        )

        self.client.login(
            username='testuser',
            password='TestPassword123!',
        )

    def test_warranty_create_page_requires_login(self):
        self.client.logout()

        response = self.client.get(
            reverse(
                'appliances:warranty_create',
                kwargs={
                    'appliance_public_id': self.appliance.public_id,
                },
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_open_warranty_create_page(self):
        response = self.client.get(
            reverse(
                'appliances:warranty_create',
                kwargs={
                    'appliance_public_id': self.appliance.public_id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
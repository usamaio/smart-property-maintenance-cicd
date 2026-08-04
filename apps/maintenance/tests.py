from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.appliances.models import Appliance
from apps.properties.models import Property, Room

from .models import MaintenanceRequest


class MaintenanceRequestTestBase(TestCase):
    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username='owner',
            password='TestPassword123!',
            role='landlord',
        )

        self.other_user = user_model.objects.create_user(
            username='otherowner',
            password='TestPassword123!',
            role='landlord',
        )

        self.property = Property.objects.create(
            owner=self.user,
            name='Test Property',
            address='1 Test Street',
            postcode='IP1 1AA',
            property_type='house',
        )

        self.other_property = Property.objects.create(
            owner=self.other_user,
            name='Other Property',
            address='2 Other Street',
            postcode='IP2 2BB',
            property_type='flat',
        )

        self.room = Room.objects.create(
            property=self.property,
            name='Kitchen',
            room_type='kitchen',
        )

        self.appliance = Appliance.objects.create(
            property=self.property,
            room=self.room,
            name='Test Boiler',
            appliance_type='boiler',
        )

        self.maintenance_request = MaintenanceRequest.objects.create(
            requested_by=self.user,
            property=self.property,
            room=self.room,
            appliance=self.appliance,
            title='Boiler not heating',
            category='heating',
            description='The boiler is not producing hot water.',
            priority='high',
            status='open',
        )


class MaintenanceRequestModelTests(MaintenanceRequestTestBase):
    def test_string_representation(self):
        self.assertEqual(
            str(self.maintenance_request),
            'Boiler not heating - Test Property',
        )

    def test_default_status_is_open(self):
        maintenance_request = MaintenanceRequest.objects.create(
            requested_by=self.user,
            property=self.property,
            title='Leaking tap',
            category='plumbing',
            description='The kitchen tap is leaking.',
        )

        self.assertEqual(
            maintenance_request.status,
            'open',
        )

    def test_default_priority_is_medium(self):
        maintenance_request = MaintenanceRequest.objects.create(
            requested_by=self.user,
            property=self.property,
            title='Loose cupboard handle',
            category='general',
            description='The cupboard handle requires tightening.',
        )

        self.assertEqual(
            maintenance_request.priority,
            'medium',
        )


class MaintenanceRequestViewTests(MaintenanceRequestTestBase):
    def test_list_page_requires_login(self):
        response = self.client.get(
            reverse(
                'maintenance:maintenance_request_list',
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_logged_in_owner_can_view_request_list(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:maintenance_request_list',
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'Boiler not heating',
        )

    def test_owner_can_open_request_detail(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:maintenance_request_detail',
                kwargs={
                    'public_id': self.maintenance_request.public_id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'Boiler not heating',
        )

    def test_other_user_cannot_view_request(self):
        self.client.login(
            username='otherowner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:maintenance_request_detail',
                kwargs={
                    'public_id': self.maintenance_request.public_id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_owner_can_create_request(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.post(
            reverse(
                'maintenance:maintenance_request_create',
            ),
            {
                'property': self.property.id,
                'room': self.room.id,
                'appliance': self.appliance.id,
                'title': 'Annual boiler service',
                'category': 'heating',
                'description': (
                    'The boiler requires its annual service.'
                ),
                'priority': 'medium',
                'status': 'open',
                'target_date': '',
                'resolution_notes': '',
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            MaintenanceRequest.objects.filter(
                title='Annual boiler service',
                requested_by=self.user,
            ).exists()
        )

    def test_completed_request_requires_resolution_notes(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.post(
            reverse(
                'maintenance:maintenance_request_update',
                kwargs={
                    'public_id': self.maintenance_request.public_id,
                },
            ),
            {
                'property': self.property.id,
                'room': self.room.id,
                'appliance': self.appliance.id,
                'title': self.maintenance_request.title,
                'category': self.maintenance_request.category,
                'description': self.maintenance_request.description,
                'priority': self.maintenance_request.priority,
                'status': 'completed',
                'target_date': '',
                'resolution_notes': '',
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'Resolution notes are required',
        )

    def test_list_only_shows_users_own_requests(self):
        MaintenanceRequest.objects.create(
            requested_by=self.other_user,
            property=self.other_property,
            title='Other user request',
            category='general',
            description='This belongs to another user.',
        )

        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:maintenance_request_list',
            )
        )

        self.assertContains(
            response,
            'Boiler not heating',
        )

        self.assertNotContains(
            response,
            'Other user request',
        )
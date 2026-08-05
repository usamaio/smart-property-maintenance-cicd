from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.appliances.models import Appliance
from apps.properties.models import Property, Room

from .models import MaintenanceRequest, ServiceRecord


class MaintenanceTestBase(TestCase):
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

        self.other_appliance = Appliance.objects.create(
            property=self.other_property,
            name='Other Boiler',
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
            status='completed',
            resolution_notes='The boiler was serviced and tested.',
        )

        self.service_record = ServiceRecord.objects.create(
            appliance=self.appliance,
            maintenance_request=self.maintenance_request,
            created_by=self.user,
            service_date=date.today(),
            service_provider='ABC Heating Services',
            technician_name='John Smith',
            work_performed=(
                'Completed annual boiler inspection and safety checks.'
            ),
            parts_replaced='Boiler seal',
            cost=Decimal('125.00'),
            next_service_date=date.today() + timedelta(days=365),
        )


class MaintenanceRequestModelTests(MaintenanceTestBase):
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


class MaintenanceRequestViewTests(MaintenanceTestBase):
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
            ).exists()
        )


class ServiceRecordModelTests(MaintenanceTestBase):
    def test_string_representation(self):
        self.assertIn(
            'Test Boiler',
            str(self.service_record),
        )

    def test_service_record_links_to_appliance(self):
        self.assertEqual(
            self.service_record.appliance,
            self.appliance,
        )

    def test_service_record_can_link_to_maintenance_request(self):
        self.assertEqual(
            self.service_record.maintenance_request,
            self.maintenance_request,
        )


class ServiceRecordViewTests(MaintenanceTestBase):
    def test_service_record_list_requires_login(self):
        response = self.client.get(
            reverse(
                'maintenance:service_record_list',
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_owner_can_view_service_record_list(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:service_record_list',
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'ABC Heating Services',
        )

    def test_owner_can_view_service_record_detail(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:service_record_detail',
                kwargs={
                    'public_id': self.service_record.public_id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'Completed annual boiler inspection',
        )

    def test_other_user_cannot_view_service_record(self):
        self.client.login(
            username='otherowner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:service_record_detail',
                kwargs={
                    'public_id': self.service_record.public_id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_owner_can_create_service_record(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.post(
            reverse(
                'maintenance:service_record_create',
            ),
            {
                'appliance': self.appliance.id,
                'maintenance_request': self.maintenance_request.id,
                'service_date': date.today().isoformat(),
                'service_provider': 'New Service Company',
                'technician_name': 'Jane Doe',
                'work_performed': (
                    'Replaced faulty component and tested operation.'
                ),
                'parts_replaced': 'Control valve',
                'cost': '95.50',
                'next_service_date': (
                    date.today() + timedelta(days=365)
                ).isoformat(),
                'notes': 'System operating normally.',
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            ServiceRecord.objects.filter(
                service_provider='New Service Company',
            ).exists()
        )

    def test_next_service_date_must_be_after_service_date(self):
        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.post(
            reverse(
                'maintenance:service_record_create',
            ),
            {
                'appliance': self.appliance.id,
                'maintenance_request': '',
                'service_date': date.today().isoformat(),
                'service_provider': 'Invalid Date Company',
                'technician_name': '',
                'work_performed': 'Routine inspection.',
                'parts_replaced': '',
                'cost': '20.00',
                'next_service_date': date.today().isoformat(),
                'notes': '',
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            'The next service date must be after the service date.',
        )

    def test_service_record_list_only_shows_owned_records(self):
        ServiceRecord.objects.create(
            appliance=self.other_appliance,
            created_by=self.other_user,
            service_date=date.today(),
            service_provider='Other Company',
            work_performed='Other work.',
        )

        self.client.login(
            username='owner',
            password='TestPassword123!',
        )

        response = self.client.get(
            reverse(
                'maintenance:service_record_list',
            )
        )

        self.assertContains(
            response,
            'ABC Heating Services',
        )

        self.assertNotContains(
            response,
            'Other Company',
        )
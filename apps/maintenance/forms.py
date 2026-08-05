from django import forms

from apps.appliances.models import Appliance
from apps.properties.models import Property, Room

from .models import MaintenanceRequest, ServiceRecord


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest

        fields = [
            'property',
            'room',
            'appliance',
            'title',
            'category',
            'description',
            'priority',
            'status',
            'target_date',
            'resolution_notes',
        ]

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                }
            ),
            'target_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'resolution_notes': forms.Textarea(
                attrs={
                    'rows': 4,
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        if user is not None:
            self.fields['property'].queryset = Property.objects.filter(
                owner=user,
                is_active=True,
            )

            self.fields['room'].queryset = Room.objects.filter(
                property__owner=user,
            ).select_related(
                'property',
            )

            self.fields['appliance'].queryset = Appliance.objects.filter(
                property__owner=user,
            ).select_related(
                'property',
                'room',
            )
        else:
            self.fields['property'].queryset = Property.objects.none()
            self.fields['room'].queryset = Room.objects.none()
            self.fields['appliance'].queryset = Appliance.objects.none()

        self.fields['room'].required = False
        self.fields['room'].empty_label = 'No room selected'

        self.fields['appliance'].required = False
        self.fields['appliance'].empty_label = 'No appliance selected'

        self.fields['target_date'].required = False
        self.fields['resolution_notes'].required = False

    def clean(self):
        cleaned_data = super().clean()

        property_obj = cleaned_data.get('property')
        room = cleaned_data.get('room')
        appliance = cleaned_data.get('appliance')
        status = cleaned_data.get('status')
        resolution_notes = cleaned_data.get('resolution_notes')

        if (
            property_obj
            and self.user
            and property_obj.owner_id != self.user.id
        ):
            self.add_error(
                'property',
                'You do not have permission to use this property.',
            )

        if (
            room
            and property_obj
            and room.property_id != property_obj.id
        ):
            self.add_error(
                'room',
                'The selected room does not belong to this property.',
            )

        if (
            appliance
            and property_obj
            and appliance.property_id != property_obj.id
        ):
            self.add_error(
                'appliance',
                'The selected appliance does not belong to this property.',
            )

        if (
            room
            and appliance
            and appliance.room_id
            and appliance.room_id != room.id
        ):
            self.add_error(
                'appliance',
                'The selected appliance is not assigned to this room.',
            )

        if status == 'completed' and not resolution_notes:
            self.add_error(
                'resolution_notes',
                'Resolution notes are required for a completed request.',
            )

        return cleaned_data


class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord

        fields = [
            'appliance',
            'maintenance_request',
            'service_date',
            'service_provider',
            'technician_name',
            'work_performed',
            'parts_replaced',
            'cost',
            'next_service_date',
            'notes',
        ]

        widgets = {
            'service_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'next_service_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'work_performed': forms.Textarea(
                attrs={
                    'rows': 5,
                }
            ),
            'parts_replaced': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'cost': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '0.01',
                }
            ),
        }

    def __init__(
        self,
        *args,
        user=None,
        appliance=None,
        maintenance_request=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.user = user

        if user is not None:
            self.fields['appliance'].queryset = Appliance.objects.filter(
                property__owner=user,
            ).select_related(
                'property',
                'room',
            )

            self.fields[
                'maintenance_request'
            ].queryset = MaintenanceRequest.objects.filter(
                property__owner=user,
            ).select_related(
                'property',
                'appliance',
            )
        else:
            self.fields['appliance'].queryset = Appliance.objects.none()

            self.fields[
                'maintenance_request'
            ].queryset = MaintenanceRequest.objects.none()

        self.fields['maintenance_request'].required = False
        self.fields[
            'maintenance_request'
        ].empty_label = 'No maintenance request selected'

        self.fields['technician_name'].required = False
        self.fields['parts_replaced'].required = False
        self.fields['cost'].required = False
        self.fields['next_service_date'].required = False
        self.fields['notes'].required = False

        if appliance is not None:
            self.fields['appliance'].initial = appliance

        if maintenance_request is not None:
            self.fields[
                'maintenance_request'
            ].initial = maintenance_request

            if maintenance_request.appliance_id:
                self.fields[
                    'appliance'
                ].initial = maintenance_request.appliance

    def clean(self):
        cleaned_data = super().clean()

        appliance = cleaned_data.get('appliance')
        maintenance_request = cleaned_data.get('maintenance_request')
        service_date = cleaned_data.get('service_date')
        next_service_date = cleaned_data.get('next_service_date')
        cost = cleaned_data.get('cost')

        if (
            appliance
            and self.user
            and appliance.property.owner_id != self.user.id
        ):
            self.add_error(
                'appliance',
                'You do not have permission to use this appliance.',
            )

        if (
            maintenance_request
            and self.user
            and maintenance_request.property.owner_id != self.user.id
        ):
            self.add_error(
                'maintenance_request',
                'You do not have permission to use this maintenance request.',
            )

        if (
            maintenance_request
            and maintenance_request.appliance_id
            and appliance
            and maintenance_request.appliance_id != appliance.id
        ):
            self.add_error(
                'maintenance_request',
                'The selected maintenance request is linked to a '
                'different appliance.',
            )

        if (
            next_service_date
            and service_date
            and next_service_date <= service_date
        ):
            self.add_error(
                'next_service_date',
                'The next service date must be after the service date.',
            )

        if cost is not None and cost < 0:
            self.add_error(
                'cost',
                'Cost cannot be negative.',
            )

        return cleaned_data
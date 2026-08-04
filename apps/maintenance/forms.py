from django import forms

from apps.appliances.models import Appliance
from apps.properties.models import Property, Room

from .models import MaintenanceRequest


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
                    'placeholder': (
                        'Describe the maintenance problem clearly.'
                    ),
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
                    'placeholder': (
                        'Add completion or resolution information '
                        'when available.'
                    ),
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
            ).select_related('property')

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

    def clean_title(self):
        title = self.cleaned_data['title']
        return title.strip()

    def clean_description(self):
        description = self.cleaned_data['description']
        return description.strip()

    def clean_resolution_notes(self):
        resolution_notes = self.cleaned_data.get(
            'resolution_notes',
            '',
        )

        return resolution_notes.strip()

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
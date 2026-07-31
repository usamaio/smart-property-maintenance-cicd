from django import forms

from apps.properties.models import Room

from .models import Appliance, Warranty


class ApplianceForm(forms.ModelForm):
    class Meta:
        model = Appliance

        fields = [
            'room',
            'name',
            'appliance_type',
            'brand',
            'model_number',
            'serial_number',
            'purchase_date',
            'installation_date',
            'warranty_expiry_date',
            'status',
            'has_individual_qr',
            'notes',
        ]

        widgets = {
            'purchase_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'installation_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'warranty_expiry_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Add any relevant appliance notes.',
                }
            ),
        }

    def __init__(self, *args, property_obj=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.property_obj = property_obj

        if property_obj is not None:
            self.fields['room'].queryset = Room.objects.filter(
                property=property_obj
            )
        else:
            self.fields['room'].queryset = Room.objects.none()

        self.fields['room'].required = False
        self.fields['room'].empty_label = 'No room selected'

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.strip()

    def clean(self):
        cleaned_data = super().clean()

        room = cleaned_data.get('room')
        purchase_date = cleaned_data.get('purchase_date')
        installation_date = cleaned_data.get('installation_date')
        warranty_expiry_date = cleaned_data.get(
            'warranty_expiry_date'
        )

        if (
            room
            and self.property_obj
            and room.property_id != self.property_obj.id
        ):
            self.add_error(
                'room',
                'The selected room does not belong to this property.'
            )

        if (
            purchase_date
            and installation_date
            and installation_date < purchase_date
        ):
            self.add_error(
                'installation_date',
                'Installation date cannot be earlier than purchase date.'
            )

        if (
            purchase_date
            and warranty_expiry_date
            and warranty_expiry_date < purchase_date
        ):
            self.add_error(
                'warranty_expiry_date',
                'Warranty expiry date cannot be earlier than purchase date.'
            )

        return cleaned_data


class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty

        fields = [
            'provider',
            'policy_number',
            'start_date',
            'expiry_date',
            'notes',
        ]

        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'expiry_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Add any relevant warranty notes.',
                }
            ),
        }

    def clean_provider(self):
        provider = self.cleaned_data['provider']
        return provider.strip()

    def clean_policy_number(self):
        policy_number = self.cleaned_data.get('policy_number', '')
        return policy_number.strip()

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        expiry_date = cleaned_data.get('expiry_date')

        if (
            start_date
            and expiry_date
            and expiry_date < start_date
        ):
            self.add_error(
                'expiry_date',
                'Expiry date cannot be earlier than the start date.'
            )

        return cleaned_data
    
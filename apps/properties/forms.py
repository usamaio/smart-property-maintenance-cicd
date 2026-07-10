from django import forms

from .models import Property, Room


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name',
            'address',
            'postcode',
            'property_type',
            'is_active',
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'name',
            'room_type',
        ]

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.strip()
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.properties.models import Property

from .forms import ApplianceForm
from .models import Appliance


@login_required
def appliance_create(request, property_public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=property_public_id,
        owner=request.user,
    )

    if request.method == 'POST':
        form = ApplianceForm(
            request.POST,
            property_obj=property_obj,
        )

        if form.is_valid():
            appliance = form.save(commit=False)
            appliance.property = property_obj
            appliance.save()

            messages.success(
                request,
                'Appliance added successfully.',
            )

            return redirect(
                'appliances:appliance_detail',
                public_id=appliance.public_id,
            )
    else:
        form = ApplianceForm(property_obj=property_obj)

    context = {
        'form': form,
        'property': property_obj,
    }

    return render(
        request,
        'appliances/appliance_form.html',
        context,
    )


@login_required
def appliance_detail(request, public_id):
    appliance = get_object_or_404(
        Appliance,
        public_id=public_id,
        property__owner=request.user,
    )

    context = {
        'appliance': appliance,
        'property': appliance.property,
    }

    return render(
        request,
        'appliances/appliance_detail.html',
        context,
    )


@login_required
def appliance_update(request, public_id):
    appliance = get_object_or_404(
        Appliance,
        public_id=public_id,
        property__owner=request.user,
    )

    if request.method == 'POST':
        form = ApplianceForm(
            request.POST,
            instance=appliance,
            property_obj=appliance.property,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Appliance updated successfully.',
            )

            return redirect(
                'appliances:appliance_detail',
                public_id=appliance.public_id,
            )
    else:
        form = ApplianceForm(
            instance=appliance,
            property_obj=appliance.property,
        )

    context = {
        'form': form,
        'appliance': appliance,
        'property': appliance.property,
    }

    return render(
        request,
        'appliances/appliance_form.html',
        context,
    )


@login_required
def appliance_delete(request, public_id):
    appliance = get_object_or_404(
        Appliance,
        public_id=public_id,
        property__owner=request.user,
    )

    property_public_id = appliance.property.public_id

    if request.method == 'POST':
        appliance.delete()

        messages.success(
            request,
            'Appliance deleted successfully.',
        )

        return redirect(
            'properties:property_detail',
            public_id=property_public_id,
        )

    context = {
        'appliance': appliance,
        'property': appliance.property,
    }

    return render(
        request,
        'appliances/appliance_confirm_delete.html',
        context,
    )
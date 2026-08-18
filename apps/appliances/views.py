from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.properties.models import Property

from .forms import ApplianceForm, WarrantyForm
from .models import Appliance, Warranty


def get_accessible_appliances(user):
    if user.is_staff:
        return Appliance.objects.all()

    return Appliance.objects.filter(
        property__owner=user
    )


def appliance_qr_preview(request, public_id):
    appliance = get_object_or_404(
        Appliance,
        public_id=public_id,
        has_individual_qr=True,
    )

    if request.user.is_authenticated:
        accessible_appliance = get_object_or_404(
            get_accessible_appliances(request.user),
            public_id=public_id,
        )

        return redirect(
            'appliances:appliance_detail',
            public_id=accessible_appliance.public_id,
        )

    appliance_detail_url = reverse(
        'appliances:appliance_detail',
        kwargs={
            'public_id': appliance.public_id,
        },
    )

    login_url = (
        reverse('accounts:login')
        + '?next='
        + appliance_detail_url
    )

    context = {
        'appliance': appliance,
        'property': appliance.property,
        'login_url': login_url,
    }

    return render(
        request,
        'appliances/appliance_qr_preview.html',
        context,
    )


@login_required
def appliance_create(request, property_public_id):
    if request.user.is_staff:
        property_obj = get_object_or_404(
            Property,
            public_id=property_public_id,
        )
    else:
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
        form = ApplianceForm(
            property_obj=property_obj,
        )

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
        get_accessible_appliances(request.user),
        public_id=public_id,
    )

    warranty = getattr(
        appliance,
        'warranty',
        None,
    )

    context = {
        'appliance': appliance,
        'property': appliance.property,
        'warranty': warranty,
    }

    return render(
        request,
        'appliances/appliance_detail.html',
        context,
    )


@login_required
def appliance_update(request, public_id):
    appliance = get_object_or_404(
        get_accessible_appliances(request.user),
        public_id=public_id,
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
        get_accessible_appliances(request.user),
        public_id=public_id,
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


@login_required
def warranty_create(request, appliance_public_id):
    appliance = get_object_or_404(
        get_accessible_appliances(request.user),
        public_id=appliance_public_id,
    )

    existing_warranty = getattr(
        appliance,
        'warranty',
        None,
    )

    if existing_warranty:
        messages.info(
            request,
            'This appliance already has a warranty. '
            'You can update the existing warranty instead.',
        )

        return redirect(
            'appliances:warranty_update',
            public_id=existing_warranty.public_id,
        )

    if request.method == 'POST':
        form = WarrantyForm(request.POST)

        if form.is_valid():
            warranty = form.save(commit=False)
            warranty.appliance = appliance
            warranty.save()

            messages.success(
                request,
                'Warranty added successfully.',
            )

            return redirect(
                'appliances:appliance_detail',
                public_id=appliance.public_id,
            )
    else:
        form = WarrantyForm()

    context = {
        'form': form,
        'appliance': appliance,
        'property': appliance.property,
    }

    return render(
        request,
        'appliances/warranty_form.html',
        context,
    )


@login_required
def warranty_update(request, public_id):
    if request.user.is_staff:
        warranty = get_object_or_404(
            Warranty,
            public_id=public_id,
        )
    else:
        warranty = get_object_or_404(
            Warranty,
            public_id=public_id,
            appliance__property__owner=request.user,
        )

    if request.method == 'POST':
        form = WarrantyForm(
            request.POST,
            instance=warranty,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Warranty updated successfully.',
            )

            return redirect(
                'appliances:appliance_detail',
                public_id=warranty.appliance.public_id,
            )
    else:
        form = WarrantyForm(
            instance=warranty,
        )

    context = {
        'form': form,
        'warranty': warranty,
        'appliance': warranty.appliance,
        'property': warranty.appliance.property,
    }

    return render(
        request,
        'appliances/warranty_form.html',
        context,
    )


@login_required
def warranty_delete(request, public_id):
    if request.user.is_staff:
        warranty = get_object_or_404(
            Warranty,
            public_id=public_id,
        )
    else:
        warranty = get_object_or_404(
            Warranty,
            public_id=public_id,
            appliance__property__owner=request.user,
        )

    appliance_public_id = warranty.appliance.public_id

    if request.method == 'POST':
        warranty.delete()

        messages.success(
            request,
            'Warranty deleted successfully.',
        )

        return redirect(
            'appliances:appliance_detail',
            public_id=appliance_public_id,
        )

    context = {
        'warranty': warranty,
        'appliance': warranty.appliance,
        'property': warranty.appliance.property,
    }

    return render(
        request,
        'appliances/warranty_confirm_delete.html',
        context,
    )
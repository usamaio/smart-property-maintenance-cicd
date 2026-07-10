from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PropertyForm
from .models import Property


@login_required
def property_list(request):
    properties = Property.objects.filter(owner=request.user)

    context = {
        'properties': properties,
    }

    return render(request, 'properties/property_list.html', context)


@login_required
def property_detail(request, public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=public_id,
        owner=request.user
    )

    context = {
        'property': property_obj,
    }

    return render(request, 'properties/property_detail.html', context)


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)

        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()

            messages.success(request, 'Property created successfully.')
            return redirect('properties:property_detail', public_id=property_obj.public_id)
    else:
        form = PropertyForm()

    context = {
        'form': form,
    }

    return render(request, 'properties/property_form.html', context)


@login_required
def property_update(request, public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=public_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)

        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('properties:property_detail', public_id=property_obj.public_id)
    else:
        form = PropertyForm(instance=property_obj)

    context = {
        'form': form,
        'property': property_obj,
    }

    return render(request, 'properties/property_form.html', context)


@login_required
def property_delete(request, public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=public_id,
        owner=request.user
    )

    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully.')
        return redirect('properties:property_list')

    context = {
        'property': property_obj,
    }

    return render(request, 'properties/property_confirm_delete.html', context)
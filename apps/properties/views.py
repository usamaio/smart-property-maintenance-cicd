from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PropertyForm, RoomForm
from .models import Property, Room


@login_required
def property_list(request):
    properties = Property.objects.filter(owner=request.user)

    context = {
        'properties': properties,
    }

    return render(
        request,
        'properties/property_list.html',
        context
    )


@login_required
def property_detail(request, public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=public_id,
        owner=request.user
    )

    rooms = property_obj.rooms.all()

    context = {
        'property': property_obj,
        'rooms': rooms,
    }

    return render(
        request,
        'properties/property_detail.html',
        context
    )


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)

        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()

            messages.success(
                request,
                'Property created successfully.'
            )

            return redirect(
                'properties:property_detail',
                public_id=property_obj.public_id
            )
    else:
        form = PropertyForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'properties/property_form.html',
        context
    )


@login_required
def property_update(request, public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=public_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = PropertyForm(
            request.POST,
            instance=property_obj
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Property updated successfully.'
            )

            return redirect(
                'properties:property_detail',
                public_id=property_obj.public_id
            )
    else:
        form = PropertyForm(instance=property_obj)

    context = {
        'form': form,
        'property': property_obj,
    }

    return render(
        request,
        'properties/property_form.html',
        context
    )


@login_required
def property_delete(request, public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=public_id,
        owner=request.user
    )

    if request.method == 'POST':
        property_obj.delete()

        messages.success(
            request,
            'Property deleted successfully.'
        )

        return redirect('properties:property_list')

    context = {
        'property': property_obj,
    }

    return render(
        request,
        'properties/property_confirm_delete.html',
        context
    )


@login_required
def room_create(request, property_public_id):
    property_obj = get_object_or_404(
        Property,
        public_id=property_public_id,
        owner=request.user
    )

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.property = property_obj
            room.save()

            messages.success(
                request,
                'Room added successfully.'
            )

            return redirect(
                'properties:property_detail',
                public_id=property_obj.public_id
            )
    else:
        form = RoomForm()

    context = {
        'form': form,
        'property': property_obj,
    }

    return render(
        request,
        'properties/room_form.html',
        context
    )


@login_required
def room_update(request, room_public_id):
    room = get_object_or_404(
        Room,
        public_id=room_public_id,
        property__owner=request.user
    )

    if request.method == 'POST':
        form = RoomForm(
            request.POST,
            instance=room
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Room updated successfully.'
            )

            return redirect(
                'properties:property_detail',
                public_id=room.property.public_id
            )
    else:
        form = RoomForm(instance=room)

    context = {
        'form': form,
        'property': room.property,
        'room': room,
    }

    return render(
        request,
        'properties/room_form.html',
        context
    )


@login_required
def room_delete(request, room_public_id):
    room = get_object_or_404(
        Room,
        public_id=room_public_id,
        property__owner=request.user
    )

    property_public_id = room.property.public_id

    if request.method == 'POST':
        room.delete()

        messages.success(
            request,
            'Room deleted successfully.'
        )

        return redirect(
            'properties:property_detail',
            public_id=property_public_id
        )

    context = {
        'room': room,
        'property': room.property,
    }

    return render(
        request,
        'properties/room_confirm_delete.html',
        context
    )
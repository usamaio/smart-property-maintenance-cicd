from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MaintenanceRequestForm
from .models import MaintenanceRequest


@login_required
def maintenance_request_list(request):
    requests = MaintenanceRequest.objects.filter(
        property__owner=request.user,
    ).select_related(
        'property',
        'room',
        'appliance',
        'requested_by',
    )

    selected_status = request.GET.get('status', '').strip()
    selected_priority = request.GET.get('priority', '').strip()

    valid_statuses = {
        choice[0]
        for choice in MaintenanceRequest.STATUS_CHOICES
    }

    valid_priorities = {
        choice[0]
        for choice in MaintenanceRequest.PRIORITY_CHOICES
    }

    if selected_status in valid_statuses:
        requests = requests.filter(status=selected_status)
    else:
        selected_status = ''

    if selected_priority in valid_priorities:
        requests = requests.filter(priority=selected_priority)
    else:
        selected_priority = ''

    context = {
        'maintenance_requests': requests,
        'status_choices': MaintenanceRequest.STATUS_CHOICES,
        'priority_choices': MaintenanceRequest.PRIORITY_CHOICES,
        'selected_status': selected_status,
        'selected_priority': selected_priority,
    }

    return render(
        request,
        'maintenance/maintenance_request_list.html',
        context,
    )


@login_required
def maintenance_request_detail(request, public_id):
    maintenance_request = get_object_or_404(
        MaintenanceRequest.objects.select_related(
            'property',
            'room',
            'appliance',
            'requested_by',
        ),
        public_id=public_id,
        property__owner=request.user,
    )

    context = {
        'maintenance_request': maintenance_request,
    }

    return render(
        request,
        'maintenance/maintenance_request_detail.html',
        context,
    )


@login_required
def maintenance_request_create(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.requested_by = request.user
            maintenance_request.save()

            messages.success(
                request,
                'Maintenance request created successfully.',
            )

            return redirect(
                'maintenance:maintenance_request_detail',
                public_id=maintenance_request.public_id,
            )
    else:
        form = MaintenanceRequestForm(
            user=request.user,
        )

    context = {
        'form': form,
    }

    return render(
        request,
        'maintenance/maintenance_request_form.html',
        context,
    )


@login_required
def maintenance_request_update(request, public_id):
    maintenance_request = get_object_or_404(
        MaintenanceRequest,
        public_id=public_id,
        property__owner=request.user,
    )

    if request.method == 'POST':
        form = MaintenanceRequestForm(
            request.POST,
            instance=maintenance_request,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Maintenance request updated successfully.',
            )

            return redirect(
                'maintenance:maintenance_request_detail',
                public_id=maintenance_request.public_id,
            )
    else:
        form = MaintenanceRequestForm(
            instance=maintenance_request,
            user=request.user,
        )

    context = {
        'form': form,
        'maintenance_request': maintenance_request,
    }

    return render(
        request,
        'maintenance/maintenance_request_form.html',
        context,
    )


@login_required
def maintenance_request_delete(request, public_id):
    maintenance_request = get_object_or_404(
        MaintenanceRequest,
        public_id=public_id,
        property__owner=request.user,
    )

    if request.method == 'POST':
        maintenance_request.delete()

        messages.success(
            request,
            'Maintenance request deleted successfully.',
        )

        return redirect(
            'maintenance:maintenance_request_list',
        )

    context = {
        'maintenance_request': maintenance_request,
    }

    return render(
        request,
        'maintenance/maintenance_request_confirm_delete.html',
        context,
    )
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.appliances.models import Appliance, Warranty
from apps.maintenance.models import (
    MaintenanceRequest,
    MaintenanceSchedule,
    ServiceRecord,
)
from apps.properties.models import Property, Room


User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        matched_user = User.objects.filter(
            username__iexact=username,
        ).first()

        if matched_user is not None:
            user = authenticate(
                request,
                username=matched_user.username,
                password=password,
            )
        else:
            user = None

        if user is not None:
            login(request, user)

            next_url = request.POST.get('next', '').strip()

            if next_url:
                return redirect(next_url)

            return redirect('accounts:dashboard')

        messages.error(
            request,
            'The username or password is incorrect.',
        )

    context = {
        'next': request.GET.get('next', ''),
    }

    return render(
        request,
        'accounts/login.html',
        context,
    )


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)

        messages.success(
            request,
            'You have been logged out successfully.',
        )

    return redirect('accounts:login')


@login_required
def dashboard(request):
    today = timezone.localdate()
    due_soon_date = today + timezone.timedelta(days=30)

    if request.user.is_staff:
        properties = Property.objects.all()

        rooms = Room.objects.all()

        appliances = Appliance.objects.all()

        active_warranties = Warranty.objects.filter(
            expiry_date__gte=today,
        )

        open_requests = MaintenanceRequest.objects.filter(
            status__in=[
                'open',
                'in_progress',
                'on_hold',
            ],
        )

        service_records = ServiceRecord.objects.all()

        overdue_schedules = MaintenanceSchedule.objects.filter(
            is_active=True,
            next_due_date__lt=today,
        )

        upcoming_schedules = MaintenanceSchedule.objects.filter(
            is_active=True,
            next_due_date__gte=today,
            next_due_date__lte=due_soon_date,
        ).select_related(
            'property',
            'appliance',
        ).order_by(
            'next_due_date',
        )[:5]

        recent_requests = MaintenanceRequest.objects.select_related(
            'property',
            'room',
            'appliance',
        ).order_by(
            '-created_at',
        )[:5]

        recent_service_records = ServiceRecord.objects.select_related(
            'appliance',
            'appliance__property',
        ).order_by(
            '-service_date',
            '-created_at',
        )[:5]

    else:
        properties = Property.objects.filter(
            owner=request.user,
        )

        rooms = Room.objects.filter(
            property__owner=request.user,
        )

        appliances = Appliance.objects.filter(
            property__owner=request.user,
        )

        active_warranties = Warranty.objects.filter(
            appliance__property__owner=request.user,
            expiry_date__gte=today,
        )

        open_requests = MaintenanceRequest.objects.filter(
            property__owner=request.user,
            status__in=[
                'open',
                'in_progress',
                'on_hold',
            ],
        )

        service_records = ServiceRecord.objects.filter(
            appliance__property__owner=request.user,
        )

        overdue_schedules = MaintenanceSchedule.objects.filter(
            property__owner=request.user,
            is_active=True,
            next_due_date__lt=today,
        )

        upcoming_schedules = MaintenanceSchedule.objects.filter(
            property__owner=request.user,
            is_active=True,
            next_due_date__gte=today,
            next_due_date__lte=due_soon_date,
        ).select_related(
            'property',
            'appliance',
        ).order_by(
            'next_due_date',
        )[:5]

        recent_requests = MaintenanceRequest.objects.filter(
            property__owner=request.user,
        ).select_related(
            'property',
            'room',
            'appliance',
        ).order_by(
            '-created_at',
        )[:5]

        recent_service_records = ServiceRecord.objects.filter(
            appliance__property__owner=request.user,
        ).select_related(
            'appliance',
            'appliance__property',
        ).order_by(
            '-service_date',
            '-created_at',
        )[:5]

    urgent_requests = open_requests.filter(
        priority='urgent',
    )

    context = {
        'property_count': properties.count(),
        'room_count': rooms.count(),
        'appliance_count': appliances.count(),
        'active_warranty_count': active_warranties.count(),
        'open_request_count': open_requests.count(),
        'urgent_request_count': urgent_requests.count(),
        'service_record_count': service_records.count(),
        'overdue_schedule_count': overdue_schedules.count(),
        'recent_requests': recent_requests,
        'recent_service_records': recent_service_records,
        'upcoming_schedules': upcoming_schedules,
    }

    return render(
        request,
        'accounts/dashboard.html',
        context,
    )
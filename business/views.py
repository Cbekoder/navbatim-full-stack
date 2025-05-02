from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Count, Avg, Q, Sum, F, ExpressionWrapper, fields, Max
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Coalesce

from users.models import BusinessProfile, CustomUser
from services.models import Service, Category, BusinessHours, Review
from appointments.models import Appointment
from .forms import ServiceForm, BusinessProfileForm, BusinessHoursFormSet
# from .models import ClientNote, BlockedClient, AppointmentNote


def is_business_user(user):
    return user.is_authenticated and user.user_type == 'business'


def business_dashboard(request):
    """Main dashboard view for business owners"""
    if is_business_user(request.user):
        try:
            business = request.user.business_profile
        except BusinessProfile.DoesNotExist:
            messages.error(request, "You need to complete your business profile first.")
            return redirect('edit_business_profile')

        # Get today's date
        today = timezone.now().date()

        # Get upcoming appointments for today
        today_appointments = Appointment.objects.filter(
            business=business,
            date=today,
            status__in=['pending', 'confirmed']
        ).order_by('time')

        # Get all upcoming appointments
        upcoming_appointments = Appointment.objects.filter(
            business=business,
            date__gte=today,
            status__in=['pending', 'confirmed']
        ).order_by('date', 'time')[:10]

        # Get appointment analytics
        total_appointments = Appointment.objects.filter(business=business).count()
        completed_appointments = Appointment.objects.filter(business=business, status='completed').count()
        pending_appointments = Appointment.objects.filter(business=business, status='pending').count()
        cancelled_appointments = Appointment.objects.filter(business=business, status='cancelled').count()

        # Recent reviews
        recent_reviews = Review.objects.filter(service__business=business.id).order_by('-created_at')[:5]

        # Average rating
        avg_rating = Review.objects.filter(service__business=business.id).aggregate(Avg('rating'))['rating__avg'] or 0

        # Popular services
        popular_services = Service.objects.filter(business=business).annotate(
            appointment_count=Count('appointments')
        ).order_by('-appointment_count')[:5]

        context = {
            'business': business,
            'today_appointments': today_appointments,
            'upcoming_appointments': upcoming_appointments,
            'total_appointments': total_appointments,
            'completed_appointments': completed_appointments,
            'pending_appointments': pending_appointments,
            'cancelled_appointments': cancelled_appointments,
            'recent_reviews': recent_reviews,
            'avg_rating': avg_rating,
            'popular_services': popular_services,
        }

        return render(request, 'business/dashboard.html', context)
    return redirect('/accounts/login/?next=/business/dashboard/')


def business_services(request):
    """View for managing business services"""
    try:
        business = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        messages.error(request, "You need to complete your business profile first.")
        return redirect('edit_business_profile')

    # Get all services for this business
    services = Service.objects.filter(business=business)

    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        services = services.filter(category_id=category_id)

    # Filter by search query if provided
    query = request.GET.get('q')
    if query:
        services = services.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        is_active = status == 'active'
        services = services.filter(is_active=is_active)

    # Pagination
    paginator = Paginator(services, 10)  # Show 10 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all categories for the filter dropdown
    categories = Category.objects.all()

    context = {
        'services': page_obj,
        'categories': categories,
        'business': business,
        'category_id': category_id,
        'query': query,
        'status': status,
    }

    return render(request, 'business/services.html', context)



def add_service(request):
    """View for adding a new service"""
    try:
        business = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        messages.error(request, "You need to complete your business profile first.")
        return redirect('edit_business_profile')

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.business = business
            service.save()
            messages.success(request, f"Service '{service.name}' added successfully!")
            return redirect('business_services')
    else:
        form = ServiceForm()

    context = {
        'form': form,
        'business': business,
        'is_add': True,
    }

    return render(request, 'business/service_form.html', context)



def edit_service(request, service_id):
    """View for editing an existing service"""
    try:
        business = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        messages.error(request, "You need to complete your business profile first.")
        return redirect('edit_business_profile')

    service = get_object_or_404(Service, id=service_id, business=business)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f"Service '{service.name}' updated successfully!")
            return redirect('business_services')
    else:
        form = ServiceForm(instance=service)

    context = {
        'form': form,
        'business': business,
        'service': service,
        'is_add': False,
    }

    return render(request, 'business/service_form.html', context)



def delete_service(request, service_id):
    """View for deleting a service"""
    try:
        business = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        messages.error(request, "You need to complete your business profile first.")
        return redirect('edit_business_profile')

    service = get_object_or_404(Service, id=service_id, business=business)

    if request.method == 'POST':
        service_name = service.name
        service.delete()
        messages.success(request, f"Service '{service_name}' deleted successfully!")
        return redirect('business_services')

    context = {
        'service': service,
        'business': business,
    }

    return render(request, 'business/service_confirm_delete.html', context)



def toggle_service_status(request, service_id):
    """AJAX view for toggling a service's active status"""
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        business = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        return JsonResponse({'error': 'Business profile not found'}, status=404)

    service = get_object_or_404(Service, id=service_id, business=business)
    service.is_active = not service.is_active
    service.save()

    return JsonResponse({
        'success': True,
        'is_active': service.is_active,
        'service_id': service.id,
    })



# Add this view function for business appointments
@login_required
@user_passes_test(is_business_user)
def business_appointments(request):
    """View for managing business appointments"""
    try:
        business = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        messages.error(request, "You need to complete your business profile first.")
        return redirect('business:edit_business_profile')

    # Get all appointments for this business
    appointments_query = Appointment.objects.filter(business=business)

    # Filter by date range if provided
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from:
        appointments_query = appointments_query.filter(date__gte=date_from)

    if date_to:
        appointments_query = appointments_query.filter(date__lte=date_to)

    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        appointments_query = appointments_query.filter(status=status)

    # Filter by service if provided
    service_id = request.GET.get('service')
    if service_id:
        appointments_query = appointments_query.filter(service_id=service_id)

    # Sort appointments if requested
    sort_by = request.GET.get('sort', 'date')
    order = request.GET.get('order', 'asc')

    if sort_by == 'date':
        order_by = 'date' if order == 'asc' else '-date'
        appointments_query = appointments_query.order_by(order_by, 'time')
    elif sort_by == 'client':
        order_by = 'client__username' if order == 'asc' else '-client__username'
        appointments_query = appointments_query.order_by(order_by)
    elif sort_by == 'service':
        order_by = 'service__name' if order == 'asc' else '-service__name'
        appointments_query = appointments_query.order_by(order_by)
    elif sort_by == 'status':
        order_by = 'status' if order == 'asc' else '-status'
        appointments_query = appointments_query.order_by(order_by)
    else:
        # Default sorting
        appointments_query = appointments_query.order_by('-date', '-time')

    # Pagination
    paginator = Paginator(appointments_query, 10)  # Show 10 appointments per page
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    # Get all services for this business for the filter dropdown
    services = Service.objects.filter(business=business)

    # Get today's date for highlighting
    today = timezone.now().date()

    context = {
        'appointments': appointments,
        'services': services,
        'business': business,
        'date_from': date_from,
        'date_to': date_to,
        'status': status,
        'service_id': service_id,
        'sort_by': sort_by,
        'order': order,
        'today': today,
    }

    return render(request, 'business/appointments.html', context)


@login_required
@user_passes_test(is_business_user)
def update_appointment_status(request, appointment_id):
    """View for updating appointment status via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    try:
        business = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Business profile not found'})

    appointment = get_object_or_404(Appointment, id=appointment_id, business=business)
    new_status = request.POST.get('status')

    if new_status not in dict(Appointment.STATUS_CHOICES):
        return JsonResponse({'success': False, 'error': 'Invalid status'})

    appointment.status = new_status
    appointment.save()

    return JsonResponse({'success': True})


# Existing views...

# @login_required
# @user_passes_test(is_business_user)
# def business_clients(request):
#     """View for managing business clients"""
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     # Get all clients who have had appointments with this business
#     client_query = CustomUser.objects.filter(
#         appointments__business=business,
#         user_type='client'
#     ).distinct()
#
#     # Search filter
#     query = request.GET.get('q')
#     if query:
#         client_query = client_query.filter(
#             Q(username__icontains=query) |
#             Q(first_name__icontains=query) |
#             Q(last_name__icontains=query) |
#             Q(email__icontains=query) |
#             Q(phone_number__icontains=query)
#         )
#
#     # Visit count filter
#     visits = request.GET.get('visits')
#     if visits:
#         if visits == '0':
#             client_query = client_query.annotate(
#                 visit_count=Count('appointments', filter=Q(appointments__business=business))
#             ).filter(visit_count=1)
#         elif visits == '1-3':
#             client_query = client_query.annotate(
#                 visit_count=Count('appointments', filter=Q(appointments__business=business))
#             ).filter(visit_count__gt=1, visit_count__lte=3)
#         elif visits == '4-10':
#             client_query = client_query.annotate(
#                 visit_count=Count('appointments', filter=Q(appointments__business=business))
#             ).filter(visit_count__gt=3, visit_count__lte=10)
#         elif visits == '10+':
#             client_query = client_query.annotate(
#                 visit_count=Count('appointments', filter=Q(appointments__business=business))
#             ).filter(visit_count__gt=10)
#
#     # Last visit filter
#     last_visit = request.GET.get('last_visit')
#     if last_visit:
#         today = timezone.now().date()
#         if last_visit == 'week':
#             date_threshold = today - timezone.timedelta(days=7)
#         elif last_visit == 'month':
#             date_threshold = today - timezone.timedelta(days=30)
#         elif last_visit == '3months':
#             date_threshold = today - timezone.timedelta(days=90)
#         elif last_visit == '6months':
#             date_threshold = today - timezone.timedelta(days=180)
#         elif last_visit == 'year':
#             date_threshold = today - timezone.timedelta(days=365)
#
#         client_query = client_query.filter(
#             appointments__business=business,
#             appointments__date__gte=date_threshold
#         )
#
#     # Annotate with visit count, last visit date, and total spent
#     clients_with_stats = client_query.annotate(
#         visit_count=Count('appointments', filter=Q(appointments__business=business)),
#         last_visit=Max('appointments__date', filter=Q(appointments__business=business)),
#         total_spent=Coalesce(Sum(
#             'appointments__service__price',
#             filter=Q(appointments__business=business, appointments__status='completed')
#         ), 0)
#     ).order_by('-last_visit')
#
#     # Check which clients are blocked
#     blocked_clients = BlockedClient.objects.filter(business=business).values_list('client_id', flat=True)
#
#     # Pagination
#     paginator = Paginator(clients_with_stats, 20)  # Show 20 clients per page
#     page_number = request.GET.get('page')
#     clients = paginator.get_page(page_number)
#
#     context = {
#         'clients': clients,
#         'business': business,
#         'blocked_clients': blocked_clients,
#     }
#
#     return render(request, 'business/clients.html', context)
#
#
# @login_required
# @user_passes_test(is_business_user)
# def client_detail(request, client_id):
#     """View for client details"""
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     # Get client
#     client = get_object_or_404(CustomUser, id=client_id, user_type='client')
#
#     # Check if client has had appointments with this business
#     has_appointments = Appointment.objects.filter(business=business, client=client).exists()
#     if not has_appointments:
#         messages.error(request, "This client has not had any appointments with your business.")
#         return redirect('business:clients')
#
#     # Get client profile
#     try:
#         client_profile = client.client_profile
#     except:
#         client_profile = None
#
#     # Check if client is blocked
#     is_blocked = BlockedClient.objects.filter(business=business, client=client).exists()
#
#     # Get client notes
#     notes = ClientNote.objects.filter(business=business, client=client)
#
#     # Get client stats
#     appointments = Appointment.objects.filter(business=business, client=client)
#     total_appointments = appointments.count()
#     completed_appointments = appointments.filter(status='completed').count()
#     cancelled_appointments = appointments.filter(status='cancelled').count()
#
#     # Calculate total and average spent
#     completed_with_price = appointments.filter(status='completed').select_related('service')
#     total_spent = sum(apt.service.price for apt in completed_with_price)
#     avg_spent = total_spent / completed_appointments if completed_appointments > 0 else 0
#
#     # Get most used service
#     service_counts = {}
#     for apt in appointments:
#         service_name = apt.service.name
#         if service_name in service_counts:
#             service_counts[service_name] += 1
#         else:
#             service_counts[service_name] = 1
#
#     most_used_service = None
#     max_count = 0
#     for service_name, count in service_counts.items():
#         if count > max_count:
#             most_used_service = service_name
#             max_count = count
#
#     # Get last appointment date
#     last_appointment = appointments.order_by('-date', '-time').first()
#
#     stats = {
#         'total_appointments': total_appointments,
#         'completed_appointments': completed_appointments,
#         'cancelled_appointments': cancelled_appointments,
#         'total_spent': total_spent,
#         'avg_spent': avg_spent,
#         'most_used_service': most_used_service,
#         'last_appointment': last_appointment.date if last_appointment else None,
#     }
#
#     context = {
#         'client': client,
#         'client_profile': client_profile,
#         'business': business,
#         'is_blocked': is_blocked,
#         'notes': notes,
#         'stats': stats,
#     }
#
#     return render(request, 'business/client_detail.html', context)
#
#
# @login_required
# @user_passes_test(is_business_user)
# def client_appointments(request, client_id):
#     """View for client appointments history"""
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     # Get client
#     client = get_object_or_404(CustomUser, id=client_id, user_type='client')
#
#     # Get appointments
#     appointments_query = Appointment.objects.filter(business=business, client=client)
#
#     # Filter by date range if provided
#     date_from = request.GET.get('date_from')
#     date_to = request.GET.get('date_to')
#
#     if date_from:
#         appointments_query = appointments_query.filter(date__gte=date_from)
#
#     if date_to:
#         appointments_query = appointments_query.filter(date__lte=date_to)
#
#     # Filter by status if provided
#     status = request.GET.get('status')
#     if status:
#         appointments_query = appointments_query.filter(status=status)
#
#     # Order appointments
#     appointments_query = appointments_query.order_by('-date', '-time')
#
#     # Pagination
#     paginator = Paginator(appointments_query, 10)  # Show 10 appointments per page
#     page_number = request.GET.get('page')
#     appointments = paginator.get_page(page_number)
#
#     context = {
#         'client': client,
#         'business': business,
#         'appointments': appointments,
#     }
#
#     return render(request, 'business/client_appointments.html', context)
#
#
# @login_required
# @user_passes_test(is_business_user)
# def add_client_note(request):
#     """View for adding a note about a client"""
#     if request.method != 'POST':
#         return redirect('business:clients')
#
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     client_id = request.POST.get('client_id')
#     note_text = request.POST.get('note')
#     redirect_to = request.POST.get('redirect_to', 'list')
#
#     if not client_id or not note_text:
#         messages.error(request, "Client ID and note text are required.")
#         if redirect_to == 'detail':
#             return redirect('business:client_detail', client_id=client_id)
#         return redirect('business:clients')
#
#     client = get_object_or_404(CustomUser, id=client_id, user_type='client')
#
#     # Create note
#     ClientNote.objects.create(
#         client=client,
#         business=business,
#         text=note_text,
#         created_by=request.user
#     )
#
#     messages.success(request, "Note added successfully.")
#
#     if redirect_to == 'detail':
#         return redirect('business:client_detail', client_id=client_id)
#     return redirect('business:clients')
#
#
# @login_required
# @user_passes_test(is_business_user)
# def delete_client_note(request):
#     """View for deleting a client note"""
#     if request.method != 'POST':
#         return redirect('business:clients')
#
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     note_id = request.POST.get('note_id')
#     redirect_to = request.POST.get('redirect_to', 'list')
#
#     if not note_id:
#         messages.error(request, "Note ID is required.")
#         return redirect('business:clients')
#
#     note = get_object_or_404(ClientNote, id=note_id, business=business)
#     client_id = note.client.id
#     note.delete()
#
#     messages.success(request, "Note deleted successfully.")
#
#     if redirect_to == 'detail':
#         return redirect('business:client_detail', client_id=client_id)
#     return redirect('business:clients')
#
#
# @login_required
# @user_passes_test(is_business_user)
# def block_client(request):
#     """View for blocking a client"""
#     if request.method != 'POST':
#         return redirect('business:clients')
#
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     client_id = request.POST.get('client_id')
#     reason = request.POST.get('reason')
#     redirect_to = request.POST.get('redirect_to', 'list')
#
#     if not client_id or not reason:
#         messages.error(request, "Client ID and reason are required.")
#         if redirect_to == 'detail':
#             return redirect('business:client_detail', client_id=client_id)
#         return redirect('business:clients')
#
#     client = get_object_or_404(CustomUser, id=client_id, user_type='client')
#
#     # Create blocked client entry
#     BlockedClient.objects.create(
#         client=client,
#         business=business,
#         reason=reason
#     )
#
#     messages.success(request, f"{client.get_full_name() or client.username} has been blocked.")
#
#     if redirect_to == 'detail':
#         return redirect('business:client_detail', client_id=client_id)
#     return redirect('business:clients')
#
#
# @login_required
# @user_passes_test(is_business_user)
# def unblock_client(request, client_id):
#     """View for unblocking a client"""
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     client = get_object_or_404(CustomUser, id=client_id)
#     blocked = get_object_or_404(BlockedClient, client=client, business=business)
#     blocked.delete()
#
#     messages.success(request, f"{client.get_full_name() or client.username} has been unblocked.")
#     return redirect('business:client_detail', client_id=client_id)
#
#
# @login_required
# @user_passes_test(is_business_user)
# def add_appointment_note(request):
#     """View for adding a note to an appointment"""
#     if request.method != 'POST':
#         return redirect('business:business_appointments')
#
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     appointment_id = request.POST.get('appointment_id')
#     note_text = request.POST.get('note')
#     redirect_to = request.POST.get('redirect_to', 'appointments')
#     client_id = request.POST.get('client_id')
#
#     if not appointment_id or not note_text:
#         messages.error(request, "Appointment ID and note text are required.")
#         if redirect_to == 'client_appointments' and client_id:
#             return redirect('business:client_appointments', client_id=client_id)
#         return redirect('business:business_appointments')
#
#     appointment = get_object_or_404(Appointment, id=appointment_id, business=business)
#
#     # Create note
#     AppointmentNote.objects.create(
#         appointment=appointment,
#         text=note_text,
#         created_by=request.user
#     )
#
#     messages.success(request, "Note added successfully.")
#
#     if redirect_to == 'client_appointments' and client_id:
#         return redirect('business:client_appointments', client_id=client_id)
#     return redirect('business:business_appointments')
#
#
# @login_required
# @user_passes_test(is_business_user)
# def export_clients(request):
#     """View for exporting clients data"""
#     try:
#         business = request.user.business_profile
#     except BusinessProfile.DoesNotExist:
#         messages.error(request, "You need to complete your business profile first.")
#         return redirect('business:edit_business_profile')
#
#     # Get export format
#     export_format = request.GET.get('format', 'csv')
#     include_notes = request.GET.get('include_notes') == '1'
#     include_appointments = request.GET.get('include_appointments') == '1'
#
#     # Get clients
#     clients = CustomUser.objects.filter(
#         appointments__business=business,
#         user_type='client'
#     ).distinct().annotate(
#         visit_count=Count('appointments', filter=Q(appointments__business=business)),
#         last_visit=Max('appointments__date', filter=Q(appointments__business=business)),
#         total_spent=Coalesce(Sum(
#             'appointments__service__price',
#             filter=Q(appointments__business=business, appointments__status='completed')
#         ), 0)
#     )
#
#     # Generate export file
#     if export_format == 'csv':
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="clients.csv"'
#         # Implementation of CSV export would go here
#         response.write('Client export functionality will be implemented soon.')
#     else:  # excel
#         response = HttpResponse(content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="clients.xlsx"'
#         # Implementation of Excel export would go here
#         response.write('Client export functionality will be implemented soon.')
#
#     return response
#
# # Update business/urls.py to include these new views

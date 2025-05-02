from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm
from services.models import Service, BusinessProfile


def appointment_list(request):
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        client=request.user,
        date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    ).order_by('date', 'time')
    
    # Get past appointments
    past_appointments = Appointment.objects.filter(
        client=request.user,
        date__lt=timezone.now().date(),
        status__in=['completed', 'cancelled']
    ).order_by('-date', '-time')
    
    # Get cancelled appointments
    cancelled_appointments = Appointment.objects.filter(
        client=request.user,
        status='cancelled'
    ).order_by('-date', '-time')
    
    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'cancelled_appointments': cancelled_appointments,
    }
    
    return render(request, 'appointments/appointment_list.html', context)


def book_appointment(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    business = service.business
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.business = business
            appointment.service = service
            appointment.save()
            messages.success(request,
                             f"{service.name} xizmati uchun {business.business_name} biznesida navbat muvaffaqiyatli band qilindi!")
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
        'service': service,
        'business': business,
    }
    
    return render(request, 'appointments/book_appointment.html', context)


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, client=request.user)
    
    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Your appointment has been cancelled.")
    else:
        messages.error(request, "This appointment cannot be cancelled.")
    
    return redirect('appointment_list')


def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, client=request.user)
    
    if appointment.status in ['pending', 'confirmed']:
        if request.method == 'POST':
            form = AppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                form.save()
                messages.success(request, "Your appointment has been rescheduled.")
                return redirect('appointment_list')
        else:
            form = AppointmentForm(instance=appointment)
        
        context = {
            'form': form,
            'appointment': appointment,
        }
        
        return render(request, 'appointments/reschedule_appointment.html', context)
    else:
        messages.error(request, "This appointment cannot be rescheduled.")
        return redirect('appointment_list')

"""python file="appointments/forms.py" type="code"""""

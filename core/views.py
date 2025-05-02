from django.shortcuts import render, redirect
from django.contrib import messages
from services.models import Category, BusinessProfile, Deal
from django.db.models import Avg, Count
from .forms import ContactForm
from .models import Testimonial


def home(request):
    categories = Category.objects.all()

    # Fix: Use services__reviews instead of reviews
    popular_businesses = BusinessProfile.objects.annotate(
        avg_rating=Avg('services__reviews__rating'),
        review_count=Count('services__reviews')
    ).filter(is_verified=True).order_by('-avg_rating', '-review_count')[:5]

    premium_businesses = BusinessProfile.objects.filter(is_premium=True).order_by('?')[:1]

    deals = Deal.objects.filter(is_active=True).order_by('-created_at')[:3]

    new_businesses = BusinessProfile.objects.filter(is_verified=True).order_by('-created_at')[:4]

    # Fix: Use services__reviews instead of reviews
    businesses = BusinessProfile.objects.annotate(
        avg_rating=Avg('services__reviews__rating'),
        review_count=Count('services__reviews')
    ).filter(is_verified=True).order_by('-avg_rating')[:6]

    testimonials = Testimonial.objects.filter(is_active=True).order_by('?')[:3]

    context = {
        'categories': categories,
        'popular_businesses': popular_businesses,
        'premium_businesses': premium_businesses,
        'deals': deals,
        'new_businesses': new_businesses,
        'businesses': businesses,
        'testimonials': testimonials,
    }

    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. We'll get back to you soon!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


def terms(request):
    return render(request, 'core/terms.html')


def privacy(request):
    return render(request, 'core/privacy.html')

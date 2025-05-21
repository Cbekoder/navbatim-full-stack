from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import BusinessProfile
from .models import Category, Service, Review, BusinessHours, Favorite
from .forms import ReviewForm


def service_list(request):
    # Get filter parameters
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'popularity')
    city = request.GET.get('city', '')
    business_type = request.GET.get('type', 'all')
    is_vip = request.GET.get('vip', False)
    award_winners = request.GET.get('award_winners', False)

    # Get selected categories
    selected_categories = request.GET.getlist('category')

    # Base queryset
    businesses = BusinessProfile.objects.annotate(
        avg_rating=Avg('services__reviews__rating'),
        review_count=Count('services__reviews')
    )

    # Apply filters
    if query:
        businesses = businesses.filter(business_name__icontains=query)

    if city:
        businesses = businesses.filter(city=city)

    if selected_categories:
        businesses = businesses.filter(categories__id__in=selected_categories).distinct()

    if business_type == 'companies':
        businesses = businesses.filter(is_company=True)
    elif business_type == 'specialists':
        businesses = businesses.filter(is_company=False)

    if is_vip:
        businesses = businesses.filter(is_premium=True)

    if award_winners:
        businesses = businesses.filter(has_award=True)

    # Apply sorting
    if sort == 'rating':
        businesses = businesses.order_by('-avg_rating')
    elif sort == 'reviews':
        businesses = businesses.order_by('-review_count')
    elif sort == 'price-low':
        businesses = businesses.order_by('services__price')
    elif sort == 'price-high':
        businesses = businesses.order_by('-services__price')
    else:  # popularity
        businesses = businesses.order_by('-review_count', '-avg_rating')

    # Get all categories for the filter
    categories = Category.objects.all()

    context = {
        'businesses': businesses,
        'categories': categories,
        'selected_categories': selected_categories,
    }

    return render(request, 'services/service_list.html', context)


def business_detail(request, pk):
    business = get_object_or_404(BusinessProfile, pk=pk)
    services = Service.objects.filter(business=business)
    reviews = Review.objects.filter(service__business=business).order_by('-created_at')

    # Get business hours
    business_hours = BusinessHours.objects.filter(business=business).order_by('day')

    # Create a dictionary of business hours by day for easier access in the template
    hours_by_day = {}
    for hours in business_hours:
        hours_by_day[hours.day] = hours

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Check if user has favorited this business
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = business in request.user.favorites.all()

    context = {
        'business': business,
        'services': services,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_favorite': is_favorite,
        'business_hours': business_hours,
        'hours_by_day': hours_by_day,
        'days_of_week': BusinessHours.DAYS_OF_WEEK,
    }

    return render(request, 'services/business_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    services = Service.objects.filter(category=category)

    businesses = BusinessProfile.objects.filter(services__in=services).distinct().annotate(
        avg_rating=Avg('services__reviews__rating'),
        review_count=Count('services__reviews')
    )

    context = {
        'category': category,
        'businesses': businesses,
    }

    return render(request, 'services/category_detail.html', context)


@login_required
def add_favorite(request, business_id):
    if not request.user.is_authenticated:
        business = get_object_or_404(BusinessProfile, id=business_id)
        user = request.user

        if business not in Favorite.objects.filter(user=user).values_list('business', flat=True):
            Favorite.objects.create(user=user, business=business)

        next_url = request.GET.get('next', reverse('services:service_list'))
        return HttpResponseRedirect(next_url)
    return redirect('account_login')



@login_required
def remove_favorite(request, business_id):
    if not request.user.is_authenticated:
        business = get_object_or_404(BusinessProfile, id=business_id)
        user = request.user

        if business in user.favorites.all():
            user.favorites.remove(business)

        next_url = request.GET.get('next', reverse('services:service_list'))
        return HttpResponseRedirect(next_url)
    return redirect('account_login')


@login_required
def add_review(request, business_id):
    business = get_object_or_404(BusinessProfile, id=business_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Sizning bahongiz muvaffaqiyatli qo\'shildi!')
            return redirect('services/business', pk=business_id)
    else:
        form = ReviewForm(initial={'service': business.services.first()})

    context = {
        'form': form,
        'business': business,
    }

    return render(request, 'services/add_review.html', context)


def deals_list(request):
    deals = Service.objects.filter(has_discount=True).select_related('business')

    context = {
        'deals': deals,
    }

    return render(request, 'services/deals_list.html', context)


def map_view(request):
    businesses = BusinessProfile.objects.filter(latitude__isnull=False, longitude__isnull=False)

    context = {
        'businesses': businesses,
    }

    return render(request, 'services/map_view.html', context)

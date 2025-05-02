from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from services.models import Category, Service, BusinessProfile, Review, BusinessHours, Deal
from appointments.models import Appointment
from core.models import Testimonial
from users.models import BusinessProfile, ClientProfile
import random
from datetime import timedelta, datetime, time

User = get_user_model()


class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        self.create_categories()

        # Create users
        self.create_users()

        # Create businesses
        self.create_businesses()

        # Create services
        self.create_services()

        # Create business hours
        self.create_business_hours()

        # Create reviews
        self.create_reviews()

        # Create deals
        self.create_deals()

        # Create testimonials
        self.create_testimonials()

        # Create appointments
        self.create_appointments()

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_categories(self):
        categories = [
            {
                'name': "Go'zallik",
                'slug': 'beauty',
                'icon': 'scissors',
                'icon_color': 'bg-pink-100 text-pink-500',
                'order': 1
            },
            {
                'name': "Sog'liq",
                'slug': 'health',
                'icon': 'heart',
                'icon_color': 'bg-teal-100 text-teal-500',
                'order': 2
            },
            {
                'name': "Avto",
                'slug': 'auto',
                'icon': 'car-front',
                'icon_color': 'bg-blue-100 text-blue-500',
                'order': 3
            },
            {
                'name': "Ko'ngil ochar",
                'slug': 'entertainment',
                'icon': 'music-note',
                'icon_color': 'bg-orange-100 text-orange-500',
                'order': 4
            },
            {
                'name': "Xizmatlar",
                'slug': 'services',
                'icon': 'briefcase',
                'icon_color': 'bg-purple-100 text-purple-500',
                'order': 5
            },
            {
                'name': "Ta'lim",
                'slug': 'education',
                'icon': 'mortarboard',
                'icon_color': 'bg-red-100 text-red-500',
                'order': 6
            },
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                slug=category_data['slug'],
                defaults=category_data
            )

        self.stdout.write(f'Created {len(categories)} categories')

    def create_users(self):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'user_type': 'business'
            }
        )

        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Create business users
        business_users = [
            {
                'username': 'beauty_zone',
                'email': 'beauty@example.com',
                'first_name': 'Beauty',
                'last_name': 'Zone',
                'user_type': 'business',
                'phone_number': '+998 90 123 45 67'
            },
            {
                'username': 'health_style',
                'email': 'health@example.com',
                'first_name': 'Health',
                'last_name': 'Style',
                'user_type': 'business',
                'phone_number': '+998 90 234 56 78'
            },
            {
                'username': 'glamour',
                'email': 'glamour@example.com',
                'first_name': 'Glamour',
                'last_name': 'Salon',
                'user_type': 'business',
                'phone_number': '+998 90 345 67 89'
            },
            {
                'username': 'medispa',
                'email': 'medispa@example.com',
                'first_name': 'Medi',
                'last_name': 'Spa',
                'user_type': 'business',
                'phone_number': '+998 90 456 78 90'
            },
            {
                'username': 'elite_clinic',
                'email': 'elite@example.com',
                'first_name': 'Elite',
                'last_name': 'Clinic',
                'user_type': 'business',
                'phone_number': '+998 90 567 89 01'
            },
            {
                'username': 'nail_art',
                'email': 'nail@example.com',
                'first_name': 'Nail',
                'last_name': 'Art',
                'user_type': 'business',
                'phone_number': '+998 90 678 90 12'
            },
            {
                'username': 'barber_shop',
                'email': 'barber@example.com',
                'first_name': 'Barber',
                'last_name': 'Shop',
                'user_type': 'business',
                'phone_number': '+998 90 789 01 23'
            },
            {
                'username': 'dental_clinic',
                'email': 'dental@example.com',
                'first_name': 'Dental',
                'last_name': 'Clinic',
                'user_type': 'business',
                'phone_number': '+998 90 890 12 34'
            },
            {
                'username': 'fitness_center',
                'email': 'fitness@example.com',
                'first_name': 'Fitness',
                'last_name': 'Center',
                'user_type': 'business',
                'phone_number': '+998 90 901 23 45'
            },
            {
                'username': 'spa_relax',
                'email': 'spa@example.com',
                'first_name': 'Spa',
                'last_name': 'Relax',
                'user_type': 'business',
                'phone_number': '+998 90 012 34 56'
            },
        ]

        for user_data in business_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )

            if created:
                user.set_password('password123')
                user.save()

        # Create client users
        client_users = [
            {
                'username': 'client1',
                'email': 'client1@example.com',
                'first_name': 'Aziz',
                'last_name': 'Karimov',
                'user_type': 'client',
                'phone_number': '+998 90 111 22 33'
            },
            {
                'username': 'client2',
                'email': 'client2@example.com',
                'first_name': 'Dilshod',
                'last_name': 'Rahimov',
                'user_type': 'client',
                'phone_number': '+998 90 222 33 44'
            },
            {
                'username': 'client3',
                'email': 'client3@example.com',
                'first_name': 'Malika',
                'last_name': 'Saidova',
                'user_type': 'client',
                'phone_number': '+998 90 333 44 55'
            },
            {
                'username': 'client4',
                'email': 'client4@example.com',
                'first_name': 'Nodira',
                'last_name': 'Aliyeva',
                'user_type': 'client',
                'phone_number': '+998 90 444 55 66'
            },
            {
                'username': 'client5',
                'email': 'client5@example.com',
                'first_name': 'Rustam',
                'last_name': 'Umarov',
                'user_type': 'client',
                'phone_number': '+998 90 555 66 77'
            },
            {
                'username': 'client6',
                'email': 'client6@example.com',
                'first_name': 'Zarina',
                'last_name': 'Yusupova',
                'user_type': 'client',
                'phone_number': '+998 90 666 77 88'
            },
            {
                'username': 'client7',
                'email': 'client7@example.com',
                'first_name': 'Timur',
                'last_name': 'Azimov',
                'user_type': 'client',
                'phone_number': '+998 90 777 88 99'
            },
            {
                'username': 'client8',
                'email': 'client8@example.com',
                'first_name': 'Gulnora',
                'last_name': 'Kamalova',
                'user_type': 'client',
                'phone_number': '+998 90 888 99 00'
            },
            {
                'username': 'client9',
                'email': 'client9@example.com',
                'first_name': 'Akbar',
                'last_name': 'Toshmatov',
                'user_type': 'client',
                'phone_number': '+998 90 999 00 11'
            },
            {
                'username': 'client10',
                'email': 'client10@example.com',
                'first_name': 'Lola',
                'last_name': 'Mirzayeva',
                'user_type': 'client',
                'phone_number': '+998 90 000 11 22'
            },
        ]

        for user_data in client_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )

            if created:
                user.set_password('password123')
                user.save()

                # Create client profile
                ClientProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'gender': random.choice(['male', 'female']),
                        'birth_date': timezone.now().date() - timedelta(days=random.randint(7000, 15000))
                    }
                )

        self.stdout.write(f'Created {len(business_users) + len(client_users) + 1} users')

    def create_businesses(self):
        business_data = [
            {
                'user': User.objects.get(username='beauty_zone'),
                'business_name': 'Beauty Zone',
                'description': 'Professional beauty salon offering a wide range of services.',
                'address': 'Navoiy ko\'chasi, 15',
                'city': 'Toshkent',
                'district': 'Mirobod',
                'latitude': 41.311081,
                'longitude': 69.240562,
                'is_premium': True,
                'is_verified': True,
                'logo': 'business_logos/beauty_zone.png',
                'cover_image': 'business_covers/beauty_zone_cover.jpg',
                'website': 'https://beautyzone.uz',
                'instagram': 'beauty_zone_uz',
                'telegram': '@beauty_zone',
                'facebook': 'beautyzone.uz'
            },
            {
                'user': User.objects.get(username='health_style'),
                'business_name': 'Health & Style',
                'description': 'Health and beauty services for your wellbeing.',
                'address': 'Samarqand ko\'chasi, 22',
                'city': 'Toshkent',
                'district': 'Yunusobod',
                'latitude': 41.325678,
                'longitude': 69.287654,
                'is_premium': False,
                'is_verified': True,
                'logo': 'business_logos/health_style.png',
                'cover_image': 'business_covers/health_style_cover.jpg',
                'website': 'https://healthstyle.uz',
                'instagram': 'health_style_uz',
                'telegram': '@health_style',
                'facebook': 'healthstyle.uz'
            },
            {
                'user': User.objects.get(username='glamour'),
                'business_name': 'Glamour',
                'description': 'Luxury beauty salon for those who appreciate quality.',
                'address': 'Amir Temur ko\'chasi, 107',
                'city': 'Toshkent',
                'district': 'Chilonzor',
                'latitude': 41.298765,
                'longitude': 69.254321,
                'is_premium': False,
                'is_verified': True,
                'logo': 'business_logos/glamour.png',
                'cover_image': 'business_covers/glamour_cover.jpg',
                'website': 'https://glamour.uz',
                'instagram': 'glamour_uz',
                'telegram': '@glamour',
                'facebook': 'glamour.uz'
            },
            {
                'user': User.objects.get(username='medispa'),
                'business_name': 'MediSpa',
                'description': 'Medical spa offering both medical and cosmetic treatments.',
                'address': 'Shayxontohur, 42',
                'city': 'Toshkent',
                'district': 'Shayxontohur',
                'latitude': 41.312345,
                'longitude': 69.223456,
                'is_premium': False,
                'is_verified': True,
                'logo': 'business_logos/medispa.png',
                'cover_image': 'business_covers/medispa_cover.jpg',
                'website': 'https://medispa.uz',
                'instagram': 'medispa_uz',
                'telegram': '@medispa',
                'facebook': 'medispa.uz'
            },
            {
                'user': User.objects.get(username='elite_clinic'),
                'business_name': 'Elite Clinic',
                'description': 'Premium medical and cosmetic services.',
                'address': 'Yunusobod, 19',
                'city': 'Toshkent',
                'district': 'Yunusobod',
                'latitude': 41.334567,
                'longitude': 69.276543,
                'is_premium': True,
                'is_verified': True,
                'logo': 'business_logos/elite_clinic.png',
                'cover_image': 'business_covers/elite_clinic_cover.jpg',
                'website': 'https://eliteclinic.uz',
                'instagram': 'elite_clinic_uz',
                'telegram': '@elite_clinic',
                'facebook': 'eliteclinic.uz'
            },
            {
                'user': User.objects.get(username='nail_art'),
                'business_name': 'Nail Art Studio',
                'description': 'Professional nail care and design.',
                'address': 'Mirzo Ulug\'bek ko\'chasi, 56',
                'city': 'Toshkent',
                'district': 'Mirzo Ulug\'bek',
                'latitude': 41.321234,
                'longitude': 69.265432,
                'is_premium': False,
                'is_verified': True,
                'logo': 'business_logos/nail_art.png',
                'cover_image': 'business_covers/nail_art_cover.jpg',
                'website': 'https://nailart.uz',
                'instagram': 'nail_art_uz',
                'telegram': '@nail_art',
                'facebook': 'nailart.uz'
            },
            {
                'user': User.objects.get(username='barber_shop'),
                'business_name': 'Modern Barber Shop',
                'description': 'Modern barbershop for stylish men.',
                'address': 'Chilonzor, 78',
                'city': 'Toshkent',
                'district': 'Chilonzor',
                'latitude': 41.289876,
                'longitude': 69.243210,
                'is_premium': False,
                'is_verified': True,
                'logo': 'business_logos/barber_shop.png',
                'cover_image': 'business_covers/barber_shop_cover.jpg',
                'website': 'https://modernbarber.uz',
                'instagram': 'modern_barber_uz',
                'telegram': '@modern_barber',
                'facebook': 'modernbarber.uz'
            },
            {
                'user': User.objects.get(username='dental_clinic'),
                'business_name': 'Smile Dental Clinic',
                'description': 'Professional dental care for the whole family.',
                'address': 'Yakkasaroy, 34',
                'city': 'Toshkent',
                'district': 'Yakkasaroy',
                'latitude': 41.301234,
                'longitude': 69.256789,
                'is_premium': True,
                'is_verified': True,
                'logo': 'business_logos/dental_clinic.png',
                'cover_image': 'business_covers/dental_clinic_cover.jpg',
                'website': 'https://smileclinic.uz',
                'instagram': 'smile_clinic_uz',
                'telegram': '@smile_clinic',
                'facebook': 'smileclinic.uz'
            },
            {
                'user': User.objects.get(username='fitness_center'),
                'business_name': 'Power Fitness Center',
                'description': 'Modern fitness center with professional trainers.',
                'address': 'Sergeli, 12',
                'city': 'Toshkent',
                'district': 'Sergeli',
                'latitude': 41.278901,
                'longitude': 69.234567,
                'is_premium': False,
                'is_verified': True,
                'logo': 'business_logos/fitness_center.png',
                'cover_image': 'business_covers/fitness_center_cover.jpg',
                'website': 'https://powerfitness.uz',
                'instagram': 'power_fitness_uz',
                'telegram': '@power_fitness',
                'facebook': 'powerfitness.uz'
            },
            {
                'user': User.objects.get(username='spa_relax'),
                'business_name': 'Relax Spa Center',
                'description': 'Relaxation and wellness spa center.',
                'address': 'Bektemir, 45',
                'city': 'Toshkent',
                'district': 'Bektemir',
                'latitude': 41.267890,
                'longitude': 69.245678,
                'is_premium': False,
                'is_verified': True,
                'logo': 'business_logos/spa_relax.png',
                'cover_image': 'business_covers/spa_relax_cover.jpg',
                'website': 'https://relaxspa.uz',
                'instagram': 'relax_spa_uz',
                'telegram': '@relax_spa',
                'facebook': 'relaxspa.uz'
            },
        ]

        for data in business_data:
            business, created = BusinessProfile.objects.get_or_create(
                user=data['user'],
                defaults=data
            )

            if not created:
                for key, value in data.items():
                    if key != 'user':
                        setattr(business, key, value)
                business.save()

        self.stdout.write(f'Created {len(business_data)} businesses')

    def create_services(self):
        beauty_category = Category.objects.get(slug='beauty')
        health_category = Category.objects.get(slug='health')

        services_data = [
            # Beauty Zone services
            {
                'business': BusinessProfile.objects.get(business_name='Beauty Zone'),
                'category': beauty_category,
                'name': 'Soch kesish',
                'description': 'Professional soch kesish xizmati',
                'price': 50000,
                'duration': 45,
                'is_active': True,
                'image': 'service_images/haircut.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Beauty Zone'),
                'category': beauty_category,
                'name': 'Soch bo\'yash',
                'description': 'Sifatli bo\'yoqlar bilan soch bo\'yash',
                'price': 150000,
                'duration': 90,
                'is_active': True,
                'image': 'service_images/hair_coloring.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Beauty Zone'),
                'category': beauty_category,
                'name': 'Soch ukladka',
                'description': 'Professional soch ukladka xizmati',
                'price': 70000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/hair_styling.jpg'
            },

            # Health & Style services
            {
                'business': BusinessProfile.objects.get(business_name='Health & Style'),
                'category': beauty_category,
                'name': 'Manikür',
                'description': 'Professional manikür xizmati',
                'price': 70000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/manicure.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Health & Style'),
                'category': beauty_category,
                'name': 'Pedikür',
                'description': 'Professional pedikür xizmati',
                'price': 90000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/pedicure.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Health & Style'),
                'category': beauty_category,
                'name': 'Shellak',
                'description': 'Shellak qoplash xizmati',
                'price': 100000,
                'duration': 75,
                'is_active': True,
                'image': 'service_images/shellac.jpg'
            },

            # Glamour services
            {
                'business': BusinessProfile.objects.get(business_name='Glamour'),
                'category': beauty_category,
                'name': 'Make-up',
                'description': 'Professional make-up xizmati',
                'price': 120000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/makeup.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Glamour'),
                'category': beauty_category,
                'name': 'Qosh va kiprik',
                'description': 'Qosh va kiprik bo\'yash xizmati',
                'price': 80000,
                'duration': 45,
                'is_active': True,
                'image': 'service_images/brows_lashes.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Glamour'),
                'category': beauty_category,
                'name': 'Laminatsiya',
                'description': 'Qosh va kiprik laminatsiyasi',
                'price': 150000,
                'duration': 90,
                'is_active': True,
                'image': 'service_images/lamination.jpg'
            },

            # MediSpa services
            {
                'business': BusinessProfile.objects.get(business_name='MediSpa'),
                'category': health_category,
                'name': 'Massaj',
                'description': 'Relax massaj xizmati',
                'price': 150000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/massage.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='MediSpa'),
                'category': health_category,
                'name': 'Yuz tozalash',
                'description': 'Professional yuz tozalash xizmati',
                'price': 180000,
                'duration': 75,
                'is_active': True,
                'image': 'service_images/facial_cleaning.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='MediSpa'),
                'category': health_category,
                'name': 'Anti-age terapiya',
                'description': 'Yoshartiruvchi anti-age terapiya',
                'price': 250000,
                'duration': 90,
                'is_active': True,
                'image': 'service_images/anti_age.jpg'
            },

            # Elite Clinic services
            {
                'business': BusinessProfile.objects.get(business_name='Elite Clinic'),
                'category': health_category,
                'name': 'Kosmetologiya',
                'description': 'Professional kosmetologiya xizmati',
                'price': 200000,
                'duration': 90,
                'is_active': True,
                'image': 'service_images/cosmetology.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Elite Clinic'),
                'category': health_category,
                'name': 'Botoks',
                'description': 'Botoks in\'eksiyasi',
                'price': 300000,
                'duration': 45,
                'is_active': True,
                'image': 'service_images/botox.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Elite Clinic'),
                'category': health_category,
                'name': 'Mezoterapiya',
                'description': 'Yuz va soch uchun mezoterapiya',
                'price': 250000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/mesotherapy.jpg'
            },

            # Nail Art Studio services
            {
                'business': BusinessProfile.objects.get(business_name='Nail Art Studio'),
                'category': beauty_category,
                'name': 'Klassik manikür',
                'description': 'Klassik manikür xizmati',
                'price': 60000,
                'duration': 45,
                'is_active': True,
                'image': 'service_images/classic_manicure.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Nail Art Studio'),
                'category': beauty_category,
                'name': 'Nail art',
                'description': 'Tirnoq dizayni xizmati',
                'price': 100000,
                'duration': 90,
                'is_active': True,
                'image': 'service_images/nail_art.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Nail Art Studio'),
                'category': beauty_category,
                'name': 'Gel lak',
                'description': 'Gel lak qoplash xizmati',
                'price': 80000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/gel_polish.jpg'
            },

            # Modern Barber Shop services
            {
                'business': BusinessProfile.objects.get(business_name='Modern Barber Shop'),
                'category': beauty_category,
                'name': 'Erkaklar soch kesish',
                'description': 'Erkaklar uchun professional soch kesish',
                'price': 50000,
                'duration': 30,
                'is_active': True,
                'image': 'service_images/mens_haircut.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Modern Barber Shop'),
                'category': beauty_category,
                'name': 'Soqol olish',
                'description': 'Professional soqol olish xizmati',
                'price': 40000,
                'duration': 30,
                'is_active': True,
                'image': 'service_images/shaving.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Modern Barber Shop'),
                'category': beauty_category,
                'name': 'Soqol shakllantirish',
                'description': 'Soqolni shakllantirish xizmati',
                'price': 35000,
                'duration': 25,
                'is_active': True,
                'image': 'service_images/beard_styling.jpg'
            },

            # Smile Dental Clinic services
            {
                'business': BusinessProfile.objects.get(business_name='Smile Dental Clinic'),
                'category': health_category,
                'name': 'Tish tekshiruvi',
                'description': 'To\'liq tish tekshiruvi',
                'price': 100000,
                'duration': 45,
                'is_active': True,
                'image': 'service_images/dental_checkup.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Smile Dental Clinic'),
                'category': health_category,
                'name': 'Tish tozalash',
                'description': 'Professional tish tozalash xizmati',
                'price': 150000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/teeth_cleaning.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Smile Dental Clinic'),
                'category': health_category,
                'name': 'Tish plombalash',
                'description': 'Tish plombalash xizmati',
                'price': 200000,
                'duration': 75,
                'is_active': True,
                'image': 'service_images/dental_filling.jpg'
            },

            # Power Fitness Center services
            {
                'business': BusinessProfile.objects.get(business_name='Power Fitness Center'),
                'category': health_category,
                'name': 'Personal trening',
                'description': 'Shaxsiy trener bilan mashg\'ulot',
                'price': 120000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/personal_training.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Power Fitness Center'),
                'category': health_category,
                'name': 'Guruh mashg\'ulotlari',
                'description': 'Guruh bilan mashg\'ulotlar',
                'price': 80000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/group_fitness.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Power Fitness Center'),
                'category': health_category,
                'name': 'Yoga',
                'description': 'Yoga mashg\'ulotlari',
                'price': 90000,
                'duration': 75,
                'is_active': True,
                'image': 'service_images/yoga.jpg'
            },

            # Relax Spa Center services
            {
                'business': BusinessProfile.objects.get(business_name='Relax Spa Center'),
                'category': health_category,
                'name': 'Aroma terapiya',
                'description': 'Aroma terapiya massaji',
                'price': 180000,
                'duration': 90,
                'is_active': True,
                'image': 'service_images/aromatherapy.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Relax Spa Center'),
                'category': health_category,
                'name': 'Hammom',
                'description': 'Turk hammomi xizmati',
                'price': 150000,
                'duration': 60,
                'is_active': True,
                'image': 'service_images/turkish_bath.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Relax Spa Center'),
                'category': health_category,
                'name': 'Tosh terapiya',
                'description': 'Issiq toshlar bilan massaj',
                'price': 200000,
                'duration': 75,
                'is_active': True,
                'image': 'service_images/hot_stone_therapy.jpg'
            },
        ]

        for data in services_data:
            Service.objects.get_or_create(
                business=data['business'],
                name=data['name'],
                defaults=data
            )

        self.stdout.write(f'Created {len(services_data)} services')

    def create_business_hours(self):
        businesses = BusinessProfile.objects.all()

        for business in businesses:
            for day in range(7):
                # Monday to Friday: 9:00 - 18:00
                if day < 5:
                    BusinessHours.objects.get_or_create(
                        business=business,
                        day=day,
                        defaults={
                            'open_time': '09:00',
                            'close_time': '18:00',
                            'is_closed': False
                        }
                    )
                # Saturday: 10:00 - 16:00
                elif day == 5:
                    BusinessHours.objects.get_or_create(
                        business=business,
                        day=day,
                        defaults={
                            'open_time': '10:00',
                            'close_time': '16:00',
                            'is_closed': False
                        }
                    )
                # Sunday: Closed
                else:
                    BusinessHours.objects.get_or_create(
                        business=business,
                        day=day,
                        defaults={
                            'open_time': '00:00',
                            'close_time': '00:00',
                            'is_closed': True
                        }
                    )

        self.stdout.write(f'Created business hours for {businesses.count()} businesses')

    def create_reviews(self):
        businesses = BusinessProfile.objects.all()
        clients = User.objects.filter(user_type='client')

        reviews_data = []

        for business in businesses:
            for client in clients:
                # Not every client reviews every business
                if random.choice([True, False, False]):
                    reviews_data.append({
                        'business': business,
                        'user': client,
                        'rating': random.randint(3, 5),  # Mostly positive reviews
                        'comment': random.choice([
                            'Juda yaxshi xizmat ko\'rsatishdi!',
                            'Professional xizmat, tavsiya qilaman.',
                            'Yaxshi narx va sifat nisbati.',
                            'Xizmat sifati a\'lo darajada.',
                            'Yana qaytib kelaman, juda yoqdi.',
                            'Ajoyib xizmat, rahmat!',
                            'Xodimlar juda xushmuomala.',
                            'Toza va qulay joy.',
                            'Vaqtida xizmat ko\'rsatishdi.',
                            'Narxi sifatiga mos.'
                        ]),
                        'created_at': timezone.now() - timedelta(days=random.randint(1, 90))
                    })

        for data in reviews_data:
            Review.objects.get_or_create(
                business=data['business'],
                user=data['user'],
                defaults=data
            )

        self.stdout.write(f'Created {len(reviews_data)} reviews')

    def create_deals(self):
        businesses = BusinessProfile.objects.all()

        deals_data = [
            {
                'business': BusinessProfile.objects.get(business_name='Beauty Zone'),
                'title': 'Soch kesish va ukladka -30%',
                'description': 'Soch kesish va ukladka xizmatlariga maxsus chegirma',
                'discount_percentage': 30,
                'original_price': 150000,
                'discounted_price': 105000,
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=30)).date(),
                'is_active': True,
                'image': 'deal_images/haircut_deal.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Health & Style'),
                'title': 'Manikür + Pedikür -20%',
                'description': 'Manikür va pedikür xizmatlariga maxsus chegirma',
                'discount_percentage': 20,
                'original_price': 160000,
                'discounted_price': 128000,
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=15)).date(),
                'is_active': True,
                'image': 'deal_images/manicure_pedicure_deal.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='MediSpa'),
                'title': 'Massaj -15%',
                'description': 'Massaj xizmatiga maxsus chegirma',
                'discount_percentage': 15,
                'original_price': 150000,
                'discounted_price': 127500,
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=20)).date(),
                'is_active': True,
                'image': 'deal_images/massage_deal.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Glamour'),
                'title': 'Make-up -25%',
                'description': 'Make-up xizmatiga maxsus chegirma',
                'discount_percentage': 25,
                'original_price': 120000,
                'discounted_price': 90000,
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=10)).date(),
                'is_active': True,
                'image': 'deal_images/makeup_deal.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Elite Clinic'),
                'title': 'Botoks -10%',
                'description': 'Botoks xizmatiga maxsus chegirma',
                'discount_percentage': 10,
                'original_price': 300000,
                'discounted_price': 270000,
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=25)).date(),
                'is_active': True,
                'image': 'deal_images/botox_deal.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Nail Art Studio'),
                'title': 'Gel lak -20%',
                'description': 'Gel lak xizmatiga maxsus chegirma',
                'discount_percentage': 20,
                'original_price': 80000,
                'discounted_price': 64000,
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=15)).date(),
                'is_active': True,
                'image': 'deal_images/gel_polish_deal.jpg'
            },
            {
                'business': BusinessProfile.objects.get(business_name='Modern Barber Shop'),
                'title': 'Soch kesish + soqol -25%',
                'description': 'Soch kesish va soqol olish xizmatlariga maxsus chegirma',
                'discount_percentage': 25,
                'original_price': 90000,
                'discounted_price': 67500,
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=20)).date(),
                'is_active': True,
                'image': 'deal_images/haircut_shave_deal.jpg'
            },
        ]

        for data in deals_data:
            Deal.objects.get_or_create(
                business=data['business'],
                title=data['title'],
                defaults=data
            )

        self.stdout.write(f'Created {len(deals_data)} deals')

    def create_testimonials(self):
        testimonials_data = [
            {
                'name': 'Farida S.',
                'text': 'Juda qulay ilova. Navbatga yozilish oson, vaqtni tejaydi. Har doim o\'z vaqtida xizmat ko\'rsatiladi.',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'Lola Nurmatova',
                'text': 'Go\'zallik saloniga navbat olish uchun ajoyib ilova. Endi navbat kutib o\'tirmayman, oldindan band qilaman.',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'Akbarali D.',
                'text': 'Ajoyib xizmat! Endi men o\'z vaqtimni rejalashtira olaman va navbat kutib vaqtimni yo\'qotmayman. Juda qulay!',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'Gulnora M.',
                'text': 'Navbatim.uz orqali ko\'p vaqtimni tejadim. Endi men o\'zimga qulay vaqtda navbatga yozilaman.',
                'rating': 4,
                'is_active': True
            },
            {
                'name': 'Rustam Aliyev',
                'text': 'Soch olish uchun navbatga yozilish juda oson bo\'ldi. Ilova juda qulay va tushunishga oson.',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'Dilshod T.',
                'text': 'Biznesimiz uchun ajoyib platforma. Mijozlar bilan aloqa o\'rnatish va navbatlarni boshqarish juda oson.',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'Malika Yusupova',
                'text': 'Navbatim.uz orqali ko\'plab yangi salonlarni topdim. Endi men ularni osongina taqqoslay olaman va eng yaxshisini tanlashim mumkin.',
                'rating': 4,
                'is_active': True
            },
        ]

        for data in testimonials_data:
            Testimonial.objects.get_or_create(
                name=data['name'],
                text=data['text'],
                defaults=data
            )

        self.stdout.write(f'Created {len(testimonials_data)} testimonials')

    def create_appointments(self):
        services = Service.objects.all()
        clients = User.objects.filter(user_type='client')

        # Create past appointments
        past_appointments = []
        for _ in range(50):
            service = random.choice(services)
            client = random.choice(clients)

            # Random date in the past 30 days
            days_ago = random.randint(1, 30)
            appointment_date = timezone.now().date() - timedelta(days=days_ago)

            # Random time during business hours
            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])
            appointment_time = time(hour, minute)

            status = random.choice([
                "completed", "cancelled"
            ])

            past_appointments.append({
                'service': service,
                'client': client,
                'date': appointment_date,
                'time': appointment_time,
                'status': status,
                'notes': random.choice([
                    'Vaqtida keldi',
                    'Mijoz juda mamnun',
                    'Keyingi safar uchun tavsiyalar berildi',
                    '',
                    'Maxsus talablar mavjud',
                    'Allergiya bor'
                ]),
                'created_at': timezone.now() - timedelta(days=days_ago + random.randint(1, 10))
            })

        # Create future appointments
        future_appointments = []
        for _ in range(30):
            service = random.choice(services)
            client = random.choice(clients)

            # Random date in the next 14 days
            days_ahead = random.randint(1, 14)
            appointment_date = timezone.now().date() + timedelta(days=days_ahead)

            # Random time during business hours
            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])
            appointment_time = time(hour, minute)

            status = random.choice([
                "completed", "cancelled"
            ])

            future_appointments.append({
                'service': service,
                'client': client,
                'date': appointment_date,
                'time': appointment_time,
                'status': status,
                'notes': random.choice([
                    'Birinchi tashrif',
                    'Doimiy mijoz',
                    'Maxsus talablar mavjud',
                    '',
                    'Allergiya bor'
                ]),
                'created_at': timezone.now() - timedelta(days=random.randint(1, 5))
            })

        all_appointments = past_appointments + future_appointments

        for data in all_appointments:
            business = BusinessProfile.objects.order_by("?")[1]
            Appointment.objects.get_or_create(
                service=data['service'],
                business=business,
                client=data['client'],
                date=data['date'],
                time=data['time'],
                defaults=data
            )

        self.stdout.write(f'Created {len(all_appointments)} appointments')

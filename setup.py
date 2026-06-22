import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Configuration
PROJECT_NAME = 'ariran_project'
APP_NAME = 'studios'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_project():
    """Create Django project and app structure"""
    
    # Create directories
    directories = [
        PROJECT_NAME,
        f'{APP_NAME}/templates/{APP_NAME}',
        f'{APP_NAME}/static/{APP_NAME}/css',
        f'{APP_NAME}/static/{APP_NAME}/js',
        'static/images',
        'media/studios',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create manage.py
    manage_py = f'''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{PROJECT_NAME}.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
'''
    
    with open('manage.py', 'w', encoding='utf-8') as f:
        f.write(manage_py)
    
    # Create settings.py
    settings_py = f'''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '{APP_NAME}',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{PROJECT_NAME}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]]

WSGI_APPLICATION = '{PROJECT_NAME}.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = '{APP_NAME}.User'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'catalog'
LOGOUT_REDIRECT_URL = 'index'
'''
    
    os.makedirs(PROJECT_NAME, exist_ok=True)
    with open(f'{PROJECT_NAME}/settings.py', 'w', encoding='utf-8') as f:
        f.write(settings_py)
    
    # Create urls.py for project
    project_urls = f'''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{APP_NAME}.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
    
    with open(f'{PROJECT_NAME}/urls.py', 'w', encoding='utf-8') as f:
        f.write(project_urls)
    
    # Create wsgi.py
    wsgi_py = f'''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{PROJECT_NAME}.settings')
application = get_wsgi_application()
'''
    
    with open(f'{PROJECT_NAME}/wsgi.py', 'w', encoding='utf-8') as f:
        f.write(wsgi_py)
    
    # Create __init__.py files
    with open(f'{PROJECT_NAME}/__init__.py', 'w') as f:
        f.write('')
    
    with open(f'{APP_NAME}/__init__.py', 'w') as f:
        f.write('')
    
    print("✓ Django project structure created")

def create_models():
    """Create models.py"""
    
    models_py = '''from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    """Пользователь системы"""
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('admin', 'Администратор'),
        ('staff', 'Сотрудник'),
    )
    
    phone = models.CharField('Телефон', max_length=20)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='client')
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Studio(models.Model):
    """Студийное помещение"""
    TYPE_CHOICES = (
        ('minimal', 'Minimal'),
        ('cyclorama', 'Циклорама'),
        ('chroma', 'Хромакей'),
        ('thematic', 'Тематическая'),
        ('interior', 'Интерьерная'),
        ('podcast', 'Подкаст'),
    )
    
    INTERIOR_CHOICES = (
        ('white', 'Белый зал'),
        ('loft', 'Лофт'),
        ('classic', 'Классика'),
        ('modern', 'Модерн'),
        ('industrial', 'Индастриал'),
    )
    
    name = models.CharField('Название', max_length=255)
    type = models.CharField('Тип', max_length=255, choices=TYPE_CHOICES)
    interior = models.CharField('Интерьер', max_length=255, choices=INTERIOR_CHOICES, blank=True, null=True)
    description = models.TextField('Описание')
    price_per_hour = models.DecimalField('Цена за час', max_digits=10, decimal_places=2)
    area = models.DecimalField('Площадь (м²)', max_digits=6, decimal_places=2)
    capacity = models.IntegerField('Вместимость (чел)')
    ceiling_height = models.DecimalField('Высота потолков (м)', max_digits=4, decimal_places=2, default=3.0)
    is_available = models.BooleanField('Доступна', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def is_available_at_time(self, date, start_hour, end_hour):
        """Проверка доступности студии на конкретное время"""
        from django.db.models import Q
        
        start_time = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.strptime(f"{start_hour:02d}:00", "%H:%M").time()))
        end_time = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.strptime(f"{end_hour:02d}:00", "%H:%M").time()))
        
        conflicting_bookings = self.bookings.filter(
            status__in=['pending', 'confirmed'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        return not conflicting_bookings.exists()
    
    def get_available_dates(self, days_ahead=30):
        """Получить список доступных дат"""
        available_dates = []
        today = timezone.now().date()
        
        for i in range(days_ahead):
            date = today + timedelta(days=i)
            if self.is_date_available(date):
                available_dates.append(date)
        
        return available_dates
    
    def is_date_available(self, date):
        """Проверка доступности даты"""
        from django.db.models import Q
        
        day_start = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.strptime("10:00", "%H:%M").time()))
        day_end = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.strptime("22:00", "%H:%M").time()))
        
        bookings = self.bookings.filter(
            status__in=['pending', 'confirmed'],
            start_time__lt=day_end,
            end_time__gt=day_start
        )
        
        return not bookings.exists()

class StudioPhoto(models.Model):
    """Фотографии студий"""
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField('Фото', upload_to='studios/')
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Фотография студии'
        verbose_name_plural = 'Фотографии студий'
        ordering = ['order']
    
    def __str__(self):
        return f"Фото {self.studio.name}"

class Equipment(models.Model):
    """Оборудование"""
    CATEGORY_CHOICES = (
        ('light', 'Свет'),
        ('props', 'Реквизит'),
        ('stands', 'Стойки'),
        ('camera', 'Камеры'),
        ('other', 'Другое'),
    )
    
    name = models.CharField('Название', max_length=255)
    category = models.CharField('Категория', max_length=255, choices=CATEGORY_CHOICES)
    description = models.TextField('Описание', blank=True)
    is_available = models.BooleanField('Доступно', default=True)
    
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    """Бронирование"""
    STATUS_CHOICES = (
        ('pending', 'На проверке'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField('Начало')
    end_time = models.DateTimeField('Окончание')
    equipment = models.ManyToManyField(Equipment, blank=True, related_name='bookings')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField('Причина отклонения', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.studio.name} - {self.start_time}"

class Review(models.Model):
    """Отзывы"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=[(i, i) for i in range(1, 6)])
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв на {self.studio.name}"
'''
    
    with open(f'{APP_NAME}/models.py', 'w', encoding='utf-8') as f:
        f.write(models_py)
    
    print("✓ Models created")

def create_views():
    """Create views.py"""
    
    views_py = '''from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, timedelta
from .models import User, Studio, StudioPhoto, Equipment, Booking, Review
from .forms import UserRegistrationForm, BookingForm
import json

def index(request):
    """Главная страница"""
    popular_studios = Studio.objects.filter(is_available=True).prefetch_related('photos')[:5]
    return render(request, 'studios/index.html', {'popular_studios': popular_studios})

def catalog(request):
    """Каталог студий с фильтрацией"""
    studios = Studio.objects.filter(is_available=True).prefetch_related('photos')
    
    # Получаем параметры фильтрации
    studio_type = request.GET.get('type')
    interior = request.GET.get('interior')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    duration = request.GET.get('duration', '1')
    
    # Фильтрация по типу
    if studio_type:
        studios = studios.filter(type=studio_type)
    
    # Фильтрация по интерьеру
    if interior:
        studios = studios.filter(interior=interior)
    
    # Фильтрация по цене
    if min_price:
        studios = studios.filter(price_per_hour__gte=min_price)
    if max_price:
        studios = studios.filter(price_per_hour__lte=max_price)
    
    # Фильтрация по дате и времени
    if date_str and time_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_hour = int(time_str.split(':')[0])
            duration_hours = int(duration)
            end_hour = start_hour + duration_hours
            
            available_studios = []
            for studio in studios:
                if studio.is_available_at_time(filter_date, start_hour, end_hour):
                    available_studios.append(studio.id)
            studios = studios.filter(id__in=available_studios)
        except (ValueError, TypeError):
            pass
    
    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        studios = studios.order_by('price_per_hour')
    elif sort_by == 'price_desc':
        studios = studios.order_by('-price_per_hour')
    elif sort_by == 'availability':
        # Сортировка по доступности
        studios = studios.order_by('-is_available', 'name')
    else:
        studios = studios.order_by('name')
    
    # Пагинация (показываем первые 12)
    page = int(request.GET.get('page', 1))
    per_page = 12
    total_count = studios.count()
    studios_page = studios[(page-1)*per_page:page*per_page]
    
    context = {
        'studios': studios_page,
        'types': Studio.TYPE_CHOICES,
        'interiors': Studio.INTERIOR_CHOICES,
        'equipment_list': Equipment.objects.filter(is_available=True),
        'has_more': total_count > page * per_page,
        'current_page': page,
    }
    
    if request.htmx:
        return render(request, 'studios/partials/studio_grid.html', context)
    
    return render(request, 'studios/catalog.html', context)

def studio_detail(request, pk):
    """Детальная страница студии"""
    studio = get_object_or_404(Studio, pk=pk)
    photos = studio.photos.all()
    equipment = Equipment.objects.filter(is_available=True)
    reviews = studio.reviews.select_related('user').all()
    
    context = {
        'studio': studio,
        'photos': photos,
        'equipment': equipment,
        'reviews': reviews,
    }
    return render(request, 'studios/studio_detail.html', context)

@require_http_methods(["GET"])
def check_availability(request):
    """Проверка доступности студии"""
    studio_id = request.GET.get('studio_id')
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    duration = int(request.GET.get('duration', 1))
    
    try:
        studio = Studio.objects.get(id=studio_id)
        filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_hour = int(time_str.split(':')[0])
        end_hour = start_hour + duration
        
        is_available = studio.is_available_at_time(filter_date, start_hour, end_hour)
        
        return JsonResponse({'available': is_available})
    except Exception as e:
        return JsonResponse({'available': False, 'error': str(e)})

@require_http_methods(["GET"])
def get_available_times(request):
    """Получение доступных временных слотов"""
    studio_id = request.GET.get('studio_id')
    date_str = request.GET.get('date')
    
    try:
        studio = Studio.objects.get(id=studio_id)
        filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        available_times = []
        for hour in range(10, 22):  # С 10:00 до 22:00
            if studio.is_available_at_time(filter_date, hour, hour + 1):
                available_times.append(f"{hour:02d}:00")
        
        return JsonResponse({'times': available_times})
    except Exception as e:
        return JsonResponse({'times': [], 'error': str(e)})

@login_required
@require_http_methods(["POST"])
def create_booking(request):
    """Создание бронирования"""
    try:
        data = json.loads(request.body)
        studio = Studio.objects.get(id=data['studio_id'])
        
        start_datetime = timezone.make_aware(datetime.strptime(data['start_datetime'], '%Y-%m-%d %H:%M'))
        end_datetime = timezone.make_aware(datetime.strptime(data['end_datetime'], '%Y-%m-%d %H:%M'))
        
        # Проверка доступности
        if not studio.is_available_at_time(start_datetime.date(), start_datetime.hour, end_datetime.hour):
            return JsonResponse({'success': False, 'error': 'Студия уже забронирована на это время'})
        
        booking = Booking.objects.create(
            user=request.user,
            studio=studio,
            start_time=start_datetime,
            end_time=end_datetime,
        )
        
        # Добавляем оборудование
        if 'equipment_ids' in data:
            equipment = Equipment.objects.filter(id__in=data['equipment_ids'])
            booking.equipment.set(equipment)
        
        return JsonResponse({'success': True, 'booking_id': booking.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('catalog')
    
    return render(request, 'studios/login.html')

def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')

def user_register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'studios/register.html', {'form': form})

@login_required
def user_profile(request):
    """Личный кабинет пользователя"""
    bookings = request.user.bookings.select_related('studio').order_by('-start_time')
    return render(request, 'studios/profile.html', {'bookings': bookings})
'''
    
    with open(f'{APP_NAME}/views.py', 'w', encoding='utf-8') as f:
        f.write(views_py)
    
    print("✓ Views created")

def create_forms():
    """Create forms.py"""
    
    forms_py = '''from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking

class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    phone = forms.CharField(label='Телефон', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    """Форма бронирования"""
    class Meta:
        model = Booking
        fields = ['studio', 'start_time', 'end_time', 'equipment']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
'''
    
    with open(f'{APP_NAME}/forms.py', 'w', encoding='utf-8') as f:
        f.write(forms_py)
    
    print("✓ Forms created")

def create_urls():
    """Create urls.py for app"""
    
    urls_py = '''from django.urls import path
from . import views

app_name = 'studios'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('studio/<int:pk>/', views.studio_detail, name='studio_detail'),
    path('api/check-availability/', views.check_availability, name='check_availability'),
    path('api/get-available-times/', views.get_available_times, name='get_available_times'),
    path('api/create-booking/', views.create_booking, name='create_booking'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),
]
'''
    
    with open(f'{APP_NAME}/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_py)
    
    print("✓ URLs created")

def create_admin():
    """Create admin.py"""
    
    admin_py = '''from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Studio, StudioPhoto, Equipment, Booking, Review

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone', 'role')}),
    )

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'interior', 'price_per_hour', 'area', 'capacity', 'is_available')
    list_filter = ('type', 'interior', 'is_available')
    search_fields = ('name', 'description')
    ordering = ['name']

@admin.register(StudioPhoto)
class StudioPhotoAdmin(admin.ModelAdmin):
    list_display = ('studio', 'order', 'image')
    list_filter = ('studio',)
    ordering = ['studio', 'order']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('studio', 'user', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'start_time')
    date_hierarchy = 'start_time'
    ordering = ['-start_time']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('studio', 'user')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('studio', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    ordering = ['-created_at']
'''
    
    with open(f'{APP_NAME}/admin.py', 'w', encoding='utf-8') as f:
        f.write(admin_py)
    
    print("✓ Admin created")

def create_templates():
    """Create HTML templates"""
    
    # Base template
    base_html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}АРИРАН — Креативный комплекс студийных помещений{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'studios/css/style.css' %}">
    <script src="https://unpkg.com/htmx.org@1.9.10" integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5xLSi8nO7UC" crossorigin="anonymous"></script>
</head>
<body>
    <!-- Sticky Navigation -->
    <div class="sticky-nav" id="stickyNav">
        <nav class="nav">
            <a href="{% url 'studios:index' %}">Главная</a>
            <a href="{% url 'studios:catalog' %}">Каталог</a>
            <a href="#block2">О нас</a>
            <a href="#block7">FAQ</a>
            <a href="#block6">Контакты</a>
            {% if user.is_authenticated %}
            <a href="{% url 'studios:profile' %}">Личный кабинет</a>
            <a href="{% url 'studios:logout' %}">Выход</a>
            {% else %}
            <a href="{% url 'studios:login' %}">Вход</a>
            {% endif %}
        </nav>
    </div>

    {% block content %}{% endblock %}

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-top">
                <div class="footer-logo">АРИРАН</div>
                <nav class="footer-nav">
                    <a href="{% url 'studios:index' %}">Главная</a>
                    <a href="{% url 'studios:catalog' %}">Каталог</a>
                    <a href="#block2">О нас</a>
                    <a href="#block7">FAQ</a>
                    <a href="#block6">Контакты</a>
                </nav>
                <div class="footer-contacts">
                    <a href="tel:+79001234567" class="phone">+7 (900) 123-45-67</a>
                    <a href="mailto:info@ariran.ru" class="email">info@ariran.ru</a>
                    <div class="address">ул. Мира 10, Волгоград<br>400066</div>
                </div>
            </div>
            <div class="footer-middle">
                <div class="footer-social">
                    <a href="#" class="social-link" aria-label="Telegram">
                        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                    </a>
                    <a href="#" class="social-link" aria-label="VK">
                        <svg viewBox="0 0 24 24"><path d="M12.785 16.241s.288-.032.436-.194c.136-.148.132-.427.132-.427s-.02-1.304.587-1.496c.598-.189 1.366 1.26 2.18 1.817.615.42 1.083.328 1.083.328l2.177-.03s1.14-.07.599-.964c-.044-.073-.314-.661-1.617-1.869-1.364-1.264-1.182-1.059.462-3.246.999-1.332 1.398-2.146 1.273-2.494-.12-.332-.856-.244-.856-.244l-2.45.015s-.182-.025-.317.056c-.131.079-.216.263-.216.263s-.387 1.028-.903 1.903c-1.089 1.848-1.524 1.946-1.703 1.832-.414-.266-.31-1.07-.31-1.64 0-1.783.27-2.52-.527-2.713-.265-.064-.46-.106-1.138-.113-.87-.009-1.608.003-2.024.207-.277.136-.49.44-.36.457.16.021.522.098.714.361.248.34.24 1.103.24 1.103s.142 2.096-.332 2.353c-.326.178-.774-.185-1.738-1.847-.493-.851-.864-1.79-.864-1.79s-.072-.176-.2-.271c-.155-.115-.372-.151-.372-.151l-2.327.015s-.35.01-.478.162c-.114.135-.009.413-.009.413s1.817 4.244 3.874 6.383c1.887 1.963 4.029 1.834 4.029 1.834h.971z"/></svg>
                    </a>
                </div>
                <div class="footer-schedule">
                    Рабочие часы: <span class="time">10:00 — 22:00</span>
                </div>
            </div>
            <div class="footer-bottom">
                <div class="footer-copy">© 2025 Ариран. Все права защищены.</div>
                <div class="footer-legal">
                    <a href="#">Политика конфиденциальности</a>
                    <a href="#">Пользовательское соглашение</a>
                </div>
            </div>
        </div>
    </footer>

    <script src="{% static 'studios/js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''
    
    os.makedirs(f'{APP_NAME}/templates/{APP_NAME}', exist_ok=True)
    with open(f'{APP_NAME}/templates/{APP_NAME}/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    
    # Catalog template
    catalog_html = '''{% extends "studios/base.html" %}
{% load static %}

{% block content %}
<section class="catalog-page">
    <div class="container">
        <!-- Filters -->
        <div class="filters-section fade-in">
            <form method="get" class="filters-grid" id="filterForm" hx-get="{% url 'studios:catalog' %}" hx-target="#studiosContainer" hx-trigger="change" hx-swap="outerHTML">
                <div class="filter-group">
                    <label>Категория</label>
                    <select name="type" onchange="this.form.submit()">
                        <option value="">Выберите категорию</option>
                        {% for value, label in types %}
                        <option value="{{ value }}" {% if request.GET.type == value %}selected{% endif %}>{{ label }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label>Интерьер</label>
                    <select name="interior" onchange="this.form.submit()">
                        <option value="">Выберите интерьер</option>
                        {% for value, label in interiors %}
                        <option value="{{ value }}" {% if request.GET.interior == value %}selected{% endif %}>{{ label }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label>Цена от (₽/час)</label>
                    <input type="number" name="min_price" placeholder="Минимальная цена" value="{{ request.GET.min_price }}" onchange="this.form.submit()">
                </div>
                
                <div class="filter-group">
                    <label>Цена до (₽/час)</label>
                    <input type="number" name="max_price" placeholder="Максимальная цена" value="{{ request.GET.max_price }}" onchange="this.form.submit()">
                </div>
                
                <div class="filter-group">
                    <label>Дата</label>
                    <input type="date" name="date" id="dateFilter" value="{{ request.GET.date }}" min="{% now 'Y-m-d' %}" onchange="this.form.submit()">
                </div>
                
                <div class="filter-group">
                    <label>Время</label>
                    <select name="time" id="timeFilter" onchange="this.form.submit()">
                        <option value="">Выберите время</option>
                        {% for hour in "10,11,12,13,14,15,16,17,18,19,20,21"|split:"," %}
                        <option value="{{ hour }}:00" {% if request.GET.time == hour|add:":00" %}selected{% endif %}>{{ hour }}:00</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="filter-buttons">
                    <button type="button" class="btn btn-secondary" onclick="resetFilters()">Сбросить</button>
                </div>
            </form>
        </div>
        
        <!-- Studios Grid -->
        <div id="studiosContainer">
            {% include "studios/partials/studio_grid.html" %}
        </div>
    </div>
</section>

<script>
function resetFilters() {
    window.location.href = "{% url 'studios:catalog' %}";
}
</script>
{% endblock %}
'''
    
    with open(f'{APP_NAME}/templates/{APP_NAME}/catalog.html', 'w', encoding='utf-8') as f:
        f.write(catalog_html)
    
    # Studio grid partial
    os.makedirs(f'{APP_NAME}/templates/{APP_NAME}/partials', exist_ok=True)
    
    studio_grid_html = '''{% load static %}
<div class="studios-header">
    <div class="studios-count">Найдено: {{ studios.count }} студий</div>
    <select class="sort-select" onchange="location = this.value;">
        <option value="?{% if request.GET.type %}type={{ request.GET.type }}&{% endif %}{% if request.GET.date %}date={{ request.GET.date }}&{% endif %}sort=name" {% if request.GET.sort == 'name' or not request.GET.sort %}selected{% endif %}>Сортировать по: названию</option>
        <option value="?{% if request.GET.type %}type={{ request.GET.type }}&{% endif %}{% if request.GET.date %}date={{ request.GET.date }}&{% endif %}sort=price_asc" {% if request.GET.sort == 'price_asc' %}selected{% endif %}>Сортировать по: цене (возрастание)</option>
        <option value="?{% if request.GET.type %}type={{ request.GET.type }}&{% endif %}{% if request.GET.date %}date={{ request.GET.date }}&{% endif %}sort=price_desc" {% if request.GET.sort == 'price_desc' %}selected{% endif %}>Сортировать по: цене (убывание)</option>
    </select>
</div>

<div class="studios-grid">
    {% for studio in studios %}
    <div class="studio-card fade-in">
        {% if studio.photos.first %}
        <img src="{{ studio.photos.first.image.url }}" alt="{{ studio.name }}" class="studio-image">
        {% else %}
        <img src="{% static 'images/empty-image.png' %}" alt="{{ studio.name }}" class="studio-image">
        {% endif %}
        
        <div class="studio-info">
            <h3 class="studio-name">{{ studio.name }}</h3>
            <p class="studio-type">{{ studio.get_type_display }}</p>
            {% if studio.interior %}
            <p class="studio-interior">{{ studio.get_interior_display }}</p>
            {% endif %}
            
            <div class="studio-params">
                <div class="studio-param">
                    <span>📐</span>
                    <span>{{ studio.area }} м²</span>
                </div>
                <div class="studio-param">
                    <span>⬆</span>
                    <span>{{ studio.ceiling_height }} м</span>
                </div>
                <div class="studio-param">
                    <span>👥</span>
                    <span>{{ studio.capacity }} чел</span>
                </div>
            </div>
            
            <div class="studio-price">от {{ studio.price_per_hour }}₽/час</div>
            
            <a href="{% url 'studios:studio_detail' studio.pk %}" class="btn btn-book">Забронировать</a>
        </div>
    </div>
    {% empty %}
    <div class="no-results">
        <p>Студии не найдены</p>
        <p>Попробуйте изменить параметры фильтрации</p>
    </div>
    {% endfor %}
</div>

{% if has_more %}
<div class="load-more">
    <button class="btn btn-load-more" hx-get="{% url 'studios:catalog' %}?page={{ current_page|add:1 }}{% if request.GET.type %}&type={{ request.GET.type }}{% endif %}{% if request.GET.date %}&date={{ request.GET.date }}{% endif %}" hx-target="#studiosContainer" hx-swap="beforeend" hx-indicator=".load-more">
        Показать ещё
    </button>
</div>
{% endif %}
'''
    
    with open(f'{APP_NAME}/templates/{APP_NAME}/partials/studio_grid.html', 'w', encoding='utf-8') as f:
        f.write(studio_grid_html)
    
    print("✓ Templates created")

def create_css():
    """Create CSS file"""
    
    css_content = '''/* Base styles from index.html */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Helvetica', 'Helvetica Neue', Arial, sans-serif;
    overflow-x: hidden;
    background: #f5f5f5;
}

.container {
    max-width: 1744px;
    margin: 0 auto;
    padding: 0 88px;
}

/* Sticky Navigation */
.sticky-nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
    padding: 16px 88px;
    display: flex;
    justify-content: center;
    transform: translateY(-100%);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), background 0.4s ease;
    background: transparent;
}

.sticky-nav.visible {
    transform: translateY(0);
    background: #788BFF;
}

.sticky-nav .nav {
    display: flex;
    align-items: center;
    gap: 0;
    background: transparent;
    backdrop-filter: none;
    border: none;
    padding: 10px 28px;
}

.sticky-nav .nav a {
    color: #fff;
    font-size: 20px;
    font-weight: bold;
    margin: 0 16px;
    transition: opacity 0.3s;
}

.sticky-nav .nav a:hover {
    opacity: 0.7;
}

/* Filters */
.filters-section {
    background: #fff;
    padding: 30px 0;
    margin-bottom: 30px;
    margin-top: 80px;
}

.filters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.filter-group {
    display: flex;
    flex-direction: column;
}

.filter-group label {
    font-size: 14px;
    color: #666;
    margin-bottom: 8px;
}

.filter-group select,
.filter-group input {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    font-family: 'Helvetica', sans-serif;
}

.filter-buttons {
    display: flex;
    gap: 12px;
    margin-top: 20px;
}

.btn {
    padding: 12px 32px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s;
    text-decoration: none;
    display: inline-block;
}

.btn-primary {
    background: #788BFF;
    color: #fff;
}

.btn-primary:hover {
    background: #5a74f5;
}

.btn-secondary {
    background: #f0f0f0;
    color: #1a1a1a;
}

.btn-secondary:hover {
    background: #e0e0e0;
}

/* Studios Grid */
.studios-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding: 20px 0;
}

.studios-count {
    font-size: 18px;
    color: #666;
}

.sort-select {
    padding: 8px 16px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-family: 'Helvetica', sans-serif;
}

.studios-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
}

.studio-card {
    background: #fff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.studio-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.studio-image {
    width: 100%;
    height: 280px;
    object-fit: cover;
}

.studio-info {
    padding: 20px;
}

.studio-name {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 8px;
}

.studio-type {
    font-size: 16px;
    color: #666;
    margin-bottom: 8px;
}

.studio-interior {
    font-size: 14px;
    color: #999;
    margin-bottom: 16px;
}

.studio-params {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
    font-size: 14px;
    color: #666;
}

.studio-param {
    display: flex;
    align-items: center;
    gap: 4px;
}

.studio-price {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 16px;
}

.btn-book {
    width: 100%;
    padding: 14px;
    background: #788BFF;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s;
    text-align: center;
}

.btn-book:hover {
    background: #5a74f5;
}

.load-more {
    text-align: center;
    margin: 40px 0;
}

.btn-load-more {
    padding: 16px 48px;
    background: #788BFF;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}

.no-results {
    grid-column: 1 / -1;
    text-align: center;
    padding: 60px;
    background: #fff;
    border-radius: 16px;
}

/* Animations */
.fade-in {
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}

/* Footer */
.footer {
    width: 100%;
    background: #1a1a1a;
    padding: 80px 0 40px;
    margin-top: 80px;
}

.footer-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 60px;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}

.footer-logo {
    font-size: 40px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 3px;
}

.footer-nav {
    display: flex;
    gap: 40px;
}

.footer-nav a {
    color: #fff;
    font-size: 20px;
    font-weight: 400;
    transition: color 0.3s ease;
}

.footer-nav a:hover {
    color: #788BFF;
}

.footer-contacts {
    display: flex;
    flex-direction: column;
    gap: 16px;
    text-align: right;
}

.footer-contacts .phone {
    font-size: 24px;
    font-weight: 300;
    color: #fff;
    transition: color 0.3s ease;
}

.footer-contacts .phone:hover {
    color: #788BFF;
}

.footer-contacts .email {
    font-size: 20px;
    font-weight: 300;
    color: rgba(255,255,255,0.7);
    transition: color 0.3s ease;
}

.footer-contacts .email:hover {
    color: #788BFF;
}

.footer-contacts .address {
    font-size: 18px;
    font-weight: 300;
    color: rgba(255,255,255,0.5);
    line-height: 1.4;
}

.footer-middle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 40px 0;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}

.footer-social {
    display: flex;
    gap: 20px;
}

.social-link {
    width: 48px;
    height: 48px;
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.social-link:hover {
    border-color: #788BFF;
    background: rgba(120, 139, 255, 0.1);
}

.social-link svg {
    width: 20px;
    height: 20px;
    fill: #fff;
    transition: fill 0.3s ease;
}

.social-link:hover svg {
    fill: #788BFF;
}

.footer-schedule {
    font-size: 18px;
    font-weight: 300;
    color: rgba(255,255,255,0.6);
}

.footer-schedule .time {
    color: #fff;
    font-size: 20px;
}

.footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px;
}

.footer-copy {
    font-size: 16px;
    font-weight: 300;
    color: rgba(255,255,255,0.4);
}

.footer-legal {
    display: flex;
    gap: 30px;
}

.footer-legal a {
    font-size: 16px;
    font-weight: 300;
    color: rgba(255,255,255,0.4);
    transition: color 0.3s ease;
}

.footer-legal a:hover {
    color: #788BFF;
}
'''
    
    os.makedirs(f'{APP_NAME}/static/{APP_NAME}/css', exist_ok=True)
    with open(f'{APP_NAME}/static/{APP_NAME}/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✓ CSS created")

def create_js():
    """Create JavaScript file"""
    
    js_content = '''// Sticky Navigation
const stickyNav = document.getElementById('stickyNav');
const hero = document.getElementById('hero');

if (stickyNav && hero) {
    window.addEventListener('scroll', () => {
        const heroBottom = hero.offsetTop + hero.offsetHeight;
        if (window.scrollY > heroBottom - 100) {
            stickyNav.classList.add('visible');
        } else {
            stickyNav.classList.remove('visible');
        }
    });
}

// Fade-in animation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// Date filter - only show available dates
const dateFilter = document.getElementById('dateFilter');
if (dateFilter) {
    const today = new Date();
    const maxDate = new Date();
    maxDate.setDate(today.getDate() + 30);
    
    dateFilter.min = today.toISOString().split('T')[0];
    dateFilter.max = maxDate.toISOString().split('T')[0];
}

// Time filter - update based on date selection
const timeFilter = document.getElementById('timeFilter');
if (timeFilter && dateFilter) {
    dateFilter.addEventListener('change', async () => {
        const date = dateFilter.value;
        if (date) {
            // Here you would fetch available times from the server
            // For now, just keep all times 10:00-22:00
        }
    });
}

// HTMX event handlers
document.body.addEventListener('htmx:afterSwap', (event) => {
    // Re-initialize animations after HTMX swap
    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
});

console.log('Arirang Studio Management System loaded');
'''
    
    os.makedirs(f'{APP_NAME}/static/{APP_NAME}/js', exist_ok=True)
    with open(f'{APP_NAME}/static/{APP_NAME}/js/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("✓ JavaScript created")

def run_migrations():
    """Run Django migrations"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')
    django.setup()
    
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✓ Migrations completed")

def create_superuser():
    """Create admin user"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@ariran.ru',
            password='admin',
            phone='+7 (999) 999-99-99',
            role='admin'
        )
        print("✓ Superuser created (username: admin, password: admin)")
    else:
        print("✓ Superuser already exists")

def create_sample_data():
    """Create sample studios and equipment"""
    from .studios.models import Studio, Equipment
    
    # Create sample studios
    if not Studio.objects.exists():
        studios_data = [
            {
                'name': 'Зал "Циклорама 01"',
                'type': 'cyclorama',
                'interior': 'white',
                'description': 'Просторная студия с циклорамой',
                'price_per_hour': 2000,
                'area': 45.0,
                'capacity': 10,
                'ceiling_height': 3.0,
            },
            {
                'name': 'Зал "Интерьер 01"',
                'type': 'interior',
                'interior': 'loft',
                'description': 'Стильный лофт интерьер',
                'price_per_hour': 2500,
                'area': 60.0,
                'capacity': 15,
                'ceiling_height': 3.5,
            },
            {
                'name': 'Зал "Подкаст 01"',
                'type': 'podcast',
                'interior': 'modern',
                'description': 'Студия для записи подкастов',
                'price_per_hour': 1500,
                'area': 30.0,
                'capacity': 6,
                'ceiling_height': 2.8,
            },
        ]
        
        for studio_data in studios_data:
            Studio.objects.create(**studio_data)
        
        print("✓ Sample studios created")
    
    # Create sample equipment
    if not Equipment.objects.exists():
        equipment_data = [
            {'name': 'Импульсный свет Godox', 'category': 'light'},
            {'name': 'Постоянный свет Aputure', 'category': 'light'},
            {'name': 'Стойка для света', 'category': 'stands'},
            {'name': 'Фон белый', 'category': 'props'},
            {'name': 'Отражатель 5в1', 'category': 'props'},
        ]
        
        for equip_data in equipment_data:
            Equipment.objects.create(**equip_data)
        
        print("✓ Sample equipment created")

def main():
    """Main function to setup the project"""
    print("🚀 Creating Arirang Studio Management System...")
    print()
    
    # Create project structure
    create_project()
    
    # Create app files
    create_models()
    create_views()
    create_forms()
    create_urls()
    create_admin()
    create_templates()
    create_css()
    create_js()
    
    print()
    print("📦 Installing dependencies...")
    os.system('pip install django pillow')
    
    print()
    print("🗄️  Running migrations...")
    run_migrations()
    
    print()
    print("👤 Creating superuser...")
    create_superuser()
    
    print()
    print("📝 Creating sample data...")
    from studios import models
    create_sample_data()
    
    print()
    print("=" * 60)
    print("✅ Project setup completed successfully!")
    print("=" * 60)
    print()
    print("To start the development server, run:")
    print("  python manage.py runserver")
    print()
    print("Admin panel:")
    print("  http://127.0.0.1:8000/admin/")
    print("  Username: admin")
    print("  Password: admin")
    print()
    print("Main site:")
    print("  http://127.0.0.1:8000/")
    print()
    print("Catalog:")
    print("  http://127.0.0.1:8000/catalog/")
    print()

if __name__ == '__main__':
    main()
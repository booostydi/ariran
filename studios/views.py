import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import datetime, timedelta
from .decorators import admin_required
from .models import (
    User, Category, Interior, EquipmentCategory,
    Studio, StudioPhoto, Equipment, Booking, Favorite
)




from .forms import UserRegistrationForm, UserLoginForm, BookingForm, StudioForm, CategoryForm, InteriorForm, EquipmentCategoryForm, EquipmentForm

# ===== СТУДИИ =====
@admin_required
def admin_studio_add(request):
    if request.method == 'POST':
        form = StudioForm(request.POST)
        if form.is_valid():
            studio = form.save()
            # Сохраняем фото
            for f in request.FILES.getlist('photos'):
                StudioPhoto.objects.create(studio=studio, image=f, order=0)
            return redirect('/admin-panel/?tab=studios')
    else:
        form = StudioForm()
    return render(request, 'studios/admin_studio_form.html', {'form': form, 'title': 'Добавить студию'})


@admin_required
def admin_studio_edit(request, studio_id):
    studio = get_object_or_404(Studio, pk=studio_id)
    if request.method == 'POST':
        form = StudioForm(request.POST, instance=studio)
        if form.is_valid():
            form.save()
            # Новые фото
            for f in request.FILES.getlist('photos'):
                StudioPhoto.objects.create(studio=studio, image=f, order=0)
            # Удаление фото
            delete_photo_ids = request.POST.getlist('delete_photos')
            if delete_photo_ids:
                StudioPhoto.objects.filter(id__in=delete_photo_ids, studio=studio).delete()
            return redirect('/admin-panel/?tab=studios')
    else:
        form = StudioForm(instance=studio)
    photos = studio.photos.all()
    return render(request, 'studios/admin_studio_form.html', {'form': form, 'title': 'Редактировать студию', 'studio': studio, 'photos': photos})


# ===== КАТЕГОРИИ =====
@admin_required
def admin_categories(request):
    items = Category.objects.all()
    return render(request, 'studios/admin_simple_list.html', {
        'title': 'Категории', 'items': items, 'add_url': 'studios:admin_category_add',
        'edit_url': 'studios:admin_category_edit', 'delete_url': 'studios:admin_category_delete',
    })

@admin_required
def admin_category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_categories')
    else:
        form = CategoryForm()
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Добавить категорию', 'back_url': 'studios:admin_categories'})

@admin_required
def admin_category_edit(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_categories')
    else:
        form = CategoryForm(instance=obj)
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Редактировать категорию', 'back_url': 'studios:admin_categories'})

@admin_required
def admin_category_delete(request, pk):
    get_object_or_404(Category, pk=pk).delete()
    return redirect('studios:admin_categories')


# ===== ИНТЕРЬЕРЫ =====
@admin_required
def admin_interiors(request):
    items = Interior.objects.all()
    return render(request, 'studios/admin_simple_list.html', {
        'title': 'Интерьеры', 'items': items, 'add_url': 'studios:admin_interior_add',
        'edit_url': 'studios:admin_interior_edit', 'delete_url': 'studios:admin_interior_delete',
    })

@admin_required
def admin_interior_add(request):
    if request.method == 'POST':
        form = InteriorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_interiors')
    else:
        form = InteriorForm()
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Добавить интерьер', 'back_url': 'studios:admin_interiors'})

@admin_required
def admin_interior_edit(request, pk):
    obj = get_object_or_404(Interior, pk=pk)
    if request.method == 'POST':
        form = InteriorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_interiors')
    else:
        form = InteriorForm(instance=obj)
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Редактировать интерьер', 'back_url': 'studios:admin_interiors'})

@admin_required
def admin_interior_delete(request, pk):
    get_object_or_404(Interior, pk=pk).delete()
    return redirect('studios:admin_interiors')


# ===== КАТЕГОРИИ ОБОРУДОВАНИЯ =====
@admin_required
def admin_equipment_categories(request):
    items = EquipmentCategory.objects.all()
    return render(request, 'studios/admin_simple_list.html', {
        'title': 'Категории оборудования', 'items': items,
        'add_url': 'studios:admin_equipment_category_add',
        'edit_url': 'studios:admin_equipment_category_edit',
        'delete_url': 'studios:admin_equipment_category_delete',
    })

@admin_required
def admin_equipment_category_add(request):
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_equipment_categories')
    else:
        form = EquipmentCategoryForm()
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Добавить категорию оборудования', 'back_url': 'studios:admin_equipment_categories'})

@admin_required
def admin_equipment_category_edit(request, pk):
    obj = get_object_or_404(EquipmentCategory, pk=pk)
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_equipment_categories')
    else:
        form = EquipmentCategoryForm(instance=obj)
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Редактировать категорию оборудования', 'back_url': 'studios:admin_equipment_categories'})

@admin_required
def admin_equipment_category_delete(request, pk):
    get_object_or_404(EquipmentCategory, pk=pk).delete()
    return redirect('studios:admin_equipment_categories')


# ===== ОБОРУДОВАНИЕ =====
@admin_required
def admin_equipment_list(request):
    items = Equipment.objects.select_related('category', 'studio').all()
    return render(request, 'studios/admin_equipment_list.html', {'items': items})

@admin_required
def admin_equipment_add(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Добавить оборудование', 'back_url': 'studios:admin_equipment_list'})

@admin_required
def admin_equipment_edit(request, pk):
    obj = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('studios:admin_equipment_list')
    else:
        form = EquipmentForm(instance=obj)
    return render(request, 'studios/admin_form.html', {'form': form, 'title': 'Редактировать оборудование', 'back_url': 'studios:admin_equipment_list'})

@admin_required
def admin_equipment_delete(request, pk):
    get_object_or_404(Equipment, pk=pk).delete()
    return redirect('studios:admin_equipment_list')


def index(request):
    """Главная страница"""
    popular_studios = Studio.objects.filter(is_available=True)[:5]
    return render(request, 'studios/index.html', {'popular_studios': popular_studios})


def catalog(request):
    """Каталог студий с фильтрацией"""
    studios = Studio.objects.filter(is_available=True)
    
    # Фильтр по категории (Category)
    category_id = request.GET.get('category')
    if category_id:
        studios = studios.filter(category_id=category_id)
    
    # Фильтр по интерьеру (Interior)
    interior_id = request.GET.get('interior')
    if interior_id:
        studios = studios.filter(interior_id=interior_id)
    
    # Фильтр по оборудованию (Equipment)
    equipment_id = request.GET.get('equipment')
    if equipment_id:
        studios = studios.filter(equipment__id=equipment_id).distinct()
    
    # Фильтр по цене
    price_range = request.GET.get('price_range')
    if price_range:
        if price_range == '0-1500':
            studios = studios.filter(price_per_hour__lte=1500)
        elif price_range == '1500-2500':
            studios = studios.filter(price_per_hour__gte=1500, price_per_hour__lte=2500)
        elif price_range == '2500-5000':
            studios = studios.filter(price_per_hour__gte=2500, price_per_hour__lte=5000)
        elif price_range == '5000+':
            studios = studios.filter(price_per_hour__gte=5000)
    
    # Фильтр по дате и времени
    date_str = request.GET.get('date')
    times_str = request.GET.get('times')
    if date_str and times_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            selected_times = [t.strip() for t in times_str.split(',') if t.strip()]
            
            available_ids = []
            for studio in studios:
                is_available = True
                for time_str in selected_times:
                    start_hour = int(time_str.split(':')[0])
                    end_hour = start_hour + 1
                    if not studio.is_available_at_time(filter_date, start_hour, end_hour):
                        is_available = False
                        break
                if is_available:
                    available_ids.append(studio.id)
            studios = studios.filter(id__in=available_ids)
        except (ValueError, TypeError):
            pass
    
    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price':
        studios = studios.order_by('price_per_hour')
    elif sort_by == '-price':
        studios = studios.order_by('-price_per_hour')
    elif sort_by == '-name':
        studios = studios.order_by('-name')
    else:
        studios = studios.order_by('name')
    
    user_favorites = set()
    if request.user.is_authenticated:
        from .models import Favorite
        user_favorites = set(
            Favorite.objects.filter(user=request.user).values_list('studio_id', flat=True)
        )

    context = {
        'studios': studios,
        'categories': Category.objects.all(),
        'interiors': Interior.objects.all(),
        'equipment_list': Equipment.objects.filter(is_available=True),
        'sort': sort_by,
        'filter_date': date_str or '',
        'filter_times': times_str or '',
        'selected_category': category_id or '',
        'selected_interior': interior_id or '',
        'selected_equipment': equipment_id or '',
        'user_favorites': user_favorites,
    }

    return render(request, 'studios/catalog.html', context)



def create_booking(request):
    """Создание бронирования"""
    try:
        data = json.loads(request.body)
        
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        start_time = int(data['start_time'].split(':')[0])
        end_time = int(data['end_time'])
        
        start_datetime = timezone.make_aware(
            datetime.combine(start_date, datetime.strptime(f"{start_time:02d}:00", "%H:%M").time())
        )
        end_datetime = timezone.make_aware(
            datetime.combine(end_date, datetime.strptime(f"{end_time:02d}:00", "%H:%M").time())
        )
        
        studio = get_object_or_404(Studio, pk=data['studio_id'])
        
        if not studio.is_available_at_time(start_date, start_time, end_time):
            return JsonResponse({'success': False, 'error': 'Выбранное время уже забронировано'})
        
        booking = Booking.objects.create(
            user=request.user,
            studio=studio,
            start_time=start_datetime,
            end_time=end_datetime,
            status='pending'
        )
        
        if 'equipment' in data and data['equipment']:
            booking.equipment.set(data['equipment'])
        
        return JsonResponse({'success': True, 'booking_id': booking.id})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def user_register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('studios:catalog')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'studios/register.html', {'form': form})


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('studios:catalog')
    else:
        form = UserLoginForm()
    
    return render(request, 'studios/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('studios:index')


def delete_account(request):
    """Удаление аккаунта пользователя вместе с его бронированиями."""
    if not request.user.is_authenticated:
        return redirect('studios:login')

    if request.method == 'POST':
        user = request.user
        # Booking.user = on_delete=CASCADE, поэтому бронирования удалятся автоматически.
        user.delete()
        logout(request)
        return redirect('studios:index')

    return redirect('studios:profile')


def user_profile(request):
    """Личный кабинет пользователя"""
    if not request.user.is_authenticated:
        return redirect('studios:login')
    
    user = request.user
    
    # Все бронирования
    all_bookings = Booking.objects.filter(user=user).select_related('studio').prefetch_related('equipment')
    
    # Активные бронирования (pending и confirmed)
    active_bookings = all_bookings.filter(status__in=['pending', 'confirmed'])
    
    # История (rejected и completed)
    history_bookings = all_bookings.filter(status__in=['rejected'])
    
    # Избранные студии
    favorite_studios = Studio.objects.filter(favorited_by__user=user)

    
    # Статистика
    total_bookings = all_bookings.count()
    active_count = active_bookings.count()
    favorites_count = favorite_studios.count()
    
    # Определяем активную вкладку
    active_tab = request.GET.get('tab', 'active')
    
    context = {
        'user': user,
        'all_bookings': all_bookings,
        'active_bookings': active_bookings,
        'history_bookings': history_bookings,
        'favorite_studios': favorite_studios,
        'total_bookings': total_bookings,
        'active_count': active_count,
        'favorites_count': favorites_count,
        'active_tab': active_tab,
    }
    return render(request, 'studios/profile.html', context)


def cancel_booking(request, booking_id):
    """Отмена бронирования"""
    if not request.user.is_authenticated:
        return redirect('studios:login')
    
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'rejected'
        booking.rejection_reason = 'Отменено пользователем'
        booking.save()
    
    return redirect('studios:profile')


def toggle_favorite(request, studio_id):
    """Добавить/удалить студию из избранного"""
    if not request.user.is_authenticated:
        return redirect('studios:login')
    
    studio = get_object_or_404(Studio, pk=studio_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, studio=studio)
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})
    
    return redirect(request.META.get('HTTP_REFERER', 'studios:profile'))

def studio_detail(request, pk):
    """Детальная страница студии"""
    studio = get_object_or_404(Studio, pk=pk)
    photos = studio.photos.all()
    equipment = studio.equipment.filter(is_available=True)
    # Отзывы/предоплаты удалены из проекта
    reviews = []



    
    today = timezone.now().date()
    days = []
    day_names = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    month_names = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
                   'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    # Собираем занятые слоты с учётом timezone
    booked_slots = set()
    confirmed_bookings = studio.bookings.filter(status__in=['pending', 'confirmed'])
    for booking in confirmed_bookings:
        current = booking.start_time
        while current < booking.end_time:
            local_current = timezone.localtime(current)
            booked_slots.add(local_current.strftime('%Y-%m-%d_%H:00'))
            current += timedelta(hours=1)

    for i in range(28):
        date = today + timedelta(days=i)
        day_of_week = date.weekday()

        days.append({
            'date': date.isoformat(),
            'name': f'{day_names[day_of_week]}, {date.day}',
            'full_date': f'{date.day} {month_names[date.month - 1]}',
            'day_name': day_names[day_of_week],
            'day_number': date.day,
            'is_available': True,
            'is_booked': False,
        })

    hours = [f'{h:02d}:00' for h in range(10, 23)]

    context = {
        'studio': studio,
        'photos': photos,
        'equipment': equipment,
        'reviews': reviews,
        'days': days,
        'hours': hours,
        'booked_slots': list(booked_slots),
    }

    return render(request, 'studios/studio_detail.html', context)

def admin_required(view_func):
    """Декоратор: только для админов"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('studios:index')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_panel(request):
    active_tab = request.GET.get('tab', 'bookings')

    bookings = Booking.objects.select_related('user', 'studio').order_by('-created_at')
    users = User.objects.all().order_by('-created_at')
    studios = Studio.objects.select_related('category', 'interior').order_by('name')

    # Статистика
    stats = {
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(status='pending').count(),
        'confirmed_bookings': bookings.filter(status='confirmed').count(),
        'total_users': users.count(),
        'total_studios': studios.count(),
        'available_studios': studios.filter(is_available=True).count(),
    }

    context = {
        'active_tab': active_tab,
        'bookings': bookings,
        'users': users,
        'studios': studios,
        'stats': stats,
    }
    return render(request, 'studios/admin_panel.html', context)


@admin_required
def admin_confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.status = 'confirmed'
    booking.rejection_reason = ''
    booking.save()
    return redirect('/admin-panel/?tab=bookings')


@admin_required
def admin_reject_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.status = 'rejected'
        booking.rejection_reason = request.POST.get('reason', 'Отклонено администратором')
        booking.save()
    return redirect(f"/admin-panel/?tab=bookings")


@admin_required
def admin_delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
    return redirect('/admin-panel/?tab=bookings')


@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user != request.user:
        user.delete()
    return redirect('/admin-panel/?tab=users')


@admin_required
def admin_toggle_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()
    return redirect('/admin-panel/?tab=users')


@admin_required
def admin_delete_studio(request, studio_id):
    studio = get_object_or_404(Studio, pk=studio_id)
    studio.delete()
    return redirect('/admin-panel/?tab=studios')


@admin_required
def admin_toggle_studio(request, studio_id):
    studio = get_object_or_404(Studio, pk=studio_id)
    studio.is_available = not studio.is_available
    studio.save()
    return redirect('/admin-panel/?tab=studios')
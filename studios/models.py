from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
import re


class UserManager(BaseUserManager):
    """Кастомный менеджер пользователей"""
    
    def create_user(self, login, first_name, last_name, phone, email, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен для заполнения')
        if not email:
            raise ValueError('Email обязателен для заполнения')
        
        email = self.normalize_email(email)
        user = self.model(
            login=login,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone=phone,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, login, first_name, last_name, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')
        
        return self.create_user(login, first_name, last_name, phone, email, password, **extra_fields)


# ========== ТАБЛИЦА 1: ПОЛЬЗОВАТЕЛЬ ==========
class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь системы"""
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('admin', 'Администратор'),
        ('staff', 'Сотрудник'),
    )
    
    login = models.CharField('Логин', max_length=100, unique=True, null=False)
    first_name = models.CharField('Имя', max_length=100, null=False)
    last_name = models.CharField('Фамилия', max_length=100, null=False)
    email = models.EmailField('Email', max_length=255, unique=True, null=False)
    phone = models.CharField('Телефон', max_length=20, null=False)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='client', null=False)
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Доступ к админке', default=False)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True, null=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'email']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'user'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.login})"
    
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_short_name(self):
        return self.first_name


# ========== ТАБЛИЦА 2: КАТЕГОРИЯ ==========
class Category(models.Model):
    """Категории студий"""
    name = models.CharField('Название категории', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ========== ТАБЛИЦА 3: ИНТЕРЬЕР ==========
class Interior(models.Model):
    """Типы интерьеров"""
    name = models.CharField('Название интерьера', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Интерьер'
        verbose_name_plural = 'Интерьеры'
        db_table = 'interior'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ========== ТАБЛИЦА 4: СТУДИЯ ==========
class Studio(models.Model):
    """Студийное помещение"""
    name = models.CharField('Название', max_length=255, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, 
        related_name='studios', 
        null=True, blank=True,
        verbose_name='Категория'
    )
    interior = models.ForeignKey(
        Interior, on_delete=models.CASCADE, 
        related_name='studios',
        null=True, blank=True,
        verbose_name='Интерьер'
    )
    description = models.TextField('Описание', null=False)
    price_per_hour = models.DecimalField('Цена за час', max_digits=10, decimal_places=2, null=False)
    area = models.IntegerField('Площадь (м²)', null=False)
    ceiling_height = models.IntegerField('Высота потолков (м)', default=3, null=False)
    is_available = models.BooleanField('Доступна', default=True, null=False)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True, null=False)
    
    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'
        db_table = 'studio'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def is_available_at_time(self, date, start_hour, end_hour):
        """Проверка доступности студии на конкретное время"""
        start_time = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.strptime(f"{start_hour:02d}:00", "%H:%M").time())
        )
        end_time = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.strptime(f"{end_hour:02d}:00", "%H:%M").time())
        )
        
        conflicting_bookings = self.bookings.filter(
            status__in=['pending', 'confirmed'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        return not conflicting_bookings.exists()


# ========== ТАБЛИЦА 5: ФОТОГРАФИИ СТУДИЙ ==========
class StudioPhoto(models.Model):
    """Фотографии студий"""
    studio = models.ForeignKey(
        Studio, on_delete=models.CASCADE, 
        related_name='photos', 
        null=False,
        verbose_name='Студия'
    )
    image = models.ImageField('Фото', upload_to='studios/', null=False)
    order = models.IntegerField('Порядок', default=0, null=False)
    
    class Meta:
        verbose_name = 'Фотография студии'
        verbose_name_plural = 'Фотографии студий'
        db_table = 'studiophoto'
        ordering = ['order']
    
    def __str__(self):
        return f"Фото {self.studio.name}"


# ========== ТАБЛИЦА 6: КАТЕГОРИЯ ОБОРУДОВАНИЯ ==========
class EquipmentCategory(models.Model):
    """Категории оборудования"""
    name = models.CharField('Название категории', max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Категория оборудования'
        verbose_name_plural = 'Категории оборудования'
        db_table = 'equipment_category'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ========== ТАБЛИЦА 7: ОБОРУДОВАНИЕ ==========
class Equipment(models.Model):
    """Оборудование"""
    name = models.CharField('Название', max_length=255, null=False)
    category = models.ForeignKey(
        EquipmentCategory, on_delete=models.CASCADE,
        related_name='equipment',
        null=True, blank=True,
        verbose_name='Категория оборудования'
    )
    description = models.TextField('Описание', null=False, blank=True)
    is_available = models.BooleanField('Доступно', default=True, null=False)
    studio = models.ForeignKey(
        Studio, on_delete=models.CASCADE, 
        related_name='equipment', 
        null=True, blank=True, 
        verbose_name='Студия'
    )
    
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        db_table = 'equipment'
    
    def __str__(self):
        return self.name


# ========== ТАБЛИЦА 8: БРОНИРОВАНИЕ ==========
class Booking(models.Model):
    """Бронирование"""
    STATUS_CHOICES = (
        ('pending', 'На проверке'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=False)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='bookings', null=False)
    start_time = models.DateTimeField('Начало', null=False)
    end_time = models.DateTimeField('Окончание', null=False)
    equipment = models.ManyToManyField(Equipment, blank=True, related_name='bookings', verbose_name='Оборудование')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending', null=False)
    rejection_reason = models.TextField('Причина отклонения', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=False)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        db_table = 'booking'
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.studio.name} - {self.start_time}"

    def total_price(self):
        from decimal import Decimal
        hours = Decimal(str((self.end_time - self.start_time).total_seconds() / 3600))
        return int(hours * self.studio.price_per_hour)

# ========== ТАБЛИЦА 11: ИЗБРАННЫЕ СТУДИИ ==========
class Favorite(models.Model):
    """Избранные студии пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', null=False)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='favorited_by', null=False)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True, null=False)
    
    class Meta:
        verbose_name = 'Избранная студия'
        verbose_name_plural = 'Избранные студии'
        db_table = 'favorite'
        unique_together = ['user', 'studio']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.studio}"
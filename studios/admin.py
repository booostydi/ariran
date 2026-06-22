from django.contrib import admin
from .models import (
    User, Category, Interior, EquipmentCategory,
    Studio, StudioPhoto, Equipment, Booking, Favorite
)



class StudioPhotoInline(admin.TabularInline):
    model = StudioPhoto
    extra = 1
    fields = ['image', 'order']
    ordering = ['order']


class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 1
    fields = ['name', 'category', 'is_available']
    ordering = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'first_name', 'last_name', 'email', 'phone', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('login', 'email', 'first_name', 'last_name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ['name']


@admin.register(Interior)
class InteriorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ['name']


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'interior', 'price_per_hour', 'area_display', 'ceiling_height_display', 'is_available', 'created_at')
    list_filter = ('category', 'interior', 'is_available')
    search_fields = ('name', 'description')
    inlines = [StudioPhotoInline, EquipmentInline]
    
    fields = (
        'name',
        'category',
        'interior',
        'description',
        'price_per_hour',
        'area',
        'ceiling_height',
        'is_available',
    )
    
    def area_display(self, obj):
        return f"{obj.area} м²"
    area_display.short_description = 'Площадь'
    
    def ceiling_height_display(self, obj):
        return f"{obj.ceiling_height} м"
    ceiling_height_display.short_description = 'Высота потолков'


@admin.register(StudioPhoto)
class StudioPhotoAdmin(admin.ModelAdmin):
    list_display = ('studio', 'image', 'order')
    list_filter = ('studio',)
    ordering = ['studio', 'order']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'studio', 'is_available')
    list_filter = ('category', 'is_available', 'studio')
    search_fields = ('name', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'studio', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status',)
    date_hierarchy = 'start_time'
    filter_horizontal = ('equipment',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'studio', 'created_at')
    list_filter = ('user',)
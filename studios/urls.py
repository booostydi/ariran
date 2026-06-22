from django.urls import path
from . import views

app_name = 'studios'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('studio/<int:pk>/', views.studio_detail, name='studio_detail'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('profile/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('profile/favorite/<int:studio_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # Админка
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # Бронирования (админ)
    path('admin-panel/booking/<int:booking_id>/confirm/', views.admin_confirm_booking, name='admin_confirm_booking'),
    path('admin-panel/booking/<int:booking_id>/reject/', views.admin_reject_booking, name='admin_reject_booking'),
    path('admin-panel/booking/<int:booking_id>/delete/', views.admin_delete_booking, name='admin_delete_booking'),

    # Пользователи (админ)
    path('admin-panel/users/<int:user_id>/toggle/', views.admin_toggle_user, name='admin_toggle_user'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),

    # Студии
    path('admin-panel/studio/add/', views.admin_studio_add, name='admin_studio_add'),
    path('admin-panel/studio/<int:studio_id>/edit/', views.admin_studio_edit, name='admin_studio_edit'),
    path('admin-panel/studio/<int:studio_id>/toggle/', views.admin_toggle_studio, name='admin_toggle_studio'),
    path('admin-panel/studio/<int:studio_id>/delete/', views.admin_delete_studio, name='admin_delete_studio'),

    # Категории
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/category/add/', views.admin_category_add, name='admin_category_add'),
    path('admin-panel/category/<int:pk>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('admin-panel/category/<int:pk>/delete/', views.admin_category_delete, name='admin_category_delete'),
    
    # Интерьеры
    path('admin-panel/interiors/', views.admin_interiors, name='admin_interiors'),
    path('admin-panel/interior/add/', views.admin_interior_add, name='admin_interior_add'),
    path('admin-panel/interior/<int:pk>/edit/', views.admin_interior_edit, name='admin_interior_edit'),
    path('admin-panel/interior/<int:pk>/delete/', views.admin_interior_delete, name='admin_interior_delete'),
    
    # Категории оборудования
    path('admin-panel/equipment-categories/', views.admin_equipment_categories, name='admin_equipment_categories'),
    path('admin-panel/equipment-category/add/', views.admin_equipment_category_add, name='admin_equipment_category_add'),
    path('admin-panel/equipment-category/<int:pk>/edit/', views.admin_equipment_category_edit, name='admin_equipment_category_edit'),
    path('admin-panel/equipment-category/<int:pk>/delete/', views.admin_equipment_category_delete, name='admin_equipment_category_delete'),
    
    # Оборудование
    path('admin-panel/equipment/', views.admin_equipment_list, name='admin_equipment_list'),
    path('admin-panel/equipment/add/', views.admin_equipment_add, name='admin_equipment_add'),
    path('admin-panel/equipment/<int:pk>/edit/', views.admin_equipment_edit, name='admin_equipment_edit'),
    path('admin-panel/equipment/<int:pk>/delete/', views.admin_equipment_delete, name='admin_equipment_delete'),
]
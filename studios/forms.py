from django import forms
from django.contrib.auth.forms import AuthenticationForm
import re
from .models import User, Booking, Studio, Category, Interior, EquipmentCategory, Equipment, StudioPhoto

class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = ['name', 'category', 'interior', 'description', 'price_per_hour', 'area', 'ceiling_height', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'adm-input'}),
            'category': forms.Select(attrs={'class': 'adm-select'}),
            'interior': forms.Select(attrs={'class': 'adm-select'}),
            'description': forms.Textarea(attrs={'class': 'adm-textarea', 'rows': 4}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'adm-input'}),
            'area': forms.NumberInput(attrs={'class': 'adm-input'}),
            'ceiling_height': forms.NumberInput(attrs={'class': 'adm-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'adm-checkbox'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'adm-input'}),
            'description': forms.Textarea(attrs={'class': 'adm-textarea', 'rows': 3}),
        }

class InteriorForm(forms.ModelForm):
    class Meta:
        model = Interior
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'adm-input'}),
            'description': forms.Textarea(attrs={'class': 'adm-textarea', 'rows': 3}),
        }

class EquipmentCategoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'adm-input'}),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'description', 'is_available', 'studio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'adm-input'}),
            'category': forms.Select(attrs={'class': 'adm-select'}),
            'description': forms.Textarea(attrs={'class': 'adm-textarea', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'adm-checkbox'}),
            'studio': forms.Select(attrs={'class': 'adm-select'}),
        }

class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}),
        min_length=8,
        help_text='Минимум 8 символов'
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        min_length=8
    )
    
    class Meta:
        model = User
        fields = ['login', 'first_name', 'last_name', 'phone', 'email']
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Логин (только латиница)',
                'pattern': '[a-zA-Z0-9_]+',
                'title': 'Только латинские буквы, цифры и подчёркивание'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Имя (только кириллица)',
                'pattern': '[а-яА-ЯёЁ\\s-]+',
                'title': 'Только кириллица'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Фамилия (только кириллица)',
                'pattern': '[а-яА-ЯёЁ\\s-]+',
                'title': 'Только кириллица'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+7(___)-___-__-__',
                'id': 'id_phone',
                'maxlength': '18'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'example@mail.ru'
            }),
        }
    
    def clean_login(self):
        login = self.cleaned_data.get('login')
        if not re.match(r'^[a-zA-Z0-9_]+$', login):
            raise forms.ValidationError('Логин должен содержать только латинские буквы, цифры и подчёркивание')
        return login
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', first_name):
            raise forms.ValidationError('Имя должно содержать только кириллицу')
        if len(first_name.strip()) < 2:
            raise forms.ValidationError('Имя должно содержать минимум 2 символа')
        return first_name.strip()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', last_name):
            raise forms.ValidationError('Фамилия должна содержать только кириллицу')
        return last_name.strip()
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Удаляем все нецифровые символы
        phone_clean = re.sub(r'\D', '', phone)
        if not phone_clean.startswith('7') and not phone_clean.startswith('8'):
            raise forms.ValidationError('Номер телефона должен начинаться с +7')
        if len(phone_clean) != 11:
            raise forms.ValidationError('Номер телефона должен содержать 11 цифр')
        return phone
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return password_confirm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введите ваш логин',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введите ваш пароль'
        })
    )


class BookingForm(forms.ModelForm):
    """Форма бронирования"""
    class Meta:
        model = Booking
        fields = ['studio', 'start_time', 'end_time', 'status', 'rejection_reason']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
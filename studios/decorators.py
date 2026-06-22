from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """
    Декоратор для проверки прав администратора.
    Проверяет, что пользователь авторизован и имеет роль 'admin'.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Проверяем авторизацию
        if not request.user.is_authenticated:
            return redirect('studios:login')
        
        # Проверяем роль (admin или is_staff)
        if not (request.user.role == 'admin' or request.user.is_staff):
            messages.error(request, 'Доступ запрещён. Требуются права администратора.')
            return redirect('studios:index')
        
        return view_func(request, *args, **kwargs)
    return wrapper
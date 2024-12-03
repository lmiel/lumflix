# carpeta: authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def user_register(request):
    """Vista para registrar nuevos usuarios."""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('authentication:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
            return redirect('authentication:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
        return redirect('authentication:login')

    return render(request, 'authentication/register.html')

def user_login(request):
    """Vista para iniciar sesión."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('streaming:home')
        else:
            messages.error(request, "Credenciales inválidas. Por favor, inténtalo de nuevo.")
            return redirect('authentication:login')

    return render(request, 'authentication/login.html')

def user_logout(request):
    """Vista para cerrar sesión."""
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('authentication:login')

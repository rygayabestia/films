from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        login = request.POST['login']
        password = request.POST['password']
        User.objects.create(name=name, login=login, password=password)
        return redirect('login')
    return render(request, 'users/register.html')

def user_login(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, login=login, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Перенаправляем на профиль после входа
        else:
            return render(request, 'users/login.html', {'error': 'Invalid login or password'})
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('movie_list')

def profile(request):
    if request.method == 'POST':
        # Обновляем данные пользователя
        user = request.user
        user.name = request.POST.get('name', user.name)
        user.login = request.POST.get('login', user.login)
        user.password = request.POST.get('password', user.password)
        user.save()
        return redirect('profile')
    return render(request, 'users/profile.html', {'user': request.user})
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login as login_user, logout as logout_user

active_tab_login = '\'login\''
active_tab_logout = '\'logout\''
active_tab_register = '\'register\''


def register(response):
    page_title = 'Создать аккаунт'
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else:
        form = RegisterForm()

    return render(response, 'register/register.html',
                  {'form': form, 'page_title': page_title, 'active_tab': active_tab_register})


def login(request):
    page_title = 'Войти'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_user(request, user)
            return redirect('/')
        else:
            auth_error = True
            variables = {
                'form': form, 'auth_error': auth_error, 'page_title': page_title, 'active_tab': active_tab_login}
            return render(request, 'registration/login.html', context=variables)
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'page_title': page_title,
                                                       'active_tab': active_tab_login})


def logout(request):
    page_title = 'Выйти'
    if request.method == 'POST':
        logout_user(request)
        return redirect('/')
    else:
        return render(request, 'registration/logout.html', {'page_title': page_title,
                                                            'active_tab': active_tab_logout})

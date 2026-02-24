from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.forms import CustomUserCreationForm
from kernel import settings


def cadastrar(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


def logar(request):
    template_name = 'accounts/login.html'
    if request.method == 'GET':
        return render(request, template_name)
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    # Usuário autenticado
    if user is not None:
        auth_login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    msg = f'Usuário/senha inválidos. Reveja!'
    messages.error(request, msg)
    return render(request, template_name)


@login_required
def sair(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

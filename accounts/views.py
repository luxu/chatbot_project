from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from kernel import settings

def cadastrar(request):
    template_name = 'accounts/register.html'
    msg = ''
    if request.method == 'GET':
        return render(request, template_name)
    username = request.POST.get('username')
    if len(username) < 3:
        msg = 'Nome de usuário deve ter pelo menos 3 caracteres.'
        messages.error(request,msg)
    email = request.POST.get('email')
    if '@' not in email:
        msg = 'Email inválido. Tente novamente.'
        messages.error(request,msg)
    if User.objects.filter(email=email).first():
        msg = 'Email já cadastrado. Tente novamente.'
        messages.error(request, msg)
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if password != confirm_password:
        msg = 'Senhas não coincidem. Tente novamente.'
        messages.error(request,msg)
    try:
        validate_password(password, user=None)
    except ValidationError as e:
        msg = f"ERRO..: {e}"
        messages.error(request, msg)
    try:
        user = User.objects.create_user(username=username, email=email)
    except IntegrityError:
        msg = "Usuário já existe. Crie outro"
        messages.error(request, msg)
    if len(msg) > 0:
        context = {
            'username': username,
            'email': email
        }
        return render(request, template_name, context)
    user.set_password(password)
    user.save()
    messages.success(request,'Cadastro realizado com sucesso!')
    return redirect(reverse_lazy('index'))

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

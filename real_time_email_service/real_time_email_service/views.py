from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, 'home.html')  

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a home após o login
    return render(request, 'messaging/login.html')  # Renderiza o template de login



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')  # Redireciona para a home após o registro
    return render(request, 'register.html')  # Renderiza o template de registro


def send_message(request):
    if request.method == 'POST':
        # Lógica para enviar mensagem
        message = request.POST.get('message')
        # Aqui você poderia salvar a mensagem no banco de dados ou processá-la
        return JsonResponse({'status': 'success', 'message': message})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Registro realizado com sucesso!')
                return redirect('login')  # Redireciona para a página de login
            except:
                messages.error(request, 'Erro ao registrar o usuário.')
        else:
            messages.error(request, 'As senhas não coincidem.')
    
    return render(request, 'registration/register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redireciona para a página inicial após login
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')

    return render(request, 'registration/login.html')

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')



from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from messaging.models import Message




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

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f"user_{self.user.id}"

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

    async def notify_user(self, event):
        await self.send(text_data=json.dumps(event))


@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipient_username = data.get('recipient')
        title = data.get('title')
        body = data.get('body')

        try:
            recipient = User.objects.get(username=recipient_username)
            message = Message(sender=request.user, recipient=recipient, title=title, body=body)
            message.save()

            # Notify the recipient via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{recipient.id}",
                {
                    'type': 'notify_user',
                    'message': f"You have a new message from {request.user.username}: {title}",
                }
            )

            return JsonResponse({'status': 'success'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=400)

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Carregar dados do pedido
        recipient_username = data.get('recipient')  # Obter nome do destinatário
        title = data.get('title')  # Obter título da mensagem
        body = data.get('body')  # Obter corpo da mensagem

        try:
            recipient = User.objects.get(username=recipient_username)  # Obter o usuário destinatário
            message = Message(sender=request.user, recipient=recipient, title=title, body=body)  # Criar mensagem
            message.save()  # Salvar mensagem no banco de dados

            channel_layer = get_channel_layer()  # Obter o canal de camada
            async_to_sync(channel_layer.group_send)(
                f"user_{recipient.id}",
                {
                    'type': 'notify_user',  # Tipo de evento
                    'message': f"Você tem uma nova mensagem de {request.user.username}: {title}",  # Mensagem de notificação
                }
            )
            return JsonResponse({'status': 'sucesso'}, status=201) 
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário não existe'}, status=404)  
    return JsonResponse({'error': 'Método inválido'}, status=400)

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
                return redirect('login')  
            except:
                messages.error(request, 'Erro ao registrar o usuário.')
        else:
            messages.error(request, 'As senhas não coincidem.')
    
    return render(request, 'registration/register.html')

@login_required
def index(request):
    mensagens_recebidas = Message.objects.filter(recipient=request.user)  # Filtra mensagens recebidas
    return render(request, 'index.html', {'mensagens_recebidas': mensagens_recebidas})



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

# @login_required
# def home(request):
#     mensagens_recebidas = Message.objects.filter(recipient=request.user)
#     return render(request, 'home.html', {'mensagens_recebidas': mensagens_recebidas})




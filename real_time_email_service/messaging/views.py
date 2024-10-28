from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
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
from django.contrib import messages

def home(request):
    return render(request, 'home.html')


def register_view(request):
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

    return render(request, 'messaging/register.html')


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

        # Aqui você pode processar a mensagem recebida, se necessário
        await self.notify_user(text_data_json)

    async def notify_user(self, event):
        await self.send(text_data=json.dumps(event))

@csrf_exempt
@login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Dados recebidos:", data)  # Log dos dados recebidos

            recipient_username = data.get('recipient')
            title = data.get('title')
            body = data.get('body')

            # Validação dos dados recebidos
            if not recipient_username or not title or not body:
                return JsonResponse({'error': 'Dados faltando'}, status=400)

            # Tentando encontrar o usuário destinatário
            try:
                recipient = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Usuário não existe'}, status=404)

            # Criação da mensagem
            message = Message(sender=request.user, recipient=recipient, title=title, body=body)
            message.save()

            # Envio da notificação via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{recipient.id}",
                {
                    'type': 'notify_user',
                    'message': f"Você tem uma nova mensagem de {request.user.username}: {title}",
                }
            )
            return JsonResponse({'status': 'success'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método inválido'}, status=400)


@login_required
def index(request):
    mensagens_recebidas = Message.objects.filter(recipient=request.user)
    return render(request, 'messaging/index.html', {'mensagens_recebidas': mensagens_recebidas})


@login_required
def painel(request):
    mensagens_recebidas = Message.objects.filter(recipient=request.user)
    return render(request, 'messaging/painel.html', {'mensagens_recebidas': mensagens_recebidas})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('painel')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')

    return render(request, 'messaging/login.html')

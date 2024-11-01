from rest_framework import generics, permissions
from messaging.serializers import MessageSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from messaging.models import Message


# View para visualizar a caixa de entrada (inbox)
class InboxView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

def index(request):
    return render(request, 'messaging/index.html')

# View para marcar uma mensagem como lida
class MarkMessageAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, recipient=request.user)
            message.is_read = True  # Corrigido para 'is_read'
            message.save()
            return Response({'status': 'Mensagem marcada como lida!'})
        except Message.DoesNotExist:
            return Response({'error': 'Mensagem não encontrada.'}, status=status.HTTP_404_NOT_FOUND)


def home(request):
    return render(request, 'home.html') 

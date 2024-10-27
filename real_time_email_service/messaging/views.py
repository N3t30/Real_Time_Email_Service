from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import models
from django.contrib.auth.models import User

class SendMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class InboxView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)

class OutboxView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)
    
def index(request):
    return render(request, 'messaging/index.html')

# View para envio de mensagem
class MarkMessageAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, recipient=request.user)
            message.is_read = True
            message.save()
            return Response({'status': 'Mensagem marcada como lida!'})
        except Message.DoesNotExist:
            return Response({'error': 'Mensagem não encontrada.'}, status=status.HTTP_404_NOT_FOUND)




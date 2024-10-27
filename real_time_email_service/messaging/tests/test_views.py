from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Message

class MessageViewTests(APITestCase):
    
    def setUp(self):
        # Criação de usuários para testes
        self.sender = User.objects.create_user(username='sender', password='senderpass')
        self.recipient = User.objects.create_user(username='recipient', password='recipientpass')
        self.client.login(username='sender', password='senderpass')  # Logar o usuário sender
        
        self.message_data = {
            'sender': self.sender.id,
            'recipient': self.recipient.id,
            'title': 'Test Message',
            'body': 'This is a test message.'
        }

    def test_create_message(self):
        """Testa a criação de uma nova mensagem."""
        url = reverse('message-list')  # Substitua 'message-list' pela sua URL real
        response = self.client.post(url, self.message_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().title, 'Test Message')

    def test_get_messages(self):
        """Testa a obtenção da lista de mensagens."""
        Message.objects.create(**self.message_data)  # Cria uma mensagem
        url = reverse('mark_as_read') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Espera-se que haja 1 mensagem

    def test_get_single_message(self):
        """Testa a obtenção de uma única mensagem."""
        message = Message.objects.create(**self.message_data)
        url = reverse('mark_as_read', args=[message.id]) 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], message.title)

    def test_delete_message(self):
        """Testa a exclusão de uma mensagem."""
        message = Message.objects.create(**self.message_data)
        url = reverse('mark_as_read', args=[message.id]) 
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)  # Verifica se a mensagem foi excluída

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Message 

class MessageModelTests(TestCase):

    def setUp(self):
        # criando usuarios para enviar e receber mensagens
        self.sender = User.objects.create_user(username='sender', password='senderpass')
        self.recipient = User.objects.create_user(username='recipient', password='recipientpass')
        
        # fazendo uma instância de mensagem
        self.message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            title='teste de mensagem',
            body='esse é um teste de mensagem'
        )

    def test_message_creation(self):
        """Verifica se a instância da mensagem é criada corretamente."""
        self.assertIsNotNone(self.message)
        self.assertEqual(self.message.title, 'Teste mensagem')
        self.assertEqual(self.message.body, 'Isso é um teste de mensagem')
        self.assertEqual(self.message.sender, self.sender)
        self.assertEqual(self.message.recipient, self.recipient)

    def test_message_str(self):
        """Verifica a representação em string da mensagem."""
        self.assertEqual(str(self.message), f"{self.sender} para {self.recipient}: teste mensagem")

    def test_message_read_default(self):
        """Verifica se o campo 'read' é False."""
        self.assertFalse(self.message.read)

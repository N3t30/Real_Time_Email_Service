from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
    # Verificando se um token de autenticação pode ser obtido com credenciais válidas.
    def test_token_obtain(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    #  Verificando se o sistema exclui credenciais inválidas ao tentar obter um token.
    def test_token_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {"username": "testuser", "password": "wrongpass"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

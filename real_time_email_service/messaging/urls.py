from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home,
    SendMessageView,
    InboxView,
    OutboxView,
    index,
    MarkMessageAsReadView,
    register,
    login_view,
    painel,
)

urlpatterns = [
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('send/', SendMessageView.as_view(), name='send_message'),  # Certifique-se de que o nome aqui seja 'send_message'
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('outbox/', OutboxView.as_view(), name='outbox'),
    path('mark/<int:message_id>/', MarkMessageAsReadView.as_view(), name='mark_message_as_read'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('painel/', painel, name='painel'),
]

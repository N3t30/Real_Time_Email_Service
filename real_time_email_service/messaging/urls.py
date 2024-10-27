from django.urls import path
from .views import home, SendMessageView, InboxView, OutboxView, index, MarkMessageAsReadView, register, login_view

urlpatterns = [
    path('', home, name='home'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('outbox/', OutboxView.as_view(), name='outbox'),
    path('messages/read/<int:message_id>/', MarkMessageAsReadView.as_view(), name='mark_as_read'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'), 
]

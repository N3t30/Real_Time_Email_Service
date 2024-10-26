from django.urls import path
from .views import SendMessageView, InboxView, OutboxView, index

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('outbox/', OutboxView.as_view(), name='outbox'),
    path('', index, name='index'),
]

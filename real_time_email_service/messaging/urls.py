from django.urls import path
from .views import SendMessageView, InboxView, OutboxView, index,  MarkMessageAsReadView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('outbox/', OutboxView.as_view(), name='outbox'),
    path('messages/read/<int:message_id>/', MarkMessageAsReadView.as_view(), name='mark_as_read'),
    path('', index, name='index'),
]

from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'title', 'body', 'created_at')
    search_fields = ('title', 'body')
    list_filter = ('recipient', 'created_at')

admin.site.register(Message, MessageAdmin)


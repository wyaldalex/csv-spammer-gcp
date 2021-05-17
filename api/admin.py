from django.contrib import admin
from .models import Message, Conversation, Customer

admin.site.register(Message)
admin.site.register(Customer)
admin.site.register(Conversation)

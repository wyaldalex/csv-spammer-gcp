from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('sendWAMessage', csrf_exempt(views.SendWhatsAppMessageView.as_view())),
    path('webhook', csrf_exempt(views.webhookMessageBird.as_view())),
    path('test', csrf_exempt(views.getConversationHistory.as_view())),
    path('ping', csrf_exempt(views.ping.as_view())),
]



from django.shortcuts import render
from webpush import send_user_notification

# Create your views here.
def index(request):
    payload = {"head": "Welcome!", "body": "Hello World"}
    send_user_notification(user=user, payload=payload, ttl=1000)
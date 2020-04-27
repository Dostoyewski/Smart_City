from django.shortcuts import render
from webpush import send_user_notification

# Create your views here.
def send_push(head,body,who):
    payload = {"head": head, "body": body}
    send_user_notification(user=who, payload=payload, ttl=1000)
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import UserProfile
from django.contrib.auth.models import User
from .forms import ChangeForm
import datetime as dt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification, send_group_notification
from django.conf import settings
import json


@require_POST
@csrf_exempt
def send_push(request):
    """
    This function gets JSON with body and head, than pushes message
    :param request:
    :return: JSONResponse with status
    """
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})


def send_to_user(head, body, user, icon="https://i.imgur.com/dRDxiCQ.png", url="https://www.example.com"):
    """
    This function will send push-notification to user
    :param head: HEAD of notification
    :type head: text
    :param body: BODY of the message
    :type body: text
    :param user: User object, that wil see this message
    :type user: User object
    :param icon: icon for notification
    :param url: notification-URL
    :return:
    """
    payload = {'head': head, 'body': body,
               "icon": icon, "url": url}
    send_user_notification(user=user, payload=payload, ttl=1000)


@login_required
@require_GET
def home(request):
    """
    This funciton represents the main page
    :param request:
    :return:
    """
    #send_to_user('INFO', 'This is the main page', get_object_or_404(User, pk=request.user.pk))
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    return render(request, 'main/home.html', {user: user, 'vapid_key': vapid_key})


@login_required
def profile(request):
    """
    This function creates User Profile site with info
    :param request: request to this site
    :return: JSON render
    """
    #send_to_user('INFO', 'This is your profile', get_object_or_404(User, pk=request.user.pk))
    try:
        obj = UserProfile.objects.get(user_id=request.user.pk)
        age = dt.date.today().year - obj.age.year
        return render(request, 'main/account.html', {'email': obj.user.email, 'name': obj.name,
                                                     'vorname': obj.vorname, 'fname': obj.fathername,
                                                     'gender': obj.gender, 'age': age,
                                                     'position': obj.position, 'exp': obj.exp,
                                                     'isFull': obj.isFull, 'avatar': obj.avatar,
                                                     'bdate': obj.age, 'message': obj.message})
    except:
        return HttpResponseRedirect("/accounts/changeform/")


@login_required
def update_profile(request):
    """
    This function creates form for updating user data
    :param request: request
    :return: render
    """
    print(request)
    if request.method == 'POST':
        obj = UserProfile.objects.get(user_id=request.user.pk)
        form = ChangeForm(request.POST, request.FILES, initial={
            'name': obj.name, 'vorname': obj.vorname,
            'fathername': obj.fathername, 'gender': obj.gender,
            'age': obj.age, 'position': obj.position,
            'exp': obj.exp
        })
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.vorname = form.cleaned_data['vorname']
            obj.fathername = form.cleaned_data['fathername']
            obj.gender = form.cleaned_data['gender']
            obj.age = form.cleaned_data['age']
            obj.position = form.cleaned_data['position']
            obj.exp = form.cleaned_data['exp']
            obj.isFull = True
            obj.save()
            print('saved')
            return HttpResponseRedirect('/accounts/profile/')
    else:
        print('render')
        obj = UserProfile.objects.get(user_id=request.user.pk)
        form = ChangeForm(request.POST, request.FILES, initial={
            'name': obj.name, 'vorname': obj.vorname,
            'fathername': obj.fathername, 'gender': obj.gender,
            'age': obj.age, 'position': obj.position,
            'exp': obj.exp
        })
    return render(request, 'main/change.html', {'form': form})

  
def mapi(request):
    return render(request,'test.html')

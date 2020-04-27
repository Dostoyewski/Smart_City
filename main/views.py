from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile
from .forms import ChangeForm
import datetime as dt


def profile(request):
    """
    This function creates User Profile site with info
    :param request: request to this site
    :return: JSON render
    """
    obj = UserProfile.objects.get(user_id=request.user.pk)
    age = dt.date.today().year - obj.age.year
    return render(request, 'main/account.html', {'email': obj.user.email, 'name': obj.name,
                                                  'vorname': obj.vorname, 'fname': obj.fathername,
                                                  'gender': obj.gender, 'age': age,
                                                  'position': obj.position, 'exp': obj.exp,
                                                 'isFull': obj.isFull})


def update_profile(request):
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

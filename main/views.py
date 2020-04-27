from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, User


def profile(request):
    """
    This function creates User Profile site with info
    :param request: request to this site
    :return: JSON render
    """
    obj = UserProfile.objects.get(user_id=request.user.pk)
    return render(request, 'main/account.html', {'email': obj.user.email, 'name': obj.name,
                                                  'vorname': obj.vorname, 'fname': obj.fathername,
                                                  'gender': obj.gender, 'age': obj.age,
                                                  'position': obj.position, 'exp': obj.exp})
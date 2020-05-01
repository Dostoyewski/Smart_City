from django.shortcuts import render
from .forms import ParserForm
from .models import Anketa
from django.http import HttpResponseRedirect
# Create your views here.


def make_parsing(request):
    """
    This function creates form for updating user data
    :param request: request
    :return: render
    """
    if request.method == 'POST':
        form = ParserForm(request.POST, request.FILES)
        if form.is_valid():
            Anketa.objects.create_anketa(form.cleaned_data['name'],
                                         form.cleaned_data['vorname'],
                                         form.cleaned_data['fathername'],
                                         form.cleaned_data['gender'],
                                         form.cleaned_data['age'],
                                         form.cleaned_data['urlVK'])
            return HttpResponseRedirect('/parsing/results/')
    else:
        form = ParserForm(request.POST, request.FILES)
    return render(request, 'parsing/change.html', {'form': form})

from django.shortcuts import render
from .forms import ParserForm
from .models import Anketa
from Smart_City.settings import STATIC_ROOT
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


def show_results(request):
    obj = Anketa.objects.all()
    n = len(obj)
    obj = obj[n-1]
    pdfString = STATIC_ROOT + '/ID_' + obj.idVK + '.pdf'
    print(pdfString)
    return render(request, 'parsing/results.html', {'name': obj.name,
                                                    'vorname': obj.vorname,
                                                    'fname': obj.fathername,
                                                    'gender': obj.gender,
                                                    'age': obj.age,
                                                    'urlVK': obj.urlVK,
                                                    'idVK': obj.idVK,
                                                    'string': pdfString})

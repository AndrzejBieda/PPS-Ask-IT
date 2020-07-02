import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from Ask_IT.forms import QuestionContent
from Ask_IT.models import *


def base(request):
    return render(request, "Ask_IT/base.html")


def index(request):
    return render(request, 'Ask_IT/index.html')


def kategorie(request):
    return render(request, 'Ask_IT/kategorie.html',
                  {"kategorie": Category.objects.all})


def pagedown(request):
    if request.method == 'POST':
        form = QuestionContent(request.POST)
        if form.is_valid():
            titlefromform = form.cleaned_data.get('title')
            contentfromform = form.cleaned_data.get('content')
            datetoform = datetime.datetime.now()
            authortoform = User.objects.get(id=1)
            categorytoform = Category.objects.get(id=3)
            a = Question(title=titlefromform, content=contentfromform, author=authortoform, date=datetoform,
                         category=categorytoform)
            a.save()
            return HttpResponseRedirect('../pokaz/')
    else:
        form = QuestionContent()
        return render(request, 'Ask_IT/pagedown.html', {'form': form})


def pokaz(request):
    return render(request, 'Ask_IT/pokaz.html',
                  {"questions": Question.objects.all()})

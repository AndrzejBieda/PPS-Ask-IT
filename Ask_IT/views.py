import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Ask_IT.forms import QuestionContent
from Ask_IT.models import Category, Question, User


# from .forms import NameForm


def base(request):
    return render(request, "Ask_IT/base.html")


def index(request):
    return render(request, 'Ask_IT/index.html')


def categories(request):
    return render(request, 'Ask_IT/kategorie.html',
                  {"categories": Category.objects.all()})


def bbcode(request):
    return render(request, 'Ask_IT/bbcode.html')


def bbcode(request):
    if request.method == 'POST':
        form = QuestionContent(request.POST)
        if form.is_valid():
            # titlefromform = form.cleaned_data.get('title')
            titlefromform = "SUPER TYTUŁ"
            contentfromform = form.cleaned_data.get('content')
            datetoform = datetime.datetime.now()
            authortoform = User.objects.get(id=1)
            categorytoform = Category.objects.get(id=3)
            a = Question(title=titlefromform, content=contentfromform, author=authortoform, date=datetoform,
                         category=categorytoform)
            a.save()
            return HttpResponseRedirect('../pokazbb/')
    else:
        form = QuestionContent()
        return render(request, 'Ask_IT/bbcode.html')


def pokazbb(request):
    return render(request, 'Ask_IT/pokazbb.html',
                  {"questions": Question.objects.all()})

# def bbcode(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             bbcode = form.save(commit=False)
#             bbcode.save()
#             return HttpResponseRedirect('/bbcode/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, 'Ask_IT/bbcode.html', {'form': form})

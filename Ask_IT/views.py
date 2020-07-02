from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from Ask_IT.models import Category
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from Ask_IT.forms import QuestionContent
from Ask_IT.models import *


def index(request):
    return render(request, 'Ask_IT/index.html')


def kategorie(request):
    return render(request, 'Ask_IT/kategorie.html',
                  {"categories": Category.objects.all()})


def wpis(request):
    return render(request, 'Ask_IT/wpis.html')


def question(request):
    if request.method == 'POST':
        form = QuestionContent(request.POST)
        if form.is_valid():
            titlefromform = request.POST.get('title')
            contentfromform = form.cleaned_data.get('content')
            datetoform = datetime.datetime.now()
            authortoform = User.objects.get(username=request.user.username)
            categorytoform = get_object_or_404(Category, pk=request.POST.get('category'))
            a = Question(title=titlefromform, content=contentfromform, author=authortoform, date=datetoform,
                         category=categorytoform)
            a.save()
            return HttpResponseRedirect('/')
    else:
        form = QuestionContent()
        return render(request, 'Ask_IT/nowe-pytanie.html', {'form': form, "categories": Category.objects.all()})


def konto(request):
    return render(request, 'Ask_IT/konto.html')


def categoryThreads(request):
    return render(request, 'Ask_IT/kategoria-watki.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowano!")
    return redirect("/")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Jesteś zalogowany jako {username}")
                return redirect('/')
            else:
                messages.error(request, "Zły login lub hasło.")
        else:
            messages.error(request, "Zły login lub hasło.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="Ask_IT/logowanie.html",
                  context={"form": form})


def rejestracja(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="Ask_IT/rejestracja.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="Ask_IT/rejestracja.html",
                  context={"form": form})


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

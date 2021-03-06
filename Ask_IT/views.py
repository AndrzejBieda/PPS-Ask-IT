from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from Ask_IT.models import Category
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from Ask_IT.forms import *
from Ask_IT.models import *


def index(request):
    return render(request, 'Ask_IT/index.html',
                  {"questions": Question.objects.all()})


def user(request, username):
    if username:
        user = get_object_or_404(User, username=username)
        questions = Question.objects.filter(author=user)
    context = {'user': user, 'questions': questions}
    return render(request, 'Ask_IT/user.html', context)


def kategorie(request):
    return render(request, 'Ask_IT/kategorie.html',
                  {"categories": Category.objects.all()})


def pytanie(request, id):
    if request.method == 'POST' and 'best_answer_button' in request.POST:

        questionfromform = get_object_or_404(Question, pk=request.POST.get('question'))
        answerfromform = get_object_or_404(Answer, pk=request.POST.get('answer'))

        a = BestAnswer(question=questionfromform, answer=answerfromform)

        if BestAnswer.objects.filter(question=questionfromform):
            b = BestAnswer.objects.filter(question=questionfromform)
            b.update(answer=a.answer)

            user_sub_rep = UserAdditional.objects.filter(user=b[0].answer.author)
            user_sub_rep.update(reputation=a.answer.author.profile.reputation - 1)

            user_add_add = UserAdditional.objects.filter(user=a.answer.author)
            user_add_add.update(reputation=a.answer.author.profile.reputation + 1)

        else:
            a.save()

            user_add_rep = UserAdditional.objects.filter(user=a.answer.author)
            user_add_rep.update(reputation=a.answer.author.profile.reputation + 1)

        strid = str(questionfromform.id)
        return redirect('/pytanie/' + strid)

    if request.method == 'POST':
        form = AnswerContent(request.POST)
        if form.is_valid():
            contentfromform = form.cleaned_data.get('content')
            authorfromform = User.objects.get(username=request.user.username)
            datefromform = datetime.datetime.now()
            questionfromform = get_object_or_404(Question, pk=request.POST.get('question'))
            a = Answer(content=contentfromform, author=authorfromform, date=datefromform, question=questionfromform)
            a.save()
            if LastAnswer.objects.filter(question=questionfromform):
                last = LastAnswer.objects.filter(question=questionfromform)
                last.update(answer=a)
            else:
                LastAnswer(question=questionfromform, answer=a).save()

            questionfromform.numberOfResponses = questionfromform.numberOfResponses + 1
            questionfromform.save()
            strid = str(questionfromform.id)
            return redirect('/pytanie/' + strid)
    else:
        form = AnswerContent()
        question = Question.objects.get(id=id)
        answers = Answer.objects.filter(question=question)
        return render(request, 'Ask_IT/pytanie.html',
                      {"form": form,
                       "question": question,
                       "answers": answers,
                       })


def question(request):
    if request.user.is_authenticated:
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
            return render(request, 'Ask_IT/nowe-pytanie.html', {"form": form, "categories": Category.objects.all()})
    else:
        return redirect('../logowanie')


def categoryThreads(request, name):
    if name:
        category = get_object_or_404(Category, name=name)
        questions = Question.objects.filter(category=category)
    context = {'category': category, 'questions': questions}
    return render(request, 'Ask_IT/kategoria-watki.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowano!")
    return redirect("/")


def login_request(request):
    if request.user.is_authenticated:
        return redirect('..')
    else:
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
    if request.user.is_authenticated:
        return redirect('..')
    else:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"New account created: {username}")
                login(request, user)
                useradd = UserAdditional(user=user)
                useradd.save()
                return redirect("..")

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

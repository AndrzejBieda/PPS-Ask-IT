from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from Ask_IT.models import Category


def index(request):
    return render(request, 'Ask_IT/index.html')


def kategorie(request):
    return render(request, 'Ask_IT/kategorie.html',
                  {"categories": Category.objects.all()})

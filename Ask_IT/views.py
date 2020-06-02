from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

# def homepage(response):
#     return render(request=cos, template_name="base.html")

def base(request):
    return render(request, "base.html")

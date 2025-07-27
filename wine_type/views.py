from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the wine_type index.")

"""
def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render("", request))
"""
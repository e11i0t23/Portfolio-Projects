from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req, "project_0_search/index.html")

def image(req):
    return render(req, "project_0_search/image.html")

def advanced(req):
    return render(req, "project_0_search/advanced.html")

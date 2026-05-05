from django.shortcuts import render


def home(request):
    return render(request, "static_pages/home.html")

def about(request):
    return render(request, "static_pages/about.html")

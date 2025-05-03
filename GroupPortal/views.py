from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def contacts(request):
    return render(request, 'contacts.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    return render(request, 'dashboard.html')


def create(request):
    return render(request, "create_template.html")
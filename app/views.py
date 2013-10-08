from django.shortcuts import get_object_or_404, render
# Create your views here.

def home(request):
    return render(request, 'app/home.html', {"active": "home"})

def about(request):
    return render(request, 'app/about.html', {"active": "about"})

def deals(request):
    return render(request, 'app/deals.html', {"active": "deals"})

def resources(request):
    return render(request, 'app/resources.html', {"active": "resources"})

def legal(request):
    #passing the active value, even tho it is not being used
    return render(request, 'app/legal.html', {"active": "legal"}) 


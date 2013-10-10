from django.shortcuts import get_object_or_404, render

from events.models import Event

def home(request):
    upcoming = Event.objects.upcoming()[:3]
    return render(request, 'app/home.html', {"active": "home", "upcoming": upcoming})

def about(request):
    return render(request, 'app/about.html', {"active": "about"})

def deals(request):
    return render(request, 'app/deals.html', {"active": "deals"})

def resources(request):
    return render(request, 'app/resources.html', {"active": "resources"})

def legal(request):
    #passing the active value, even tho it is not being used
    return render(request, 'app/legal.html', {"active": "legal"})

def contact(request):
    return render(request, 'app/contact.html', {'active': 'contact'})

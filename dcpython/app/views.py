from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from dcpython.app.integration.meetup import get_upcoming_events


# Create your views here.

@cache_page(3600)  # Cache API results for one hour
def home(request):
    upcoming = get_upcoming_events(count=3)
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

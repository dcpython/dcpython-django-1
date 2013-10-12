from django.shortcuts import get_object_or_404, render

from dcpython.events.models import Event

def home(request):
    upcoming = Event.objects.upcoming()[:3]
    return render(request, 'app/home.html', {"upcoming": upcoming})

def about(request):
    return render(request, 'app/about.html')

def deals(request):
    return render(request, 'app/deals.html')

def resources(request):
    return render(request, 'app/resources.html')

def legal(request):
    return render(request, 'app/legal.html')

def contact(request):
    return render(request, 'app/contact.html')

#from django.shortcuts import get_object_or_404, render
#from dcpython.support.models import Donor
#from dcpython.events.models import Event
#from dcpython.blog.models import Post
#from django.conf import settings
#
#def home(request):
#    upcoming = Event.objects.upcoming()[:3]
#    donor = Donor.objects.random()
#    posts = Post.objects.published()[:3]
#    return render(request, 'app/home.html', {"upcoming": upcoming, "posts": posts, "donor": donor, "donor_level": donor.get_level()[1] if donor else None, 'GOOGLE_VERIFICATION_ID': settings.GOOGLE_VERIFICATION_ID})
#
#def about(request):
#    return render(request, 'app/about.html')
#
#def deals(request):
#    return render(request, 'app/deals.html')
#
#def resources(request):
#    return render(request, 'app/resources.html')
#
#def legal(request):
#    return render(request, 'app/legal.html')
#
#def contact(request):
#    return render(request, 'app/contact.html')


from django.shortcuts import render


def home(request):
    return render(request, 'app/home.html')

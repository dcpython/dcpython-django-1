from django.shortcuts import render


def andrew_w_singer(request):
    return render(request, 'app/andrew-w-singer.html')


def donate(request):
    return render(request, 'app/donate.html')


def home(request):
    # return render(request, 'app/home.html', {"upcoming": upcoming, "posts":
    # posts, "donor": donor, "donor_level": donor.get_level()[1] if donor
    # else None, 'GOOGLE_VERIFICATION_ID': settings.GOOGLE_VERIFICATION_ID})
    return render(request, 'app/home.html')

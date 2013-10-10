# encoding: utf-8

from django.shortcuts import render
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DateDetailView

from .models import Event


def event_list(request):
    upcoming = Event.objects.upcoming()
    past = Event.objects.past()
    years = Event.objects.dates('start_time', 'year', order="DESC")

    ctx = {"upcoming": upcoming,
           "past": past,
           # Used for navigation styling:
           "active": "events",
           'archive_years': years}

    return render(request, 'events/event_list.html', ctx)


class EventYearArchiveView(YearArchiveView):
    queryset = Event.objects.all()
    date_field = "start_time"
    make_object_list = True
    allow_future = True


class EventMonthArchiveView(MonthArchiveView):
    queryset = Event.objects.all()
    date_field = "start_time"
    make_object_list = True
    allow_future = True


class EventDetail(DateDetailView):
    queryset = Event.objects.all()
    date_field = "start_time"
    month_format = '%m'
    allow_future = True

    def get_object(self, queryset=None):
        qs = queryset if queryset is not None else self.get_queryset()

        return qs.get(slug=self.kwargs['slug'],
                      start_time__year=self.kwargs['year'],
                      start_time__month=self.kwargs['month'],
                      start_time__day=self.kwargs['day'])

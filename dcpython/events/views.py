# encoding: utf-8

from dcpython.events.models import Event
from django.shortcuts import render
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DateDetailView


def event_list(request):
    upcoming = Event.objects.upcoming()
    past = Event.objects.past()
    years = Event.objects.datetimes('start_time', 'year', order="DESC")

    ctx = {"upcoming": upcoming,
           "past": past,
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


class SlideShow(EventDetail):
    #FIXME this is not a pretty looking class ;P
    template_name = 'events/slideshow.html'

    def get_context_data(self, **kwargs):
        ctx = super(EventDetail, self).get_context_data(**kwargs)
        talks = ctx['object'].description.strip().split("-" * 5)

        t = []
        for talk in talks:
            formatted = talk.replace("<p>", "").replace("</p>", "\n").split("\n")
            t.append({"title": formatted[0], "description": "\n".join(formatted[1:])})

        ctx['talks'] = t
        return ctx

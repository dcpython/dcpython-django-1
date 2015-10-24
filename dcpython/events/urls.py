# encoding: utf-8
from __future__ import absolute_import
from django.conf.urls import patterns, url

from dcpython.events.views import EventYearArchiveView, EventMonthArchiveView, EventDetail

urlpatterns = patterns(
    'dcpython.events.views',
    url(r'^$',
        'event_list',
        name='event-list'),
    url(r'^(?P<year>\d{4})/$',
        EventYearArchiveView.as_view(),
        name="event-year-archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        EventMonthArchiveView.as_view(month_format='%m'),
        name="event-month-archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]+)/$',
        EventDetail.as_view(),
        name="event-detail"), )

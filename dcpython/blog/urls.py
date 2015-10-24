# encoding: utf-8
from __future__ import absolute_import
from dcpython.blog.rss import BlogFeed
from django.conf.urls import patterns, url
from dcpython.blog.views import PostYearArchiveView, PostMonthArchiveView, PostDetail

urlpatterns = patterns(
    'dcpython.blog.views',
    url(r'^$',
        'blog',
        name='blog'),
    url(r'^(?P<year>\d{4})/$',
        PostYearArchiveView.as_view(),
        name="post-year-archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        PostMonthArchiveView.as_view(month_format='%m'),
        name="post-month-archive"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]+)/$',
        PostDetail.as_view(),
        name="post-detail"),
    url(r'^feed/$', BlogFeed()))

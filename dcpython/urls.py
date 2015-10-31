"""dcpython URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from dcpython import views

urlpatterns = [
    url(r'^$',
        views.home,
        name='home'),
    url(r'^about$',
        views.about,
        name='about'),
    url(r'^andrew-w-singer$',
        views.andrew_w_singer,
        name='andrew_w_singer'),
    url(r'^donate$',
        views.donate,
        name='donate'),
    url(r'^admin/', include(admin.site.urls)),
    #    url(r'^(?P<year>\d{4})/$',
    #        views.EventYearArchiveView.as_view(),
    #        name="event-year-archive"),
    #    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
    #        views.EventMonthArchiveView.as_view(month_format='%m'),
    #        name="event-month-archive"),
    #    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/' +
    #        '(?P<slug>[^/]+)/$',
    #        views.EventDetail.as_view(),
    #        name="event-detail"), )
]

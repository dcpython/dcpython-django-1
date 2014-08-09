# encoding: utf-8
from __future__ import absolute_import
from django.conf.urls import patterns, url

urlpatterns = patterns('dcpython.events.views',
    url(r'^donate/$', 'dcpython.support.views.support', name='support'),
    url(r'^donate/andrew-w-singer.html', 'dcpython.support.views.andrew_w_singer', name='andrew_w_singer'),
    url(r'^donate/donor/(?P<secret>[\w\-_]+=?=?=?)/$', 'dcpython.support.views.donor_update', name='donor_update'),
    url(r'^donate/make_donation$', 'dcpython.support.views.make_donation', name='make_donation'),
)
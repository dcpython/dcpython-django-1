# encoding: utf-8
from __future__ import absolute_import
from django.conf.urls import patterns, url

urlpatterns = patterns('dcpython.donate.views',
    url(r'^$', 'donate', name='donate'),
    url(r'^donate/andrew-w-singer.html', 'dcpython.donate.views.andrew_w_singer', name='andrew_w_singer'),
    url(r'^donate/donor/(?P<secret>[\w\-_]+=?=?=?)/$', 'dcpython.donate.views.donor_update', name='donor_update'),
    url(r'^donate/make_donation$', 'dcpython.donate.views.make_donation', name='make_donation'),
)

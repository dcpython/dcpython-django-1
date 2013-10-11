from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dcpython.app.views.home', name='home'),
    url(r'^events$', 'dcpython.events.views.events', name='events'),
    url(r'^donate$', 'dcpython.support.views.support', name='support'),
    url(r'^donor/(?P<secret>[\w\-_]+=?=?=?)$', 'dcpython.support.views.donor_update', name='donor_update'),
    url(r'^make_donation$', 'dcpython.support.views.make_donation', name='make_donation'),
    url(r'^about$', 'dcpython.app.views.about', name='about'),
    url(r'^deals$', 'dcpython.app.views.deals', name='deals'),
    url(r'^resources$', 'dcpython.app.views.resources', name='resources'),
    url(r'^legal$', 'dcpython.app.views.legal', name='legal'),
    url(r'^contact$', 'dcpython.app.views.contact', name='contact'),
    # url(r'^$', 'dcpython.views.home', name='home'),
    # url(r'^dcpython/', include('dcpython.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

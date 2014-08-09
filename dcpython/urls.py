from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urls = ()

urlpatterns = patterns('dcpython',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^events/', include('events.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^donate/', include('donate.urls')),
    url(r'^about/$', 'app.views.about', name='about'),
    url(r'^deals/$', 'app.views.deals', name='deals'),
    url(r'^resources/$', 'app.views.resources', name='resources'),
    url(r'^legal/$', 'app.views.legal', name='legal'),
    url(r'^contact/$', 'app.views.contact', name='contact'),

    # url(r'^$', 'dcpython.views.home', name='home'),
    # url(r'^dcpython/', include('dcpython.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

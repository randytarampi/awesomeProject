from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

# Dajax/Dajaxice configuration
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'awesomeProject.views.home', name='home'),
    # url(r'^awesomeProject/', include('awesomeProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Dajax/Dajaxice URLs
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Favicon & robots.txt
    url(r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^favicon\.ico$', redirect_to, {'url': '/static/favicon.ico'}),

    # Project URLs
    url(r'^', include('scheduler.urls')),
    url(r'^about/', include('about.urls')),
)

urlpatterns += staticfiles_urlpatterns()

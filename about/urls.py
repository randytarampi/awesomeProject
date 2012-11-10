from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('about.views',
    url(r'^$', 'index', name = "about_index"),
    url(r'^acknowledgements/', 'acknowledgements', name = "about_acknowledgements"),
    url(r'^legal/', 'legal', name = "about_legal"),
    url(r'^team/', 'team', name = "about_team"),
)

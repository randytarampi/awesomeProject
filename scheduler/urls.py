from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('scheduler.views',
    url(r'^$', 'index', name = "scheduler_index"),
    url(r'^instructions/', 'instructions', name = "scheduler_instructions"),
    url(r'^examples/', 'examples', name = "scheduler_examples"),
    url(r'^infoSubmit/', 'infoSubmit', name = "scheduler_infoSubmit"),
)

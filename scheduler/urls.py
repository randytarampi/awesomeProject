from django.conf.urls.defaults import *
from django.views.generic import *
from scheduler.models import *
from scheduler.views import *

urlpatterns = patterns('scheduler.views',
    url(r'^$', 'index', name = "scheduler_index"),
    url(r'^instructions/$', 'instructions', name = "scheduler_instructions"),
    url(r'^examples/$', 'examples', name = "scheduler_examples"),
    url(r'^instructors/$', instructorListView.as_view(), name = "scheduler_instructors"),
    url(r'^instructors/(?P<pk>[ \w\s]+)/$', instructorDetailView.as_view(), name = "scheduler_instructor"),
    url(r'^courses/$', courseListView.as_view(), name = "scheduler_courses"),
    url(r'^courses/(?P<subject>[A-Z]+)/$', courseSubjectListView.as_view(), name = "scheduler_coursesSubject"),
    url(r'^courses/(?P<subject>[A-Z]+)/(?P<number>[X]?[X]?[0-9]+[A-Z]?)/$', courseSubjectNumberListView.as_view(), name = "scheduler_coursesSubjectNumber"),
    url(r'^courses/(?P<pk>\d+)/$', courseDetailView.as_view(), name = "scheduler_course"),
)

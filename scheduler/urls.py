from django.conf.urls.defaults import *
from django.views.generic import *
from scheduler.models import *

urlpatterns = patterns('scheduler.views',
    url(r'^$', 'index', name = "scheduler_index"),
    url(r'^instructions/$', 'instructions', name = "scheduler_instructions"),
    url(r'^examples/$', 'examples', name = "scheduler_examples"),
    url(r'^instructors/$', 'instructors', name = "scheduler_instructors"),
    url(r'^instructors/(?P<pk>[ \w\s]+)/$', DetailView.as_view(model=Instructor, template_name='schedulerInstructor.html'), name = "scheduler_instructor"),
    url(r'^courses/$', 'courses', name = "scheduler_courses"),
    url(r'^courses/(?P<pk>\d+)/$', DetailView.as_view(model=Course, template_name='schedulerCourse.html'), name = "scheduler_course"),
)

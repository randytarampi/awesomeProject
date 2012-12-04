from django.conf.urls.defaults import *
from django.views.generic import *
from scheduler.models import *
from scheduler.views import *

urlpatterns = patterns('scheduler.views',
    url(r'^$', 'index', name = "scheduler_index"),
    url(r'^instructions/$', 'instructions', name = "scheduler_instructions"),
    url(r'^examples/$', 'examples', name = "scheduler_examples"),
    url(r'^instructors/$', ListView.as_view(queryset=Instructor.objects.order_by('last_name', 'first_name').exclude(first_name__startswith="."), context_object_name='instructors', template_name='schedulerInstructors.html'), name = "scheduler_instructors"),
    url(r'^instructors/(?P<pk>[ \w\s]+)/$', DetailView.as_view(model=Instructor, template_name='schedulerInstructor.html'), name = "scheduler_instructor"),
    url(r'^courses/$', ListView.as_view(queryset=Course.objects.order_by('subject').values('subject', 'number', 'title').distinct(), context_object_name='courses', template_name='schedulerCourses.html'), name = "scheduler_courses"),
    url(r'^courses/(?P<subject>[A-Z]+)/$', courseSubjectListView.as_view(), name = "scheduler_coursesSubject"),
    url(r'^courses/(?P<subject>[A-Z]+)/(?P<number>[X]?[X]?[0-9]+[A-Z]?)/$', courseSubjectNumberListView.as_view(), name = "scheduler_coursesSubjectNumber"),
    url(r'^courses/(?P<pk>\d+)/$', courseDetailView.as_view(), name = "scheduler_course"),
)

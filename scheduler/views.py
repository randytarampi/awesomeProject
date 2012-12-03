from django.shortcuts import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import *
from scheduler.models import *

def index(request):
	allSubjects = Course.objects.values_list('subject', flat=True).distinct()

	# Using the 0-th element so that any set of data will give the first element. This is using the same query as in ajax.py
	firstSubject = allSubjects[0]
	initialNumbers = Course.objects.filter(subject=firstSubject).values_list('number', flat=True).distinct()

	# More initial values, w.r.t. instructor form this time 	
	c = Course.objects.filter(subject=firstSubject)
	initialProfs = Instructor.objects.filter(course__in=c).order_by('last_name').distinct()

	instructorsCourses = []
	d = Instructor.objects.filter(userid=initialProfs[0])
	for i in d:
		for j in i.course.all():
			instructorsCourses.append(j)

	return render_to_response('schedulerIndex.html', { 'subjects': allSubjects, 'initNums': initialNumbers, 'initProfs': initialProfs, 'initNumsByProf': instructorsCourses }, context_instance=RequestContext(request))

def instructions(request):
	return render_to_response('schedulerInstructions.html')

def examples(request):
	return render_to_response('schedulerExamples.html')
    
class SubjectListView(ListView):
	context_object_name = "courses"
	template_name = "schedulerCoursesSubject.html"

	def get_queryset(self):
		return get_list_or_404(Course, subject=self.kwargs['subject'])

	def get_context_data(self, **kwargs):
		context = super(SubjectListView, self).get_context_data(**kwargs)
		context['subject'] = self.kwargs['subject']
		return context

class SubjectNumberListView(ListView):
	context_object_name = "courses"
	template_name = "schedulerCoursesSubjectNumber.html"

	def get_queryset(self):
		return get_list_or_404(Course, subject=self.kwargs['subject'], number=self.kwargs['number'])

	def get_context_data(self, **kwargs):
		context = super(SubjectNumberListView, self).get_context_data(**kwargs)
		context['subject'] = self.kwargs['subject']
		context['number'] = self.kwargs['number']
		return context

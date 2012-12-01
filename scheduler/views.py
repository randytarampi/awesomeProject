from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from scheduler.models import *

def index(request):
	allSubjects = Course.objects.values_list('subject', flat=True).distinct()
	print allSubjects
	return render_to_response('schedulerIndex.html', { 'subjects': allSubjects }, context_instance=RequestContext(request))

def instructions(request):
	return render_to_response('schedulerInstructions.html')

def examples(request):
	return render_to_response('schedulerExamples.html')

def instructors(request):
	allInstructors = Instructor.objects.order_by('name')
	return render_to_response('schedulerInstructors.html', { 'instructors': allInstructors })
    
def classes(request):
	allCourses = Course.objects.order_by('subject')
	return render_to_response('schedulerClasses.html', { 'courses': allCourses })

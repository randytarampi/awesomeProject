from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from scheduler.models import *

def index(request):
	allSubjects = Course.objects.values_list('subject', flat=True).distinct()
	firstSubject = allSubjects[0]
	initialNumbers = Course.objects.filter(subject=firstSubject).values_list('number', flat=True).distinct()
	return render_to_response('schedulerIndex.html', { 'subjects': allSubjects, 'initNums': initialNumbers }, context_instance=RequestContext(request))

def instructions(request):
	return render_to_response('schedulerInstructions.html')

def examples(request):
	return render_to_response('schedulerExamples.html')

def instructors(request):
	allInstructors = Instructor.objects.order_by('last_name', 'first_name').exclude(first_name__startswith=".")
	return render_to_response('schedulerInstructors.html', { 'instructors': allInstructors })

def instructor(request, instructorId):
	instructor = get_object_or_404(Instructor, pk=instructorId)
	return render_to_response('schedulerInstructor.html', { 'instructor': instructor })
    
def courses(request):
	allCourses = Course.objects.order_by('subject')
	return render_to_response('schedulerCourses.html', { 'courses': allCourses })

def course(request, courseId):
	course = get_object_or_404(Course, pk=courseId)
	return render_to_response('schedulerCourse.html', { 'course': course })

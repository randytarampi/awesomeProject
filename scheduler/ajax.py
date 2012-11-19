from itertools import chain
from django.shortcuts import get_object_or_404, render_to_response
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from scheduler.models import *
from scheduler.schedulingalg import *

def listOfSubjects():
	allSubjects = Course.objects.values_list('subject', flat=True).distinct()
	datList = []
	# runs through every subject and makes an option for a select tag where value = Subject
	for i in allSubjects:
		datList.append("<option value='%s'>%s</option>" % (i, i))
	return ''.join(datList)

@dajaxice_register
def generateSchedule(request, form):
	dajax = Dajax()
	dajax.clear('#scheduleViewDiv', 'innerHTML')
	
	# Get the data
	optimalCourses = functionForRandy(4, list(chain(Course.objects.filter(subject="CMPT", number__gte=400, number__lte=470), Course.objects.filter(subject="POL", number__gte=410, number__lte=470))))
	optimalInstructors = Instructor.objects.filter(course__in = optimalCourses)
	optimalMeetingTimes = MeetingTime.objects.filter(course__in = optimalCourses)
	optimalData = {'optimalCourses': optimalCourses, 'optimalInstructors': optimalInstructors, 'optimalMeetingTimes': optimalMeetingTimes}
	
	# Serve the data
	scheduleInfo = render_to_response('schedulerSchedule.html', optimalData).content
	dajax.assign('#scheduleViewDiv', 'innerHTML', scheduleInfo)
	return dajax.json()

@dajaxice_register
def listOfNumbers(request, option, idNum):
	dajax = Dajax()
	out = []

	daList = Course.objects.filter(subject=option).values_list('number', flat=True)
	for i in daList:
		out.append("<option value='%s'>%s</option>" % (i, i))

	dajax.assign(idNum, 'innerHTML', ''.join(out))	
	return dajax.json()

@dajaxice_register
def updatingCourseForm(request, option):
	dajax = Dajax()

	out = []
	# several select tags are made, each with a complete list of subjects with value = 1 through aClass
	for aClass in range(1, int(option)+1):
		out.append('<div>Course %s: <select id="courseSubject%s" onchange="Dajaxice.scheduler.listOfNumbers(Dajax.process, {\'option\':this.value, \'idNum\':\'#courseNumber%s\'})">%s</select> &nbsp<select id="courseNumber%s"></select></div>' % (str(aClass), str(aClass), str(aClass), listOfSubjects(), str(aClass)))

	dajax.assign('#listClasses', 'innerHTML', ''.join(out))
	return dajax.json()


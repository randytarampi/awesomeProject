import json
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
	selectedCourses = Course.objects.none()
	numClasses =  int(form['numTaking'])
	for i in range(numClasses):
		selectedCourses = selectedCourses | Course.objects.filter(subject=form['courseSubject%i' % (i+1)], number=form['courseNumber%i' % (i+1)])

	# Process the data
	optimalCourses = functionForRandy(numClasses, selectedCourses)[0]
	optimalInstructors = Instructor.objects.filter(course__in = optimalCourses)
	optimalLectureTimes = MeetingTime.objects.filter(course__in = optimalCourses, type="LEC")
	optimalLabTimes = MeetingTime.objects.filter(course__in = optimalCourses, type="LAB")
	optimalTestTimes = MeetingTime.objects.filter(course__in = optimalCourses, type="EXAM") | MeetingTime.objects.filter(course__in = optimalCourses, type="MIDT")
	optimalData = {'optimalCourses': optimalCourses, 'optimalInstructors': optimalInstructors, 'optimalLectureTimes': optimalLectureTimes, 'optimalLabTimes': optimalLabTimes, 'optimalTestTimes': optimalTestTimes}
	
	# Serve the data
	scheduleInfo = render_to_response('schedulerSchedule.html', optimalData).content
	dajax.assign('#scheduleViewDiv', 'innerHTML', scheduleInfo)
	return dajax.json()

@dajaxice_register
def listOfNumbers(request, option, idNum):
	dajax = Dajax()
	out = []

	daList = Course.objects.filter(subject=option).values_list('number', flat=True).distinct()
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
		out.append('<div>Course %s: <select id="courseSubject%s" name="courseSubject%s" onchange="Dajaxice.scheduler.listOfNumbers(Dajax.process, {\'option\':this.value, \'idNum\':\'#courseNumber%s\'})">%s</select> &nbsp<select id="courseNumber%s" name="courseNumber%s"></select></div>' % (str(aClass), str(aClass), str(aClass), str(aClass), listOfSubjects(), str(aClass), str(aClass)))

	moreOut = []
	#more stuff to render to the template. This renders the select tag before options are added to it.
	moreOut.append("Of these considered classes, how many would you like to take?<select id=\"numTaking\" name=\"numTaking\" onchange=\"\" size=\"1\"></select>")
	dajax.assign('#numTakingSpan', 'innerHTML', ''.join(moreOut))

	theList = []
	#adds the options to the select tag rendered previously
	for i in range(1, int(option)+1):
		theList.append("<option value='%s'>%s</option>" % (i, i))

	dajax.assign('#listClasses', 'innerHTML', ''.join(out))
	dajax.assign('#numTaking', 'innerHTML', ''.join(theList))
	return dajax.json()


from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from scheduler.models import *
from scheduler.views import *
from scheduler.algorithm import *


def listOfDays():
	listOfDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
	outString = []
	for i in range(0, len(listOfDays)):
		outString.append("<option value='%s'>%s</option>" % (str(i), listOfDays[i]))
	return ''.join(outString)

def listOfStarts():
	listOfStarts = []
	outString = []
	for i in range(8, 22):
		i = i % 12
		if i == 0:
			i = 12
		j = str(i)
		j+=':30'
		listOfStarts.append(j)
	for i in range(0, len(listOfStarts)):
		outString.append("<option value='%s'>%s</option>" % (str(i), listOfStarts[i]))
	return ''.join(outString)

def listOfEnds():
	listOfEnds = []
	outString = []
	for i in range(9, 23):
		i = i % 12
		if i == 0:
			i = 12
		j = str(i)
		j+=':20'
		listOfEnds.append(j)
	for i in range(0, len(listOfEnds)):
		outString.append("<option value='%s'>%s</option>" % (str(i), listOfEnds[i]))
	return ''.join(outString)

def listOfSubjects():
	allSubjects = Course.objects.values_list('subject', flat=True).distinct()
	datList = []
	# runs through every subject and makes an option for a select tag where value = Subject
	for i in allSubjects:
		datList.append("<option value='%s'>%s</option>" % (i, i))
	return ''.join(datList)

@dajaxice_register
def getUnavailability(request):
	dajax = Dajax()

	out = []
	i = 1
	out.append('<div>Period of Unavailability %s: <select id="unavailableDay%s" name="unavailableDay%s">%s</select> at <select id="unavailableStart%s" name="unavailableStart%s">%s</select> to <select id="unavailableEnd%s" name="unavailableEnd%s">%s</select></div>' % (str(i), str(i), str(i), listOfDays(), str(i), str(i),listOfStarts(), str(i), str(i), listOfEnds()))
	dajax.assign('#unavailable', 'innerHTML', ''.join(out))
	return dajax.json()

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
	#warning this will now filter out distance ed coures
	processedCourses = createOptimalSchedule(numClasses, selectedCourses, True)
	
	optimalCourses = processedCourses[0]
	optimalInstructors = Instructor.objects.filter(course__in = optimalCourses)	
	optimalMeetingTimes = MeetingTime.objects.filter(course__in = optimalCourses).order_by('type')
	
	rejectedCourses = processedCourses[1]
	rejectedInstructors = Instructor.objects.filter(course__in = rejectedCourses)	
	rejectedMeetingTimes = MeetingTime.objects.filter(course__in = rejectedCourses).order_by('type')
	
	processedData = {'optimalCourses': optimalCourses, 'optimalInstructors': optimalInstructors, 'optimalMeetingTimes': optimalMeetingTimes, 'rejectedCourses': rejectedCourses, 'rejectedInstructors': rejectedInstructors, 'rejectedMeetingTimes': rejectedMeetingTimes}
	
	# Serve the data
	scheduleInfo = render_to_response('schedulerSchedule.html', processedData).content
	dajax.assign('#scheduleViewDiv', 'innerHTML', scheduleInfo)
	dajax.assign('#scheduleViewWeek', 'innerHTML', "You'll see a weekly calendar here")
	dajax.assign('#scheduleViewExams', 'innerHTML', "You'll see at least one monthly calendar here")
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
	moreOut.append('Of these considered classes, how many would you like to take?<select id="numTaking" name="numTaking" onchange="Dajaxice.scheduler.getUnavailability(Dajax.process)" size="1"></select>')
	dajax.assign('#numTakingSpan', 'innerHTML', ''.join(moreOut))

	theList = []
	#adds the options to the select tag rendered previously
	for i in range(1, int(option)+1):
		theList.append("<option value='%s'>%s</option>" % (i, i))

	dajax.assign('#listClasses', 'innerHTML', ''.join(out))
	dajax.assign('#numTaking', 'innerHTML', ''.join(theList))
	return dajax.json()


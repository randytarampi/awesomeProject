from datetime import time
from django.db.models import Q
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from scheduler.models import *
from scheduler.views import *
from scheduler.algorithm import *

SCHEDULE_TIMES = (
	(time(8, 0), "8:00AM"),
	(time(9, 0), "9:00AM"),
	(time(10, 0), "10:00AM"),
	(time(11, 0), "11:00AM"),
	(time(12, 0), "12:00AM"),
	(time(13, 0), "1:00PM"),
	(time(14, 0), "2:00PM"),
	(time(15, 0), "3:00PM"),
	(time(16, 0), "4:00PM"),
	(time(17, 0), "5:00PM"),
	(time(18, 0), "6:00PM"),
	(time(19, 0), "7:00PM"),
	(time(20, 0), "8:00PM"),
	(time(21, 0), "9:00PM"),
	(time(22, 0), "10:00PM"),
)

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

def weeklySchedule(meetingTimes):
	out = []
	
	meetingTimes = MeetingTime.objects.filter(course__in = Course.objects.filter(subject="POL", number=358).order_by('start_time') | Course.objects.filter(subject="POL", number="457W")).order_by('start_time')
	
	for time in SCHEDULE_TIMES:
		timeObj = time[0]
		timeStr = time[1]
	
		# First Row (Hour)
		out.append("<tr><th rowspan='2'>%s</th>" % timeStr)
		
		for day in range(6):
			for meeting in meetingTimes:
				rowCount = 0
				meetingCount = 0
				if meeting.weekday == day:
					if meeting.start_time == timeObj:
						# Accomodate the meeting time by incrementing the rowCount and testTime while testTime <= meeting.end_time
						testTime = timeObj
						while meeting.end_time > testTime:
							try: 
								testTime = testTime.replace(minute=testTime.minute+30)
							except ValueError: 
								testTime = testTime.replace(hour=testTime.hour+1, minute=0)
							rowCount += 1
						out.append("<td rowspan='%i'>%s - %s to %s</td>" % (rowCount, meeting.course, meeting.start_time, meeting.end_time))
						rowCount = 0
						break
					elif meeting.start_time < timeObj and timeObj <= meeting.end_time:
						break
			
			else:
				# Blank space
				out.append("<td>FUCK</td>")

		out.append("</tr>")
		
		# Second Row
		timeObj = timeObj.replace(minute=timeObj.minute+30)
		out.append("<tr>")
		
		for day in range(6):
			for meeting in meetingTimes:
				rowCount = 0
				meetingCount = 0
				if meeting.weekday == day:
					if meeting.start_time == timeObj:
						# Accomodate the meeting time by incrementing the rowCount and testTime while testTime <= meeting.end_time
						testTime = timeObj
						while meeting.end_time > testTime:
							try: 
								testTime = testTime.replace(minute=testTime.minute+30)
							except ValueError: 
								testTime = testTime.replace(hour=testTime.hour+1, minute=0)
							rowCount += 1
						out.append("<td rowspan='%i'>%s - %s to %s</td>" % (rowCount, meeting.course, meeting.start_time, meeting.end_time))
						rowCount = 0
						break
					elif meeting.start_time < timeObj and timeObj <= meeting.end_time:
						break
			
			else:
				# Blank space
				out.append("<td>FUCK</td>")
		
		out.append("</tr>")
	
	return "".join(out)

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
	optimalMeetingTimes = MeetingTime.objects.filter(course__in = optimalCourses).order_by('type', 'start_day', 'start_time')
	optimalExamTimes = optimalMeetingTimes.filter(Q(type="EXAM") | Q(type="MIDT"))
	
	rejectedCourses = processedCourses[1]
	rejectedInstructors = Instructor.objects.filter(course__in = rejectedCourses)	
	rejectedMeetingTimes = MeetingTime.objects.filter(course__in = rejectedCourses).order_by('type', 'start_day', 'start_time')
	
	processedData = {'optimalCourses': optimalCourses, 'optimalInstructors': optimalInstructors, 'optimalMeetingTimes': optimalMeetingTimes, 'optimalExamTimes': optimalExamTimes, 'rejectedCourses': rejectedCourses, 'rejectedInstructors': rejectedInstructors, 'rejectedMeetingTimes': rejectedMeetingTimes}
	
	# Serve the data
	dajax.assign('#scheduleViewDiv', 'innerHTML', render_to_response('schedulerSchedule.html', processedData).content)
	dajax.assign('#scheduleTableBody', 'innerHTML', weeklySchedule(optimalMeetingTimes))
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


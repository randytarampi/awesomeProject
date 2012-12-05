from datetime import time
from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext
from django.db.models import Q
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from scheduler.models import *
from scheduler.algorithm import *

def hourIsAMorPM(h):
	if h >= 12:
		out = "p.m."
	else:
		out = "a.m."
	return out

def changeFrom24To12(h):
	out = h % 12
	if out == 0:
		out = 12
	return out

@dajaxice_register
def amORpmStart(request, option):
	dajax = Dajax()

	if int(option) >= 12:
		out = "p.m."
	else:
		out = "a.m."
	dajax.assign('#startT', 'innerHTML', out)
	return dajax.json()

@dajaxice_register
def amORpmEnd(request, option):
	dajax = Dajax()

	if int(option) >= 12:
		out = "p.m."
	else:
		out = "a.m."
	dajax.assign('#endT', 'innerHTML', out)
	return dajax.json()

def listOfDays():
	listOfDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
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
def deleteCourseFromSession(request, course, number):
	dajax = Dajax()

	sesList = request.session['byCourse']
	sesList.remove((course, number))
	request.session['byCourse'] = sesList

	out = []
	for i in request.session['byCourse']:
		out.append("<li>%s %s <a onclick=\"Dajaxice.scheduler.deleteCourseFromSession(Dajax.process, { 'course':'%s', 'number':'%s' })\">remove</a></li>" % (i[0], i[1], i[0], i[1]))

	dajax.assign('#addCourseList', 'innerHTML', ''.join(out))

	return dajax.json()

@dajaxice_register
def addCourseToSession(request, form):
	dajax = Dajax()
	sessionList = []
	courseTuple = (form['courseSubject'], form['courseNumber'])

	if 'byCourse' in request.session:
		if courseTuple in request.session['byCourse']:
			dajax.alert('You have already selected %s %s!' % courseTuple)
			return dajax.json()
		sessionList = request.session['byCourse']
		sessionList.append(courseTuple)
	else:
		sessionList.append(courseTuple)
	request.session['byCourse'] = sessionList

	out = []
	for i in request.session['byCourse']:
		out.append("<li>%s %s <a onclick=\"Dajaxice.scheduler.deleteCourseFromSession(Dajax.process, { 'course':'%s', 'number':'%s' })\">remove</a></li>" % (i[0], i[1], i[0], i[1]))

	dajax.assign('#addCourseList', 'innerHTML', ''.join(out))

	return dajax.json()

@dajaxice_register
def deleteCourseByProfFromSession(request, course, prof, number):
	dajax = Dajax()

	sesList = request.session['byProf']
	sesList.remove((course, prof, number))
	request.session['byProf'] = sesList

	out = []
	for i in request.session['byProf']:
		out.append("<li>%s %s taught by: %s <a onclick=\"Dajaxice.scheduler.deleteCourseByProfFromSession(Dajax.process, { 'course':'%s', 'prof':'%s', 'number':'%s' })\">remove</a></li>" % (i[0], i[2], i[1], i[0], i[1], i[2]))

	dajax.assign('#addCourseByProfList', 'innerHTML', ''.join(out))

	return dajax.json()

@dajaxice_register
def addCourseByProfToSession(request, form):
	dajax = Dajax()
	sessionList = []
	courseTuple = (form['courseSubjectByProf'], form['subjectProfs'], form['courseNumberByProf'])
	
	if 'byProf' in request.session:
		if courseTuple in request.session['byProf']:
			dajax.alert('You have already selected %s %s! with %s' % (courseTuple[0], courseTuple[2], courseTuple[1]))
			return dajax.json()
		sessionList = request.session['byProf']
		sessionList.append(courseTuple)
	else:
		sessionList.append(courseTuple)
	request.session['byProf'] = sessionList

	out = []
	for i in request.session['byProf']:
		out.append("<li>%s %s taught by: %s <a onclick=\"Dajaxice.scheduler.deleteCourseByProfFromSession(Dajax.process, { 'course':'%s', 'prof':'%s', 'number':'%s' })\">remove</a></li>" % (i[0], i[2], i[1], i[0], i[1], i[2]))

	dajax.assign('#addCourseByProfList', 'innerHTML', ''.join(out))

	return dajax.json()

@dajaxice_register
def deleteUnavailableFromSession(request, day, startMinute, startHour, endMinute, endHour):
	dajax = Dajax()

	listOfDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	t1 = time(int(startHour), int(startMinute))
	t2 = time(int(endHour), int(endMinute))
	sesList = request.session['timesUnavailable']
	sesList.remove((int(day), t1, t2))
	request.session['timesUnavailable'] = sesList

	out = []
	for i in request.session['timesUnavailable']:

		if int(i[1].minute) < 10:
			firstMinute = str(i[1].minute) + '0'
		else:
			firstMinute = str(i[1].minute)
		if int(i[2].minute) < 10:
			lastMinute = str(i[2].minute) + '0'
		else:
			lastMinute = str(i[2].minute)

		out.append("<li>%s from %s:%s %s to %s:%s %s <a onclick=\"Dajaxice.scheduler.deleteUnavailableFromSession(Dajax.process, { 'day':'%s', 'startMinute':'%s', 'startHour':'%s', 'endMinute':'%s', 'endHour':'%s' })\">remove</a></li>" % (listOfDays[i[0]], changeFrom24To12(i[1].hour), firstMinute, hourIsAMorPM(i[1].hour), changeFrom24To12(i[2].hour), lastMinute, hourIsAMorPM(i[2].hour), i[0], i[1].minute, i[1].hour, i[2].minute, i[2].hour))

	dajax.assign('#addTimeList', 'innerHTML', ''.join(out))

	return dajax.json()

@dajaxice_register
def addUnavailableToSession(request, form):
	dajax = Dajax()
	listOfDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	sessionList = []
	d = int(form['day'])
	t1 = time(int(form['startHour']), int(form['startMinute']))
	t2 = time(int(form['endHour']), int(form['endMinute']))
	timeTuple = (d, t1, t2)
	
	if 'timesUnavailable' in request.session:
		if timeTuple in request.session['timesUnavailable']:
			dajax.alert('You have already marked %s from %i:%s %s to %i:%s %s as unavailable' % (listOfDays[d], changeFrom24To12(int(form['startHour'])), form['startMinute'], hourIsAMorPM(int(form['startHour'])), changeFrom24To12(int(form['endHour'])), form['endMinute'], hourIsAMorPM(int(form['endHour']))))
			return dajax.json()
		sessionList = request.session['timesUnavailable']
		sessionList.append(timeTuple)
	else:
		sessionList.append(timeTuple)
	request.session['timesUnavailable'] = sessionList

	out = []

	for i in request.session['timesUnavailable']:

		if int(i[1].minute) < 10:
			firstMinute = str(i[1].minute) + '0'
		else:
			firstMinute = str(i[1].minute)
		if int(i[2].minute) < 10:
			lastMinute = str(i[2].minute) + '0'
		else:
			lastMinute = str(i[2].minute)

		out.append("<li>%s from %s:%s %s to %s:%s %s <a onclick=\"Dajaxice.scheduler.deleteUnavailableFromSession(Dajax.process, { 'day':'%s', 'startMinute':'%s', 'startHour':'%s', 'endMinute':'%s', 'endHour':'%s' })\">remove</a></li>" % (listOfDays[i[0]], changeFrom24To12(i[1].hour), firstMinute, hourIsAMorPM(i[1].hour), changeFrom24To12(i[2].hour), lastMinute, hourIsAMorPM(i[2].hour), i[0], i[1].minute, i[1].hour, i[2].minute, i[2].hour))

	dajax.assign('#addTimeList', 'innerHTML', ''.join(out))

	return dajax.json()

def weeklyScheduleRows(meetingTimes, time, proposedCourse=None):
	tableRow = []

	for day in range(6):
		for meeting in meetingTimes:
			rowCount = 0
			if meeting.weekday == day:
				if meeting.start_time == time:
					testTime = time
					while meeting.end_time > testTime:
						try: 
							testTime = testTime.replace(minute=testTime.minute+30)
						except ValueError: 
							testTime = testTime.replace(hour=testTime.hour+1, minute=0)
						rowCount += 1
					scheduledOrProposed = "scheduleTableClass" if (meeting.course != proposedCourse) else "scheduleTableProposedClass"
					tableRow.append('\n\t<td rowspan="%i" class="scheduleTableCell %s" id={{ meeting%s.id }}>\n\t\t<span class="classDescription" id={{ meeting%s.id }}>{{ meeting%s.course }}<br />{{ meeting%s.typeChoice }}<br />{{ meeting%s.start_time }} to {{ meeting%s.end_time }}<br />{{ meeting%s.room }}</span></td>' % (rowCount, scheduledOrProposed, meeting.id, meeting.id, meeting.id, meeting.id, meeting.id, meeting.id, meeting.id))
					break
				elif meeting.start_time < time and time <= meeting.end_time:
					break
		else:
			tableRow.append('\n\t<td class="scheduleTableCell">&nbsp;</td>')
	
	return ''.join(tableRow)

def weeklySchedule(scheduledTimes, proposedTimes=[]):
	meetingTimes = scheduledTimes
	meetingTimes.extend(proposedTimes)
	meetingTimes = sorted(meetingTimes, key=lambda meeting: meeting.start_time)
	proposedCourse = proposedTimes[0].course if proposedTimes else None
	meetingTable = []
	meetingContext = {}
	earlyBound = meetingTimes[0].start_time
	lateBound = meetingTimes[len(meetingTimes)-1].end_time
	tableBounds = []
	
	for meeting in meetingTimes:
		meetingContext[('meeting%s' % meeting.id)] = meeting
		earlyBound = meeting.start_time if (meeting.start_time < earlyBound) else earlyBound
		lateBound = meeting.end_time if (meeting.end_time > lateBound) else lateBound
	
	for hour in range(earlyBound.hour, lateBound.hour+1):
		tableBounds.append(time(hour))
	
	for slot in tableBounds:
		meetingContext[('time%s' % slot.hour)] = slot
	
		# First Row (Top of the Hour)
		meetingTable.append('\n<tr class="scheduleTableRow topHour"><th class="scheduleTableTime" rowspan="2">{{ time%s }}</th>' % slot.hour)
		meetingTable.append(weeklyScheduleRows(meetingTimes, slot, proposedCourse))
		meetingTable.append('\n</tr>')
		
		# Second Row (Bottom of the Hour)
		slot = slot.replace(minute=slot.minute+30)
		meetingTable.append('\n<tr class="scheduleTableRow bottomHour">')
		meetingTable.append(weeklyScheduleRows(meetingTimes, slot, proposedCourse))
		meetingTable.append('\n</tr>')
	
	return Template(''.join(meetingTable)).render(Context(meetingContext))

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
	selectedCourses = Course.objects.none()
	timesUnavailable = []

	# Get the data
	numClasses = int(form['numClasses'])
	if 'byCourse' in request.session:
		for courseTuple in request.session['byCourse']:
			selectedCourses = selectedCourses | Course.objects.filter(subject=courseTuple[0], number=courseTuple[1])
	if 'byProf' in request.session:
		for profTuple in request.session['byProf']:
			selectedCourses = selectedCourses | Instructor.objects.get(userid=profTuple[1]).course.filter(subject=profTuple[0], number=profTuple[2])
	if 'timesUnavailable' in request.session:
		for time in request.session['timesUnavailable']:
			timesUnavailable = timesUnavailable.append(time)

	# Process the data
	processedCourses = createOptimalSchedule(numClasses, selectedCourses, timesUnavailable)

	optimalCourses = processedCourses[1]
	optimalInstructors = Instructor.objects.filter(course__in = optimalCourses)	
	optimalMeetingTimes = processedCourses[0]
	optimalExamTimes = MeetingTime.objects.filter(course__in = optimalCourses).filter(Q(type="EXAM") | Q(type="MIDT"))

	rejectedCourses = processedCourses[3]
	rejectedInstructors = Instructor.objects.filter(course__in = rejectedCourses)	
	rejectedMeetingTimes = processedCourses[2]

	processedData = {'optimalCourses': optimalCourses, 'optimalInstructors': optimalInstructors, 'optimalMeetingTimes': optimalMeetingTimes, 'optimalExamTimes': optimalExamTimes, 'rejectedCourses': rejectedCourses, 'rejectedInstructors': rejectedInstructors, 'rejectedMeetingTimes': rejectedMeetingTimes}
	request.session['processedData'] = processedData
	processedData['scheduledHTML'] = weeklySchedule(optimalMeetingTimes)

	# Serve the data
	dajax.assign('#scheduleViewDiv', 'innerHTML', render_to_response('schedulerSchedule.html', processedData).content)
	dajax.script('$(\'#scheduleViewDiv\').activity(false);')
	dajax.script('$(document).ready(jQueryEffects());')
	dajax.remove_css_class('#scheduleViewDiv', 'emptySchedule');
	dajax.add_css_class('#scheduleViewDiv', 'fullSchedule');
	return dajax.json()

@dajaxice_register
def listOfProfs(request, option):
	dajax = Dajax()
	out = []

	c = Course.objects.filter(subject=option)
	d = Instructor.objects.filter(course__in=c).order_by('last_name').distinct()
	for i in d:
		out.append("<option value='%s'>%s</option>" % (i.userid, i.name()))

	dajax.assign('#subjectProfs', 'innerHTML', ''.join(out))
	return dajax.json()

@dajaxice_register
def listOfNumbersByProf(request, option, subj):
	dajax = Dajax()
	out = []

	d = Instructor.objects.filter(userid=option)
	for i in d:
		for j in i.course.all():
			if j.subject == subj:
				courseNum = j.number
				out.append("<option value='%s'>%s</option>" % (str(courseNum), str(courseNum)))

	dajax.assign('#courseNumberByProf', 'innerHTML', ''.join(out))
	return dajax.json()

@dajaxice_register
def listOfNumbers(request, option):
	dajax = Dajax()
	out = []

	daList = Course.objects.filter(subject=option).values_list('number', flat=True).distinct()
	for i in daList:
		out.append("<option value='%s'>%s</option>" % (i, i))

	dajax.assign('#courseNumber', 'innerHTML', ''.join(out))	
	return dajax.json()

@dajaxice_register
def listOfNumbers2(request, option, idNum):
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
		out.append('<div>Course %s: <select id="courseSubject%s" name="courseSubject%s" onchange="Dajaxice.scheduler.listOfNumbers2(Dajax.process, {\'option\':this.value, \'idNum\':\'#courseNumber%s\'})">%s</select> &nbsp<select id="courseNumber%s" name="courseNumber%s"></select></div>' % (str(aClass), str(aClass), str(aClass), str(aClass), listOfSubjects(), str(aClass), str(aClass)))

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


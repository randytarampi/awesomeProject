from datetime import time
from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext
from django.db.models import Q
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from scheduler.models import *
from scheduler.algorithm import *
from scheduler.helpers import *

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
			timesUnavailable.append(time)
	
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

	instructorsCourses = []
	e = Instructor.objects.filter(userid=d[0])
	for i in e:
		for j in i.course.all():
			instructorsCourses.append("<option value='%s'>%s</option>" % (j.number, j.number))


	dajax.assign('#courseNumberByProf', 'innerHTML', ''.join(instructorsCourses))

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

from django.shortcuts import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import *
from scheduler.models import *
from scheduler.algorithm import *
from scheduler.ajax import *
#from scheduler.helpers import *

def index(request):
	context = {}
	
	listOfDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	context['listOfDays'] = listOfDays

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

	# If session data already exists, list it out on first load of the page
	if 'byCourse' in request.session:
		context['byCourse'] = request.session['byCourse']

	if 'byProf' in request.session:
		context['byProf'] = request.session['byProf']

	if 'timesUnavailable' in request.session:
		context['timesUnavailable'] = request.session['timesUnavailable']

	# Build the context
	if 'processedData' in request.session:
		processedContext = request.session['processedData']
		processedContext['scheduledHTML'] = weeklySchedule(processedContext['optimalMeetingTimes'])
		context['processedHTML'] = render_to_response('schedulerSchedule.html', processedContext).content
	context['subjects'] = allSubjects
	context['initNums'] = initialNumbers
	context['initProfs'] = initialProfs
	context['initNumsByProf'] = instructorsCourses

	return render_to_response('schedulerIndex.html', context, context_instance=RequestContext(request))

def instructions(request):
	return render_to_response('schedulerInstructions.html')

def examples(request):
	return render_to_response('schedulerExamples.html')
    
class courseSubjectListView(ListView):
	context_object_name = "courses"
	template_name = "schedulerCoursesSubject.html"

	def get_queryset(self):
		queryset = get_list_or_404(Course.objects.values('subject', 'number', 'title').distinct(), subject=self.kwargs['subject'])
		for course in queryset:
			course['level'] = course['number'][0]
		return queryset

	def get_context_data(self, **kwargs):
		context = super(courseSubjectListView, self).get_context_data(**kwargs)
		context['subject'] = self.kwargs['subject']
		return context

class courseSubjectNumberListView(ListView):
	context_object_name = "courses"
	template_name = "schedulerCoursesSubjectNumber.html"

	def get_queryset(self):
		return get_list_or_404(Course, subject=self.kwargs['subject'], number=self.kwargs['number'])

	def get_context_data(self, **kwargs):
		context = super(courseSubjectNumberListView, self).get_context_data(**kwargs)
		context['subject'] = self.kwargs['subject']
		context['number'] = self.kwargs['number']
		return context
	
	def render_to_response(self, context):
		if len(self.object_list) == 1:
			return redirect('scheduler_course', self.object_list[0].id)
		return super(courseSubjectNumberListView, self).render_to_response(context)

class courseDetailView(DetailView):
	model = Course
	template_name = "schedulerCourse.html"
	
	def get_context_data(self, **kwargs):
		context = super(courseDetailView, self).get_context_data(**kwargs)
		course = kwargs['object']
		courseMeetingTimes = course.meetingtime_set.all()
		if 'processedData' in self.request.session:
			if 'proposedSchedule' in context: del context['proposedSchedule']
			if 'proposedMeetingTimes' in context: del context['proposedMeetingTimes']
			if 'proposedExamTimes' in context: del context['proposedExamTimes']
			if 'scheduledConflict' in context: del context['scheduledConflict']
			context['scheduledCourses'] = self.request.session['processedData']['optimalCourses']
			context['scheduledInstructors'] = self.request.session['processedData']['optimalInstructors']
			context['scheduledMeetingTimes'] = self.request.session['processedData']['optimalMeetingTimes']
			context['scheduledExamTimes'] = self.request.session['processedData']['optimalExamTimes']
			context['proposedSchedule'] = courseFitsWithMeetingTimeList(course, context['scheduledMeetingTimes'])
			if context['proposedSchedule']:
				context['proposedSchedule'] = sorted(context['proposedSchedule'], key=lambda meeting: meeting.type)
				context['proposedMeetingTimes'] = course.meetingtime_set.exclude(type="EXAM").exclude(type="MIDT")
				context['proposedExamTimes'] = course.meetingtime_set.exclude(type="LAB").exclude(type="LEC")
				context['scheduledHTML'] = weeklySchedule(context['scheduledMeetingTimes'], [meeting for meeting in context['proposedSchedule'] if (meeting.type == "LEC" or meeting.type == "LAB")])
			else:
				context['scheduledConflict'] = "Sorry, but %s %s conflicts with at least one of the classes in your schedule." % (course.subject, course.number)
				context['scheduledHTML'] = weeklySchedule(context['scheduledMeetingTimes'])
		else:
			context['scheduledHTML'] = weeklySchedule([], courseMeetingTimes.exclude(type="EXAM").exclude(type="MIDT"))
		return context


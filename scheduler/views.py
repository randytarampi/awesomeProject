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
	
	out = []
	byCourseList = []
	byProfList = []
	if 'byCourse' in request.session:
		for course in request.session['byCourse']:
			byCourseList.append(course)
	if 'byProf' in request.session:
		for course in request.session['byProf']:
			byProfList.append(course)
	duplicate = 0
	for e1 in byCourseList:
		for e2 in byProfList:
			if e1[0] == e2[0] and e1[1] == e2[2]:
				duplicate += 1
	length = byCourseList.__len__() + byProfList.__len__() - duplicate
	for i in range(1, length + 1):
		out.append(i)
	context['numCourses'] = out

	listOfDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

	allSubjects = Course.objects.values_list('subject', flat=True).distinct()

	# Using the 0-th element so that any set of data will give the first element. This is using the same query as in ajax.py
	firstSubject = allSubjects[0]
	initialNumbers = Course.objects.filter(subject=firstSubject).values_list('number', flat=True).distinct()

	# More initial values, w.r.t. instructor form this time 	
	c = Course.objects.filter(subject=firstSubject)
	initialProfs = Instructor.objects.filter(course__in=c).exclude(first_name__startswith=".").order_by('last_name').distinct()

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

	if 'byId' in request.session:
		context['byId'] = request.session['byId']

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
	request.breadcrumbs("Scheduler Instructions", request.path_info)
	return render_to_response('schedulerInstructions.html', context_instance=RequestContext(request))

def examples(request):
	request.breadcrumbs("Scheduler Examples", request.path_info)
	return render_to_response('schedulerExamples.html', context_instance=RequestContext(request))

class instructorListView(ListView):
	context_object_name = "instructors"
	template_name = "schedulerInstructors.html"

	def get_queryset(self):
		self.request.breadcrumbs("Instructors", self.request.path_info)
		queryset = get_list_or_404(Instructor.objects.order_by('last_name', 'first_name').exclude(first_name__startswith="."))
		return queryset

class instructorDetailView(DetailView):
	model = Instructor
	template_name = "schedulerInstructor.html"
	
	def get_object(self):
		object = super(instructorDetailView, self).get_object()
		self.request.breadcrumbs(("Instructors", reverse("scheduler_instructors")), (object.name, self.request.path_info))
		return object

class courseListView(ListView):
	context_object_name = "courses"
	template_name = "schedulerCourses.html"

	def get_queryset(self):
		self.request.breadcrumbs("Classes", self.request.path_info)
		queryset = get_list_or_404(Course.objects.order_by('subject').values('subject', 'number', 'title').distinct())
		return queryset

class courseSubjectListView(ListView):
	context_object_name = "courses"
	template_name = "schedulerCoursesSubject.html"

	def get_queryset(self):
		self.request.breadcrumbs(("Classes", reverse("scheduler_courses")), (self.kwargs['subject'], self.request.path_info))
		queryset = get_list_or_404(Course.objects.values('subject', 'number', 'title').distinct(), subject=self.kwargs['subject'])
		for course in queryset:
			course['level'] = course['number'][0]
		self.request.breadcrumbs("%s" % self.kwargs['subject'], reverse("scheduler_coursesSubject", args=(self.kwargs['subject'],)))
		return queryset

	def get_context_data(self, **kwargs):
		context = super(courseSubjectListView, self).get_context_data(**kwargs)
		context['subject'] = self.kwargs['subject']
		return context

class courseSubjectNumberListView(ListView):
	context_object_name = "courses"
	template_name = "schedulerCoursesSubjectNumber.html"

	def get_queryset(self):
		self.request.breadcrumbs(("Classes", reverse("scheduler_courses")), (self.kwargs['subject'], reverse("scheduler_coursesSubject", args=(self.kwargs['subject'],))), ("%s %s" % (self.kwargs['subject'], self.kwargs['number']), reverse("scheduler_coursesSubjectNumber", args=(self.kwargs['subject'], self.kwargs['number'],))))
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
	
	def get_object(self):
		object = super(courseDetailView, self).get_object()
		self.request.breadcrumbs(("Classes", reverse("scheduler_courses")), (object.subject, reverse("scheduler_coursesSubject", args=(object.subject,))), (object, reverse("scheduler_coursesSubjectNumber", args=(object.subject, object.number,))), ("Section %s" % object.section, self.request.path_info))
		return object
	
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
			if courseMeetingTimes.exclude(type="EXAM").exclude(type="MIDT"): context['scheduledHTML'] = weeklySchedule([], courseMeetingTimes.exclude(type="EXAM").exclude(type="MIDT"))
		return context


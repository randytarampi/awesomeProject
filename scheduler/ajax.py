from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from scheduler.models import *

def listOfSubjects():
	allSubjects = Course.objects.values_list('subject', flat=True).distinct()
	datList = []
	# runs through every subject and makes an option for a select tag where value = Subject
	for i in allSubjects:
		datList.append("<option value='%s'>%s</option>" % (i, i))
	return ''.join(datList)

def listOfNumbers(request, option):
	daList = Course.objects.filter(subject=option).values_list('number', flat=True)
	htmlList = []
	j = 0
	for i in daList:
		htmlList.append("<option value='%s'>%s</option>" % (i, i))
		dajax.assign('#courseNumber%d' % str(j), 'innerHTML', ''.join(htmlList))
		j += 1;

@dajaxice_register
def updatingCourseForm(request, option):
	dajax = Dajax()

	out = []
	# several select tags are made, each with a complete list of subjects with value = 1 through aClass
	for aClass in range(1, int(option)+1):
		out.append('<div>Course %s: <select id="courseSubject%s" onchange=%s>%s</select> &nbsp<select id="courseNumber%s"></select></div>' % (str(aClass), str(aClass), "Dajaxice.scheduler.listOfNumbers(Dajax.process, {'option':this.value})", listOfSubjects(), str(aClass)))

	dajax.assign('#listClasses', 'innerHTML', ''.join(out))
	return dajax.json()


from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from scheduler.models import *

def listOfSubjects():
	allSubjects = Course.objects.values_list('subject', flat=True).distinct()
	datList = []
	for i in allSubjects:
		datList.append("<option value='%s'>%s</option>" % (i, i))
	return ''.join(datList)

@dajaxice_register
def updatingCourseForm(request, option):
	dajax = Dajax()

	out = []
	for aClass in range(1, int(option)+1):
		out.append('<div>Course %s: &nbsp<select id="courseNumber%s">%s</select></div>' % (str(aClass), str(aClass), listOfSubjects()))
		#dajax.assign('#courseNumber%s' % str(aClass), 'innerHTML', listOfSubjects())

	dajax.assign('#listClasses', 'innerHTML', ''.join(out))
	return dajax.json()

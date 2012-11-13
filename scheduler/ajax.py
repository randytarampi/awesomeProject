from dajaxice.decorators import dajaxice_register
from dajax.core import dajax

# steven sucks

@dajaxice_register
def updatingCourseForm(request, option):
	dajax = Dajax()

	return dajax.json()
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

@dajaxice_register
def updatingCourseForm(request, option):
	dajax = Dajax()

	out = []
	for aClass in range(0, int(option)):
		out.append("<p>Course %s</p>" % str(aClass))

	dajax.assign('#listClasses', 'innerHTML', ''.join(out))
	return dajax.json()

@dajaxice_register
def updatecombo(request, option):
    dajax = Dajax()
    options = [['Madrid', 'Barcelona', 'Vitoria', 'Burgos'],
               ['Paris', 'Evreux', 'Le Havre', 'Reims'],
               ['London', 'Birmingham', 'Bristol', 'Cardiff']]
    out = []
    for option in options[int(option)]:
        out.append("<option value='#'>%s</option>" % option)

    dajax.assign('#combo2', 'innerHTML', ''.join(out))
    return dajax.json()
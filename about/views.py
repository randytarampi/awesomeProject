from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

# Create your views here.
def index(request):
	request.breadcrumbs('About', request.path_info)
	return render_to_response('aboutIndex.html', context_instance=RequestContext(request))

def acknowledgements(request):
	request.breadcrumbs(('About', reverse('about_index')), ('Acknowledgements', request.path_info))
	print request
	return render_to_response('aboutAcknowledgements.html', context_instance=RequestContext(request))

def legal(request):
	request.breadcrumbs(('About', reverse('about_index')), ('Legal', request.path_info))
	print request
	return render_to_response('aboutLegal.html', context_instance=RequestContext(request))

def team(request):
	request.breadcrumbs(('About', reverse('about_index')), ('The Team', request.path_info))
	print request
	return render_to_response('aboutTeam.html', context_instance=RequestContext(request))

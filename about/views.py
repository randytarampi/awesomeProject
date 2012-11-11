from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

# Create your views here.
def index(request):
    return render_to_response('aboutIndex.html')

def acknowledgements(request):
    return render_to_response('aboutAcknowledgements.html')

def legal(request):
    return render_to_response('aboutLegal.html')

def team(request):
    return render_to_response('aboutTeam.html')

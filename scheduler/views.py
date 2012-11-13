from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

# Create your views here.
def index(request):
    return render_to_response('schedulerIndex.html')

def instructions(request):
    return render_to_response('schedulerInstructions.html')

def examples(request):
    return render_to_response('schedulerExamples.html')

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

# Create your views here.
def index(request):
    return render_to_response('aboutIndex.html')

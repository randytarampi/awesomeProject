from datetime import time
from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext
from scheduler.models import *
from scheduler.algorithm import *

# A file that holds helper functions

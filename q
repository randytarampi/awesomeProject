diff --git a/scheduler/templates/schedulerIndex.html b/scheduler/templates/schedulerIndex.html
index d9d0b5b..77ebc28 100644
--- a/scheduler/templates/schedulerIndex.html
+++ b/scheduler/templates/schedulerIndex.html
@@ -9,6 +9,16 @@
 	<h1>Build a Schedule</h1>
 	<form id="scheduleForm" method="POST">
 	{% csrf_token %}
+		<div id="addCourse">
+			Add a course:
+			<!--<select id="courseSubject" name="courseSubject" onchange="Dajaxice.scheduler.listOfNumbers(Dajax.process, {\'option\':this.value, \'idNum\':\'courseNumber\'})">{{ subjects }}</select>-->
+			<select>
+				{% for op in subjects %}
+				<option value="{{ op }}">{{ op }}</option>
+				{% endfor %}
+			</select>
+		</div>
+
 		<span>How many classes are you considering?
 			<select id="numClasses" name="numClasses" onchange="Dajaxice.scheduler.updatingCourseForm(Dajax.process, {'option':this.value})" size="1">
 				<option value="1">1</option>
diff --git a/scheduler/views.py b/scheduler/views.py
index 5f39d64..cb69723 100644
--- a/scheduler/views.py
+++ b/scheduler/views.py
@@ -2,9 +2,12 @@ from django.shortcuts import get_object_or_404, render_to_response
 from django.http import HttpResponseRedirect, HttpResponse
 from django.core.urlresolvers import reverse
 from django.template import RequestContext
+from scheduler.models import *
 
 def index(request):
-    return render_to_response('schedulerIndex.html', context_instance=RequestContext(request))
+    allSubjects = Course.objects.values_list('subject', flat=True).distinct()
+    print allSubjects
+    return render_to_response('schedulerIndex.html',{'subjects': allSubjects}, context_instance=RequestContext(request))
 
 def instructions(request):
     return render_to_response('schedulerInstructions.html')

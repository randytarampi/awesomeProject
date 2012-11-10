from django.contrib import admin
from scheduler.models import *

class InstructorInline(admin.StackedInline):
    model = Instructor

class MeetingTimeInline(admin.StackedInline):
    model = MeetingTime

class CourseAdmin(admin.ModelAdmin):
    model = Course    

admin.site.register(Course, CourseAdmin)

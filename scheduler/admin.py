from django.contrib import admin
from scheduler.models import *

class InstructorInline(admin.StackedInline):
    model = Instructor
    extra = 0

class MeetingTimeInline(admin.StackedInline):
    model = MeetingTime
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    model = Course
    inlines = [InstructorInline, MeetingTimeInline]

admin.site.register(Course, CourseAdmin)

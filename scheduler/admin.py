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
    search_fields = ['title', 'subject', 'number', 'component']
    list_display = ('title', 'subject', 'number', 'section', 'component','campus', 'semester')
    list_filter = ['semester', 'campus', 'subject', 'number']

admin.site.register(Course, CourseAdmin)

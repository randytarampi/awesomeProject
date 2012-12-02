from django.contrib import admin
from scheduler.models import *

class InstructorInline(admin.StackedInline):
    model = Instructor.course.through
    extra = 0

class MeetingTimeInline(admin.StackedInline):
    model = MeetingTime
    extra = 0

class CourseInline(admin.StackedInline):
    model = Instructor.course.through
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    model = Course
    inlines = [InstructorInline, MeetingTimeInline]
    search_fields = ['title', 'subject', 'number', 'component']
    list_display = ('title', 'subject', 'number', 'section', 'component','campus', 'semester')
    list_filter = ['semester', 'campus', 'subject', 'number']

class InstructorAdmin(admin.ModelAdmin):
    model = Instructor
    inlines = [CourseInline]
    fieldsets = [(None, { 'fields': ['userid', 'first_name', 'last_name'] }),
                 ('Classes List', {'fields': ['course'], 'classes': ['collapse']})]
    search_fields = ['userid', 'name']
    list_display = ('userid', 'first_name', 'last_name')

admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)

from django.db import models

# Create your models here.

class Course (models.Model):
	title = models.CharField(max_length=200)
	section = models.CharField(max_length=50)
	component = models.CharField(max_length=10)#
	number = models.CharField(max_length = 10)
	semester = models.CharField(max_length = 4) 
	CAMPUS_CHOICES = (
        	('BRNBY', 'Burnaby'),
       		('SURRY', 'Surrey'),
		('VANCR', 'Vancouver'),
		('OFFST', 'Offsite'),
    	)
	campus = models.CharField(max_length=5, choices=CAMPUS_CHOICES) # BRNBY, SURRY, VANCR, OFFST
	subject = models.CharField(max_length=10) #cmpt etc...

class Instructor (models.Model):
	userid = models.CharField(max_length = 100)
	name = models.CharField(max_length = 100)
	course = models.ForeignKey(Course)

class MeetingTime (models.Model):
	start_day = models.CharField(max_length = 50)
	room = models.CharField(max_length = 50)
	start_time = models.CharField(max_length = 50)
	end_day = models.CharField(max_length = 50)
	weekday = models.IntegerField()
	type = models.CharField(max_length = 10)
	end_time = models.CharField(max_length = 50)
	course = models.ForeignKey(Course)


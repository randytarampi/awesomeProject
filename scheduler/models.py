from django.db import models

COMPONENT_CHOICES = (
	('STD', 'STD'),
	('LEC', 'Lecture'),
	('PRA', 'PRA'),
	('TUT', 'Tutorial'),
	('LAB', 'Lab'),
	('WKS', 'WKS'),
	('OLC', 'OLC'),
	('SEC', 'SEC'),
	('IND', 'IND'),
	('SEM', 'Seminar'),
	('FLD', 'FLD'),
)

CAMPUS_CHOICES = (
	('BRNBY', 'Burnaby'),
      	('SURRY', 'Surrey'),
       	('VANCR', 'Vancouver'),
	('OFFST', 'Offsite'),
)

WEEKDAY_CHOICES = (
	(0, 'Monday'),
	(1, 'Tuesday'),
	(2, 'Wednesday'),
	(3, 'Thursday'),
	(4, 'Friday'),
	(5, 'Saturday'),
	(6, 'Sunday'),
)

TYPE_CHOICES = (
	('MIDT', 'Midterm'),
	('LEC', 'Lecture'),
	('EXAM', 'Exam'),
	('LAB', 'Lab'),
)

SEMESTER_CHOICES = (
	('1127', 'Fall 2012'),
	('1131', 'Winter 2013'),
)

# Create your models here.
class Course (models.Model):
	title = models.CharField(max_length=200)
	section = models.CharField(max_length=50)
	component = models.CharField(max_length=3, choices=COMPONENT_CHOICES)
	number = models.CharField(max_length = 10)
	semester = models.CharField(max_length = 4, choices=SEMESTER_CHOICES) 
        campus = models.CharField(max_length=5, choices=CAMPUS_CHOICES)
	subject = models.CharField(max_length=10) #cmpt etc...

	def __unicode__(self):
		"""
		Return the course name.
		"""
		return self.subject + " " + self.number + ": " + self.title

class Instructor (models.Model):
	userid = models.CharField(max_length = 100, null=True)
	name = models.CharField(max_length = 100)
	course = models.ForeignKey(Course)

	def __unicode__(self):
		"""
        	Return the instructor's name.
		"""
		return self.name

class MeetingTime (models.Model):
	start_day = models.DateField('Start Date')
	room = models.CharField(max_length = 50)
	start_time = models.TimeField('Start Time')
	end_day = models.DateField('End Date')
	weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
	type = models.CharField(max_length = 10, choices=TYPE_CHOICES)
	end_time = models.TimeField('End Time')
	course = models.ForeignKey(Course)

	def __unicode__(self):
		"""
        	Return the instructor's name.
		"""
		return WEEKDAY_CHOICES[self.weekday][1] + " - " + str(self.start_time) + " to " + str(self.end_time)

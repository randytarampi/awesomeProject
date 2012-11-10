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

# Create your models here.
class Course (models.Model):
	title = models.CharField(max_length=200)
	section = models.CharField(max_length=50)
	component = models.CharField(max_length=3, choices=COMPONENT_CHOICES)
	number = models.CharField(max_length = 10)
	semester = models.CharField(max_length = 4) 
        campus = models.CharField(max_length=5, choices=CAMPUS_CHOICES)
	subject = models.CharField(max_length=10) #cmpt etc...

	def __unicode__(self):
		"""
		Return the course name.
		"""
		return self.subject + " " + self.number + ": " + self.title

class Instructor (models.Model):
	userid = models.CharField(max_length = 100)
	name = models.CharField(max_length = 100)
	course = models.ForeignKey(Course)

	def __unicode__(self):
		"""
        	Return the instructor's name.
		"""
		return self.name

class MeetingTime (models.Model):
	start_day = models.CharField(max_length = 50)
	room = models.CharField(max_length = 50)
	start_time = models.CharField(max_length = 50)
	end_day = models.CharField(max_length = 50)
	weekday = models.IntegerField()
	type = models.CharField(max_length = 10)
	end_time = models.CharField(max_length = 50)
	course = models.ForeignKey(Course)


from django.db import models

COMPONENT_CHOICES = (
	('STD', 'Studio'),
	('LEC', 'Lecture'),
	('PRA', 'Practicum'),
	('TUT', 'Tutorial'),
	('LAB', 'Laboratory'),
	('WKS', 'Workshop'),
	('OLC', 'Online Conference'),
	('SEC', 'Distance Education'),
	('IND', 'Independent Study'),
	('SEM', 'Seminar'),
	('FLD', 'Field School'),
)

CAMPUS_CHOICES = (
	('BRNBY', 'Burnaby'),
	('SURRY', 'Surrey'),
	('VANCR', 'Vancouver'),
	('OFFST', 'Offsite'),
	('METRO', 'Metro Vancouver'),
	('GNWC', 'Great Northern Way'),
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
	('EXAM', 'Final'),
	('LAB', 'Lab/Tutorial'),
)

SEMESTER_CHOICES = (
	('1127', 'Fall 2012'),
	('1131', 'Spring 2013'),
	('1134', 'Summer 2013'),
	('1137', 'Fall 2013'),
)

class Course (models.Model):
	title = models.CharField(max_length=200)
	section = models.CharField(max_length=50)
	component = models.CharField(max_length=3, choices=COMPONENT_CHOICES)
	number = models.CharField(max_length = 10)
	semester = models.CharField(max_length = 4, choices=SEMESTER_CHOICES) 
	campus = models.CharField(max_length=5, choices=CAMPUS_CHOICES)
	subject = models.CharField(max_length=10)

	def __unicode__(self):
		"""
		Return the course name.
		"""
		return self.subject + " " + self.number + ": " + self.title

	def componentChoice(self):
		"""
		Return the component.
		"""
		return self.get_component_display()

	def semesterChoice(self):
		"""
		Return the semester.
		"""
		return self.get_semester_display()

	def campusChoice(self):
		"""
		Return the campus.
		"""
		return self.get_campus_display()
	
	def courseLevel(self):
		"""
		Return the level (x00 level) of the course
		"""
		return self.number and self.number[0] or '' +"00"

class Instructor (models.Model):
	userid = models.CharField(max_length = 100, primary_key=True)
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	course = models.ManyToManyField(Course)

	def __unicode__(self):
		"""
		Return the instructor's name.
		"""
		return self.userid
	
	def name(self):
		"""
		Return the instructor's full name.
		"""
		return self.first_name + " " + self.last_name
	
	def firstLetter(self):
		"""
		Return the first letter of the instructor's last name.
		"""
		return self.last_name and self.last_name.upper()[0] or ''

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
		Return the meeting time.
		"""
		return self.get_weekday_display() + " - " + str(self.start_time) + " to " + str(self.end_time)
	
	def dayChoice(self):
		"""
		Return the weekday.
		"""
		return self.get_weekday_display()

	def typeChoice(self):
		"""
		Return the type.
		"""
		return self.get_type_display()

#course.py

class SchedulingCourse:
	def __init__(self, title, courseID, meetingTimes, exams, labs, campus, dataBaseCourse):
		self.title = title
		self.courseID = courseID
		self.meetingTimes = meetingTimes# list of meeting times
		self.exams = exams
		self.labs = labs
		self.campus = campus # 1 = Burnaby, 2 = surrey, 3 = vancouver, 0 = something else
		self.dataBaseCourse = dataBaseCourse
    	def addMeetingTime(self, meetingTime):
        	self.meetingTimes.append(meetingTime)


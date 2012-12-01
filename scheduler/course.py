#course.py

class SchedulingCourse:
	def __init__(self, title, courseID, meetingTimes, exams, labs, campus):
		self.title = title
		self.courseID = courseID
		self.meetingTimes = meetingTimes# list of meeting times
		self.exams = exams
		self.labs = labs
		self.campus = campus # 1 = Burnaby, 2 = surrey, 3 = vancouver, 0 = something else
		
        #we may want to include the id in course here...
    	def addMeetingTime(self, meetingTime):
        	self.meetingTimes.append(meetingTime)
    		#priority ... number
   	 	#has priority? boolean


class SchedulingMeetingTime:
    #def __init__(self, startTime, endTime, weekday, startDate, endDate):
	def __init__(self, startTime, endTime, weekday, startDate, endDate, meetingType, meetingTimeID):
		self.startTime = startTime
		self.endTime = endTime
		self.weekday = weekday
		self.meetingType = meetingType
		self.startDate = startDate
		self.endDate = endDate
		self.meetingTimeID = meetingTimeID


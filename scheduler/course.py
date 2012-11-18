#course.py

class SchedulingCourse:
	def __init__(self, title, courseID, meetingTimes, campus):
		self.title = title
		self.courseID = courseID
		self.meetingTimes = meetingTimes# list of meeting times
		self.campus = campus # 1 = Burnaby, 2 = surrey, 3 = vancouver, 0 = something else
        #we may want to include the id in course here...
    	def addMeetingTimes(self, meetingTime):
        	self.meetingTimes.append(meetingTime)
    		#priority ... number
   	 	#has priority? boolean


class SchedulingMeetingTime:
    #def __init__(self, startTime, endTime, weekday, startDate, endDate):
	def __init__(self, startTime, endTime, weekday):
		self.startTime = startTime
		self.endTime = endTime
		self.weekday = weekday
		#self.startDate = startDate
		#self.endDate = endDate


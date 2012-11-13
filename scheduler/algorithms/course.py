#course.py

class Course:
    def __init__(self, title, meetingTimes):
        self.title = title
        self.meetingTimes = meetingTimes# list of meeting times

    def addMeetingTimes(self, meetingTime):
        self.meetingTimes.append(meetingTime)
    #priority ... number
    #has priority? boolean


class MeetingTime:
    #def __init__(self, startTime, endTime, weekday, startDate, endDate):
    def __init__(self, startTime, endTime, weekday):
        self.startTime = startTime
        self.endTime = endTime
        self.weekday = weekday
        #self.startDate = startDate
        #self.endDate = endDate


#because python is much more.... flexible and not as tightly cast as java
# I find it hard to write certain functions

#def addMTToSingleCourse(course, meetingTime):
#    course.meetingTimes.append(meetingTime)



from schedulingalg import *


def simpleTest():
	testinput = []
    	c = Course.objects.get(id = 1L)
    	testinput.append(c)
    	return functionForRandy(1, testinput)
    	#output = functionForRandy(1, testinput)

def largeTest():
    	return functionForRandy(5, Course.objects.all())
def conradTest():
    	testCourseList = []
    	testCourse1 = Course.objects.get(id = 1L)
    	testCourseList.append(testCourse1)    
    	testCourse2 = Course.objects.get(id = 4L)
    	testCourseList.append(testCourse2)
    	#print testCourseList
    	#print functionForRandy(2, testCourseList)
    	return functionForRandy(2, testCourseList)

#output = conradTest()
#simpleTest()
output = largeTest()

c1 = output[0][0]
c2 = output[0][1]
c3 = output[0][2]
c4 = output[0][3]
c5 = output[0][4]
mt1 = MeetingTime.objects.filter(course = c1.id)
mt2 = MeetingTime.objects.filter(course = c2.id)
mt3 = MeetingTime.objects.filter(course = c3.id)
mt4 = MeetingTime.objects.filter(course = c4.id)
mt5 = MeetingTime.objects.filter(course = c5.id)

stats = output[2]
days = stats.changeNumberOfDays
gap = stats.changeTotalGap

#1l, 4l, 5l, 78l, 147l

#c2 = output[1]
#print "howdy"
#c = Course.objects.get(id = 1L)
#testinput = []
#testinput.append(c)
#functionForRandy(1, testinput)
#output = functionForRandy(1, testinput)

#dead code

#s = Schedule()
#s.totalPurge()
#c = Course()
#m1 = MeetingTime(1,2,1)
#c.addMeetingTimes(m1)
#lockCourse(c, s)
#poc = []
#generateCourses(poc)
#potc = poc
#lockc = []
#iterateBEHEMOTH(s, lockc, potc, 2)
#iterateBEHEMOTH(s, lockc, potc, 2) 
#testMT = convertStringToMeetingTime("<MeetingTime: Monday - 10:30:00 to 12:20:00>")


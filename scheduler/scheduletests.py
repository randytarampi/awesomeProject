from algorithm import *

def simpleTest():
	testinput = []
    	c = Course.objects.get(id = 1L)
    	testinput.append(c)
    	return createOptimalSchedule(1, testinput)
    	#output = createOptimalSchedule(1, testinput)

def largeTest():
	#Course.objects.filter(subject = "cmpt")

    	#return createOptimalSchedule(5, Course.objects.all())
	#return createOptimalSchedule(5, Course.objects.all(), True)
	#return createOptimalSchedule(5, Course.objects.filter(subject = "cmpt"), True)
	return createOptimalSchedule(5, Course.objects.filter(subject = "bisc"), True)
	#selectedCourses = Course.objects.filter(section__startswith="C")
	return createOptimalSchedule(5, selectedCourses, True)
	 
def conradTest():
    	testCourseList = []
    	testCourse1 = Course.objects.get(id = 1L)
    	testCourseList.append(testCourse1)    
    	testCourse2 = Course.objects.get(id = 4L)
    	testCourseList.append(testCourse2)
    	#print testCourseList
    	#print createOptimalSchedule(2, testCourseList)
    	return createOptimalSchedule(2, testCourseList, True)

#output = conradTest()
#simpleTest()
output = largeTest()

c1 = output[1][0]
c2 = output[1][1]
c3 = output[1][2]
c4 = output[1][3]
c5 = output[1][4]
mt1 = MeetingTime.objects.filter(course = c1.id)
mt2 = MeetingTime.objects.filter(course = c2.id)
mt3 = MeetingTime.objects.filter(course = c3.id)
mt4 = MeetingTime.objects.filter(course = c4.id)
mt5 = MeetingTime.objects.filter(course = c5.id)

cutcourses = output[2]

stats = output[3]
days = stats.numberOfDays
gap = stats.totalGap
travels = stats.crossCampusTravels

schedule = output[4]

monday = schedule.mondayTimeSlotAvailability
tuesday = schedule.tuesdayTimeSlotAvailability
wednesday = schedule.wednesdayTimeSlotAvailability
thursday = schedule.thursdayTimeSlotAvailability
friday = schedule.fridayTimeSlotAvailability
saturday = schedule.saturdayTimeSlotAvailability
sunday = schedule.sundayTimeSlotAvailability


c = Course.objects.get(id = 2562)
ac = convertCourseModelToCourseObject(c, False)
s = Schedule()

#1l, 4l, 5l, 78l, 147l

#c2 = output[1]
#print "howdy"
#c = Course.objects.get(id = 1L)
#testinput = []
#testinput.append(c)
#createOptimalSchedule(1, testinput)
#output = createOptimalSchedule(1, testinput)

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


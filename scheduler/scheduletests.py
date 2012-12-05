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
	#return createOptimalSchedule(5, Course.objects.filter(subject = "cmpt"))
	#return createOptimalSchedule(5, Course.objects.filter(subject = "bisc"), True)
	#selectedCourses = Course.objects.filter(section__startswith="C")
	#return createOptimalSchedule(5, selectedCourses, True)
	selectedCourses = Course.objects.filter(subject="CMPT", number=125) | Course.objects.filter(subject="CMPT", number=150) | Course.objects.filter(subject="CMPT", number=165) | Course.objects.filter(subject="MACM", number=201) | Course.objects.filter(subject="POL", number=100)
	#createOptimalSchedule(5, selectedCourses)
	cmpt165List = Course.objects.filter(subject="CMPT", number=165)
	cmpt125List = Course.objects.filter(subject="CMPT", number=125)
	cmpt165 = cmpt165List[0]
	#return createOptimalSchedule(1, cmpt165List)
	

	#H:M:S
	#convertStringToTime(inputstring)
	stringArray = ["19:30:00"]
	
	daysArray = [1]
	#for i in range (0, len(stringArray)):
	#firstUnavaiableMeetingTime = (0, convertStringToTime("10:00:00"), convertStringToTime("14:30:00"))
	#listUnavailableMeetingTimes = [firstUnavaiableMeetingTime]
	listUnavailableMeetingTimes = []
	startArray = ["10:30:00"]
	endArray = ["14:30:00"]
	weekdayArray = [0]
	if len(startArray) == len(endArray) == len(weekdayArray):
		for i in range (0, len (startArray)):	
			unavailableTimeFromArrays = (weekdayArray[i], convertStringToTime(startArray[i]), convertStringToTime(endArray[i]))
			listUnavailableMeetingTimes.append(unavailableTimeFromArrays)
	#return createOptimalSchedule(4, cmpt125List, selectedCourses, listUnavailableMeetingTimes)
	return createOptimalSchedule(4, selectedCourses, listUnavailableMeetingTimes)
	
	
	
	
	#return createOptimalSchedule(3, Course.objects.filter(subject="CMPT", number=165))
	#return createOptimalSchedule(3, createOptimalSchedule(4, selectedCourses)[1])
	#return createOptimalSchedule(5, selectedCourses)
	
	#createOptimalSchedule(3, selectedCourses)


def conradTest():
    	testCourseList = []
    	testCourse1 = Course.objects.get(id = 1L)
    	testCourseList.append(testCourse1)    
    	testCourse2 = Course.objects.get(id = 4L)
    	testCourseList.append(testCourse2)
    	#print testCourseList
    	#print createOptimalSchedule(2, testCourseList)
    	return createOptimalSchedule(2, testCourseList, True)



#Testing pasturize
selectedCourses = Course.objects.filter(subject="CMPT", number=125) | Course.objects.filter(subject="CMPT", number=150) | Course.objects.filter(subject="CMPT", number=165) | Course.objects.filter(subject="MACM", number=201) | Course.objects.filter(subject="POL", number=100)
print "Len selectedCourses = " + str(len(selectedCourses))
newSelectedCourses = []
for i in range (0, len(selectedCourses)):
	newCourse = convertCourseModelToCourseObject(selectedCourses[i], False)
	if (newCourse != False):
		handleLabsForCourse(newCourse, newSelectedCourses)
print "Len newSelectedCourses = " + str(len(newSelectedCourses))
past = regroupCoursesForPasturize(newSelectedCourses)
pastLen = len(past)
for i in range (0, pastLen):
	print "Print past list number " + str (i)
	pastSubList = past[i]
	for j in range (0, len(pastSubList)):
		pastCourse = pastSubList[j]
		print "course Title = " + pastCourse.title

schedule = Schedule()
compPast = completePasturize(newSelectedCourses, schedule, 4)
#findPasturizeTopPickDarwinism(listOfPotentialSchedules, schedule):
bestP = findPasturizeTopPickDarwinism(compPast, schedule)
#output = conradTest()
#simpleTest()
#Tests for behemoth algorithm output
output = largeTest()
meet = output[0]
for i in range (0, len (meet)):
	print meet[i].type
c1 = output[1][0]
c2 = output[1][1]
c3 = output[1][2]
c4 = output[1][3]
#c5 = output[1][4]
mt1 = MeetingTime.objects.filter(course = c1.id)
mt2 = MeetingTime.objects.filter(course = c2.id)
mt3 = MeetingTime.objects.filter(course = c3.id)
mt4 = MeetingTime.objects.filter(course = c4.id)
#mt5 = MeetingTime.objects.filter(course = c5.id)

#mtList1 = [mt1] 
#mtList2 = [mt2]

cuttimes = output[2]
cutcourses = output[3]

stats = output[4]
days = stats.numberOfDays
gap = stats.totalGap
travels = stats.crossCampusTravels

schedule = output[5]

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


#if (meetingTimesConflict(mt1[0], mt1[0])
#	print "Conflict Mt1,

#meetOne = []
#for i in range (0, len(mt1)):
#	meetOne.append(mt1[i])

#if meetingTimesNewTimesOldTimesFilter(meetOne, meetOne) == []:
#	print "Conflict Mt1, MT1"
#else:
#	print "No Conflict between mt1 and mt1"
#	print  meetingTimesNewTimesOldTimesFilter(meetOne, meetOne) 

#if meetingTimesNewTimesOldTimesFilter(mt1, mt2) == []:
#	print "Conflict Mt1, MT1"
#else:
#	print "No Conflict between mt1 and mt2"
#	print  meetingTimesNewTimesOldTimesFilter(meetOne, meetOne) 

cmpt125exam = MeetingTime.objects.filter(course = 511)[1]
macm201exam = MeetingTime.objects.filter(course = 1960)[1]

cmpt165List = Course.objects.filter(subject="CMPT", number=165)
#macm201List = Course.objects.filter(subject = "MACM", number = 201)
#macm201List = Course.objects.filter(subject = "MACM", number = 1960)

scheduleCourses = []
for i in range (0, len(schedule.poolOfLockedCourses)):
	testCourse = schedule.poolOfLockedCourses[i].dataBaseCourse
	scheduleCourses.append(testCourse)
	#poolOfLockedCourses
lockC = schedule.poolOfLockedCourses
#dataBaseCourse

for course in output[3]: print course, course.section



def courseFitsWithMeetingTimeListTest():
	
	cmpt125List = Course.objects.filter(subject="CMPT", number=125)
	cFI1 = cmpt125List[0] 
	#cFI1 = cmpt165List[1] 
	
	cFI2 = MeetingTime.objects.filter(course = 1)
	#cFI2 = MeetingTime.objects.filter(course = 511)
	cFO = courseFitsWithMeetingTimeList(cFI1, cFI2)

	if cFO == []:
		print "courseFitsWithMeetingTimeList We have a conflict with the course"
	else:
		print "courseFitsWithMeetingTimeList fits = " 
		print cFO

#courseFitsWithMeetingTimeListTest()

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


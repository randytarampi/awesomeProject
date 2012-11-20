#import schedule
from datetime import datetime
from schedule import *
from course import *
from choicestats import *
from models import *
import shlex



# Main function
#takes number of courses that the student wants,
# and a list of coursese the student is interested in and outputs a list of courses 
#that will be in an optimal schedule
def functionForRandy(numberOfCourses, listofCourses):
    schedule = Schedule()
    poolOfLockedCourses = []
    newListOfCourses = []
    poolOfCutCourses = []
    for i in range (0, len(listofCourses)):
        newCourse = convertCourseModelToCourseObject(listofCourses[i])
	if (newCourse != False):
	    #print "Course is acceptable"
	    newListOfCourses.append(newCourse)
    #print "size of newListOfCourses =" + str(len(newListOfCourses))
    #print "new newlistcourse = " + str(newListOfCourses[0])
    newCourse = newListOfCourses[0]
    newMeetingTimes = newCourse.meetingTimes
    for i in range (0, numberOfCourses):
        iterateBEHEMOTH(schedule, poolOfLockedCourses, newListOfCourses, poolOfCutCourses, numberOfCourses)
    outPutListOfLockedCourses = []
    #print "size of lockedCourses =" + str(len(poolOfLockedCourses))
    for i in range (0, len(poolOfLockedCourses)):
	temporaryID = poolOfLockedCourses[i].courseID
        outputCourse = Course.objects.get(id = temporaryID)
        outPutListOfLockedCourses.append(outputCourse)
    outPutListOfCutCourses = []
    for i in range (0, len(poolOfCutCourses)):
	temporaryID = poolOfCutCourses[i].courseID
        outputCourse = Course.objects.get(id = temporaryID)
        outPutListOfCutCourses.append(outputCourse)
    #print "size of output =" + str(len(outPutListOfCourses))
    #print "new newlistcourse = " + str(newListOfCourses[0])
    print "size of poolcut =" + str(len(poolOfCutCourses))
    #return outPutListOfCourses
    largerOutputArray = []
    largerOutputArray.append(outPutListOfLockedCourses)
    largerOutputArray.append(outPutListOfCutCourses)
    return largerOutputArray
# need a function that handles the case when the scheduler can't handle a certain course

#Turns a course model object into a course object that we can use in the scheduler
#Converts : course from database --> course usable by scheduler
def convertCourseModelToCourseObject(inputCourse):
    id = inputCourse.id		
    listofmeetingTimes = MeetingTime.objects.filter(course = id)
    if (len (listofmeetingTimes) == 0):
	return False
    if inputCourse.component == "PRA":
	return False
    courseInfo = inputCourse.subject
    courseInfo += inputCourse.number
    courseMeetingTimes = []
    courseCampus = inputCourse.campus
    courseCampusNumber = convertCampusModelToInt(courseCampus)
    #print "len newListoFmeetingtimes = " +  str(len(listofmeetingTimes))
    for i in range (0, len(listofmeetingTimes)):
	meetingTime = convertModelMeetingTimeToScheduleMeetingTime(listofmeetingTimes[i])
	#meetingTime = convertStringToMeetingTime(listofmeetingTimes[i])
	courseMeetingTimes.append(meetingTime)
    #print "aftermath ListoFmeetingtimes = " +  str(len(courseMeetingTimes))
    outputCourse = SchedulingCourse(courseInfo, id, courseMeetingTimes, courseCampusNumber)
    #print "aftermath len course's meetingTimes = " +  str(len(outputCourse.meetingTimes)) 
    return outputCourse

def convertCampusModelToInt(campus):
    if campus == "BRNBY":
	return 1
    if campus == "SURRY":
	return 2
    if campus == "VANCR" or campus == "GNWC" :
	return 3
    else :
	return 0

#converts a meeting time from the table into a meeting time object that we can use it in the scheduling algorithm
#Converts : meeting time from database --> meetingtime usable by scheduler
def convertModelMeetingTimeToScheduleMeetingTime(inputMeetingTime):   
    dayInteger = int(inputMeetingTime.weekday)
    #startTime = str(inputMeetingTime.start_time)
    startTime = inputMeetingTime.start_time
    startSlot = convertTimeToTimeSlot(startTime)
    #endTime = str(inputMeetingTime.end_time)
    endTime = inputMeetingTime.end_time
    endSlot = convertTimeToTimeSlot(endTime)
    outputMeetingTime = SchedulingMeetingTime(startSlot, endSlot, dayInteger)
    return outputMeetingTime


#Converts an input string into a date
def convertStringToDate(inputString):
    outputdate = datetime.strptime(inputString, '%Y-%m-%d')
    return outputdate
#Converts an imput string into a time object
def convertStringToTime(inputString):
    outputdate = datetime.strptime(inputString, '%H:%M:%S')
    return outputdate

#Convert Particular time to Timeslots
#See scheduler
def convertTimeToTimeSlot(intputTime):
    timeslot = intputTime.hour * 6
    timeslot += intputTime.minute /10
    return timeslot

#check to see if the coures conflicts with the schedule
def checkCourseConflict(course, schedule):
    for i in range (0, len(course.meetingTimes)):
        meetingTime = course.meetingTimes[i]
	#print "checkcourseconflict course title = " + str(course.title)
	#print "checkcourseconflict course id = " + str(course.courseID)
	#print "checkcourseconflict meetingtimes = " + str(course.meetingTimes)
        if (schedule.checkTimeWeekConflict(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday) == True):
            #print "I found a course conflict"
            return True
    return False

#locks a course into the schedule
#(time is locked and the course is added to locked courses)
def lockCourse(course, schedule, poolOfLockedCourses, poolOfPotentialCourses):
    #print "Locking Course"
    if (checkCourseConflict(course, schedule) == False):
        #print "There is no course Conflict for lock"
        # lock the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            #print "Locking MeetingTime"
            schedule.lockMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)
        poolOfLockedCourses.append(course)
        poolOfPotentialCourses.remove(course)

#unlocks the coures from the schedule (time is freed and the course is removed from locked courses)
def unlockCourse(course, schedule, poolOfLockedCourses, poolOfPotentialCourses):
    #print "unlockingCourse"
    if (checkCourseConflict(course, schedule) == True):
        #print "There is a conflict for unlock"
        # unlock/free the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            schedule.unlockMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)
        poolOfPotentialCourses.append(course)
        poolOfLockedCourses.remove(course)

#sets the course without any additional overhead
def setCourse(course, schedule):
    #print "Setting Course"
    if (checkCourseConflict(course, schedule) == False):
        #print "There is no conflict for set"
        # Set the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            schedule.setMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)

#frees the course with updating the respective list of courses
def freeCourse(course, schedule):
    #print "freeingupcourse"
    if (checkCourseConflict(course, schedule) == True):
	#print "There is a conflict for unlock"    	
	#print "There is no conflict"
        # unlock/free the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            schedule.unlockMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)

#find all courses that currently conflict with our schedule and remove them from the list of potential courses
def updateCleanPotentialCourses(poolOfPotentialCourses, poolOfCutCourses, schedule):
    listOfCoursesToDelete = []
    #build a list of courses for us to remove
    for i in range (0, len(poolOfPotentialCourses)):
        courseWeCheckOut = poolOfPotentialCourses[i]
        if checkCourseConflict(courseWeCheckOut, schedule) == True:
            listOfCoursesToDelete.append(courseWeCheckOut)
    #and remove them
    for i in range (0, len(listOfCoursesToDelete)):
        courseToDelete = listOfCoursesToDelete[i]
        poolOfPotentialCourses.remove(courseToDelete)
	poolOfCutCourses.append(courseToDelete)

#This is the central algorithm
# it requires:

#pool of courses the user is interested in
#pool of locked courses for a schedule
#a "schedule" object to handle the time grid
#the number of courses a student wants to take
def iterateBEHEMOTH(schedule, poolOfLockedCourses, poolOfPotentialCourses, poolOfCutCourses, maxSize):
    if len(poolOfLockedCourses) < maxSize:
	#print "interBehe We have the right size" 
        orignialTimeGap = schedule.getTotalTimeGap()
        originalNumberDays =  schedule.getTotalDays()
        updateCleanPotentialCourses(poolOfPotentialCourses, poolOfCutCourses, schedule);
        
        choiceStatsList = []
	
        if len(poolOfPotentialCourses) >= 2:
            #Gather information on all possible choices:
	    #First temporarily add the course to the schedule and gather stats about the new schedule
            for i in range (0, len(poolOfPotentialCourses)):
                schedule.clearSchedule()
                courseWeTryToAdd = poolOfPotentialCourses[i]
                setCourse(courseWeTryToAdd, schedule)
                #templockcourse
                #What about clear... set course, then clear again?
                #lockCourse(courseWeTryToAdd, schedule)
            
                newTotalDays = schedule.getTotalDays()
                newTotalTimeGap = schedule.getTotalTimeGap()
                currentChoiceStats = ChoiceStats(newTotalDays, newTotalDays)
                choiceStatsList.append(currentChoiceStats)
                #free certain course
                freeCourse(courseWeTryToAdd, schedule)
                schedule.clearSchedule()

            #try to make the best decision as to which course we should lock
            currentPositionOfChoice = 0
            currentBestChoiceStats = choiceStatsList[currentPositionOfChoice]

            #evaluate the stats of all potential courses we can add, and add the course that has the best stats
            for i in range (1, len(poolOfPotentialCourses)):
                currentChoiceStats = choiceStatsList[i]
                # find the best course
                if currentChoiceStats.changeNumberOfDays <= currentBestChoiceStats.changeNumberOfDays:
                    if currentChoiceStats.changeNumberOfDays < currentBestChoiceStats.changeNumberOfDays:
                        currentBestChoiceStats = currentChoiceStats;
                        currentPositionOfChoice = i;
                    elif (currentChoiceStats.changeTotalGap < currentBestChoiceStats.changeTotalGap):
                        currentBestChoiceStats = currentChoiceStats
                        currentPositionOfChoice = i
            #get the Course that has risen above all others and solidify its position in the schedule
            courseThatHasRisenAboveAllOthers = poolOfPotentialCourses[currentPositionOfChoice]
            #also make sure to update here....
            lockCourse(courseThatHasRisenAboveAllOthers, schedule, poolOfLockedCourses, poolOfPotentialCourses)

        elif len(poolOfPotentialCourses) == 1:
            onlyCourseOption = poolOfPotentialCourses[0]
	    lockCourse(onlyCourseOption, schedule, poolOfLockedCourses, poolOfPotentialCourses)

	
#Potentially obsolete code
#<MeetingTime: Monday - 10:30:00 to 12:20:00>
#parse string and turn it into a meetingtime
# same funcitonality of convertModelMeetingTimeToScheduleMeetingTime but ... instead uses a string instead of a 
def convertStringToMeetingTime(inputString):
    stringArray = shlex.split(inputString)
    #['<MeetingTime:', 'Monday', '-', '10:30:00', 'to', '12:20:00>']
    dayInteger = convertDayStringToDayInt(stringArray[1])
    #startTime = convertStringToTime(stringArray[3])
    startSlot = convertTimeToTimeSlot(startTime)
    endString = stringArray[5][:-1]
    endTime = convertStringToTime(endString)
    endSlot = convertTimeToTimeSlot(endTime)
    meetingTime = SchedulingMeetingTime(startSlot, endSlot, dayInteger)
    return meetingTime

def convertDayStringToDayInt(inputString):
    if inputString == "Monday":
        return 0
    elif inputString == "Tuesday":
        return 1
    elif inputString == "Wednesday":
        return 2
    elif inputString == "Thursday":
        return 3
    elif inputString == "Friday":
        return 4
    elif inputString == "Saturday":
        return 5
    elif inputString == "Sunday":
        return 6





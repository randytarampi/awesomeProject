#import schedule
from datetime import datetime
from schedule import *
from course import *
from choicestats import *
from scheduler/models import *
import shlex



#needs nubmer of coursees the student wants
# neeeds the number of courses
#we want to return a list of courses
#def somethingForRandyToUse(numberOfCourses, listofCourses):
    #iterateBEHEMOTH(schedule, poolOfLockedCourses, poolOfPotentialCourses, maxSize):
    #listofCourses = the input courses

    #course(subject, number, section) from model should get us 
#    schedule = Schedule()
#    poolOfLockedCourses = []
#    for i in range (0, numberOfCourses):
#        iterateBEHEMOTH(schedule, poolOfLockedCourses, listofCourses, numberOfCourses)
        
#    return poolOfLockedCourses

#def findBestChoice(

def functionForRandy(numberOfCourses, listofCourses):
    iterateBEHEMOTH(schedule, poolOfLockedCourses, poolOfPotentialCourses, maxSize)
    schedule = Schedule()
    poolOfLockedCourses = []
    newListOfCourses = []
    for i in range (0, len(listofCourses)):
        convertCourseModelToCourseObject(listofCourses[i])
        newListOfCourses.append(i)            
    for i in range (0, numberOfCourses):
        iterateBEHEMOTH(schedule, poolOfLockedCourses, newListOfCourses, numberOfCourses)

    outPutListOfCourses = []
    for i in range (0, len(poolOfLockedCourses)):
        outputCourse = Course.objects.get(id = poolOfLockedCourses[i].coursID)
        outPutListOfCourses.append(outputCourse)
    #outPutListOfCourses = []

    
    return poolOfLockedCourses

#We want to turn a course from a course object to a course model and vice versa
def convertCourseModelToCourseObject(inputCourse):
	
    id = inputCourse.id
    #<MeetingTime: Monday - 10:30:00 to 12:20:00>		
    listofmeetingTimes = MeetingTime.objects.filter(course = id)
    courseInfo = inputCourse.subject
    courseInfo += inputCourse.number
    courseMeetingTimes = []
    for i in range (0, len(listofmeetingTimes)):
        meetingTime = convertStringToMeetingTime(listofmeetingTimes[i])
        courseMeetingTimes.append(meetingTime)
    outputCourse = SchedulingCourse(courseInfo, id, courseMeetingTimes)
    return outputCourse
#<MeetingTime: Monday - 10:30:00 to 12:20:00>
#parse string and turn it into a meetingtime
def convertStringToMeetingTime(inputString):
    stringArray = shlex.split(inputString)
    #['<MeetingTime:', 'Monday', '-', '10:30:00', 'to', '12:20:00>']
    dayInteger = convertDayStringToDayInt(stringArray[1])
    startTime = convertStringToTime(stringArray[3])
    startSlot = convertTimeToTimeSlot(startTime)
    endString = stringArray[5][:-1]
    endTime = convertStringToTime(endString)
    endSlot = convertTimeToTimeSlot(endTime)
    #print dayInteger
    #print startTime
    #print endString
    meetingTime = MeetingTime(startSlot, endSlot, dayInteger)
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

#Converts an imput string into a date
def convertStringToDate(inputString):
    outputdate = datetime.strptime(inputString, '%Y-%m-%d')
    return outputdate
#Converts an imput string into a time object
def convertStringToTime(inputString):
    outputdate = datetime.strptime(inputString, '%H:%M:%S')
    return outputdate


#Convert Particular time to Timeslots
def convertTimeToTimeSlot(intputTime):
    timeslot = intputTime.hour * 6
    timeslot += intputTime.minute /10
    return timeslot

#check to see if the coures conflicts with the schedule
def checkCourseConflict(course, schedule):
    for i in range (0, len(course.meetingTimes)):
        meetingTime = course.meetingTimes[i]
        if (schedule.checkTimeWeekConflict(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday) == True):
            print "I found a course conflict"
            return True
    return False


def lockCourse(course, schedule, poolOfLockedCourses, poolOfPotentialCourses):
    print "Locking Course"
    if (checkCourseConflict(course, schedule) == False):
        print "There is no conflict"
        # lock the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            print "Locking MeetingTime"
            schedule.lockMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)
        poolOfLockedCourses.append(course)
        poolOfPotentialCourses.remove(course)
def unlockCourse(course, schedule, poolOfLockedCourses, poolOfPotentialCourses):
    print "unlockingCourse"
    if (checkCourseConflict(course, schedule) == True):
    #    print "There is no conflict"
        # unlock/free the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            schedule.unlockMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)
        poolOfPotentialCourses.append(course)
        poolOfLockedCourses.remove(course)
#sets the course without any additional overhead
def setCourse(course, schedule):
    print "Setting Course"
    if (checkCourseConflict(course, schedule) == False):
        print "There is no conflict"
        # Set the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            schedule.setMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)

#frees the course with updating the respective list of courses
def freeCourse(course, schedule):
    print "freeingupcourse"
    if (checkCourseConflict(course, schedule) == True):
    #print "There is no conflict"
        # unlock/free the course
        for i in range (0, len(course.meetingTimes)):
            meetingTime = course.meetingTimes[i]
            schedule.unlockMeetingTime(meetingTime.startTime, meetingTime.endTime, meetingTime.weekday)



#we need a pool of coursses

#poool of courses the user is interested in
#pool of courses for a schedule
#pool of locked courses for a schedule


#courses
#def generateCourses(poolofCourses):
    #cmpt 470 17:30-20:20 on tuesday
#    m470 = MeetingTime(105, 122, 1)
#    cmpt470 = Course("cmpt470", [])
    #addMTToSingleCourse(cmpt470, m470)
#    cmpt470.addMeetingTimes(m470)
#    cmpt470.title = "cmpt470"
#    poolofCourses.append(cmpt470)
    #cmpt 475 17:30-20:20 on wednesday
#    m475 = MeetingTime(105, 122, 2)
#    cmpt475 = Course("cmpt475", [])
#    cmpt475.addMeetingTimes(m475)
#    poolofCourses.append(cmpt475)
    #cmpt 320 14:30-19:20 on monday
#    m320 = MeetingTime(99, 116, 0)
#    cmpt320 = Course("cmpt320", [])
    #cmpt320.title = "cmpt320"
#    cmpt320.addMeetingTimes(m320)
#    poolofCourses.append(cmpt320)
    #cmpt 454 ,,, 2:30-4:20 on tuesday, 2:30-3:20 on thursday
#    m454n1 = MeetingTime(87, 98, 1)
#    m454n2= MeetingTime(87, 92, 3)
#    cmpt454 = Course("cmpt454", [])
    #cmpt454.title = "cmpt454"
#    cmpt454.addMeetingTimes(m454n1)
 #   cmpt454.addMeetingTimes(m454n2)
 #   poolofCourses.append(cmpt454)
    #cmpt 308, 2:30-4:20 on tuesday, 2:30-3:20 on thursday
 #   m308n1 = MeetingTime(87, 98, 1)
  #  m308n2= MeetingTime(87, 92, 3)
 #   cmpt308 = Course("cmpt308", [])
    #cmpt308.title = "cmpt308"
#    cmpt308.addMeetingTimes(m308n1)
#    cmpt308.addMeetingTimes(m308n2)
 #   poolofCourses.append(cmpt308)
    #cmpt 411, 2:30-4:20 on monday, 2:30-3:20 on wednesday
 #   m411n1 = MeetingTime(87, 98, 0)
 #   m411n2 = MeetingTime(87, 92, 2)
 #   cmpt411 = Course("cmpt411", [])
    #cmpt411.title = "cmpt411"
 #   cmpt411.addMeetingTimes(m411n1)
 #   cmpt411.addMeetingTimes(m411n2)
 #   poolofCourses.append(cmpt411)

#find all courses that currently conflict with our schedule and remove them from the list of potential courses
def updateCleanPotentialCourses(poolOfPotentialCourses, schedule):
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

    

#listofPossisbleCourses = 

def iterateBEHEMOTH(schedule, poolOfLockedCourses, poolOfPotentialCourses, maxSize):
    if len(poolOfLockedCourses) < maxSize:
        orignialTimeGap = schedule.getTotalTimeGap()
        originalNumberDays =  schedule.getTotalDays()
        updateCleanPotentialCourses(poolOfPotentialCourses, schedule);
        
        choiceStatsList = []
	
        if len(poolOfPotentialCourses) > 2:
            #Gather information on all possible choices, by seeing what the new schedules would be like
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

            #try to make the best decision
            currentPositionOfChoice = 0
            currentBestChoiceStats = choiceStatsList[currentPositionOfChoice]

            #try ou every potential course that can make a good fit here
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
            #also make sure to update course lists here...
            lockCourse(onlyCourseOption, schedule, poolOfLockedCourses, poolOfPotentialCourses)


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


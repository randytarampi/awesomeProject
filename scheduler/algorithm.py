#import schedule
import shlex
import copy
from datetime import datetime
from scheduler.schedule import *
from scheduler.course import *
from scheduler.choicestats import *
from scheduler.models import *
from scheduler.datetimeconverter import *
#=======================================================================
# Main function
# takes the number of courses the student is willing to take,
# a list of courses the student wants to take,
# a list of times the student is not available,
# and an optional list of course that the student (NEEDS) more severe than wants to take
#=======================================================================
def createOptimalSchedule(numberOfCourses, listofWantsCourses, unavailableMeetingTimes, listofNeedsCourses = []):
	schedule = Schedule()
   	newListOfNeedsCourses = []
	newListOfWantsCourses = []
    	poolOfCutCourses = []
	if listofNeedsCourses != []:
		for i in range (0, len(listofNeedsCourses)):
			newCourse = convertCourseModelToCourseObject(listofNeedsCourses[i])
				#This handles labs and appends the course
			handleLabsForCourse(newCourse, newListOfNeedsCourses)

    	for i in range (0, len(listofWantsCourses)):
		newCourse = convertCourseModelToCourseObject(listofWantsCourses[i])	
		handleLabsForCourse(newCourse, newListOfWantsCourses)


	#Handle unavailable times
	handleUnavailableMeetingTimes(unavailableMeetingTimes, schedule)
	
	#Handle needs, find top picks for course options
	if listofNeedsCourses != []:
		needAlgorithmOutputs = completePasturize(newListOfNeedsCourses, schedule, numberOfCourses)
		needAlgorithmTopChoices = needAlgorithmOutputs[0]
		needAlgorithmCutCourses = needAlgorithmOutputs[1]
		topNeedsCoursePicks = findPasturizeTopPickDarwinism(needAlgorithmTopChoices, schedule)
		pasturizeActOnTopPick(topNeedsCoursePicks, schedule, numberOfCourses)
		for i in range (0, len(needAlgorithmCutCourses)):
			schedule.poolOfCutCourses.append(needAlgorithmCutCourses[i])
	#handle wants
    	for i in range (0, numberOfCourses):
        	iterateBEHEMOTH(schedule, newListOfWantsCourses, numberOfCourses)
    	outPutListOfLockedCourses = []
    	

	#everythingElse
	unUsedCourseList = []	
	for i in range (0, len(newListOfNeedsCourses)):
		unUsedCourseList.append(newListOfNeedsCourses[i])
	for i in range (0, len(unUsedCourseList)):
		unUsedCourse = unUsedCourseList[i]
		schedule.poolOfCutCourses.append(unUsedCourse)
		newListOfNeedsCourses.remove(unUsedCourse)
	unUsedCourseList = []
	for i in range (0, len(newListOfWantsCourses)):
		unUsedCourseList.append(newListOfWantsCourses[i])
	for i in range (0, len(unUsedCourseList)):
		unUsedCourse = unUsedCourseList[i]
		schedule.poolOfCutCourses.append(unUsedCourse)
		newListOfWantsCourses.remove(unUsedCourse)

	#Locked meeting times
	listMeetingTimes = []
	for i in range (0, len(schedule.poolOfLockedCourses)):
		meetingTimes = schedule.poolOfLockedCourses[i].meetingTimes
		for j in range (0, len(meetingTimes)):
			meetingTime = meetingTimes[j]
			listMeetingTimes.append(meetingTime)
	#Locked Courses
	for i in range (0, len(schedule.poolOfLockedCourses)):
		lockedCourse = schedule.poolOfLockedCourses[i]
		outputCourse = lockedCourse.dataBaseCourse		
       		outPutListOfLockedCourses.append(outputCourse)


	
	#Cut MeetingTimes
	listCutMeetingTimes = []
	for i in range (0, len(schedule.poolOfCutCourses)):
		meetingTimes = schedule.poolOfCutCourses[i].meetingTimes
		for j in range (0, len(meetingTimes)):
			meetingTime = meetingTimes[j]
			listCutMeetingTimes.append(meetingTime)

	#Cut Courses
	#Possible fix to insufficient number of cut classes
    	outPutListOfCutCourses = []
	for i in range (0, len(schedule.poolOfCutCourses)):
		cutCourse = schedule.poolOfCutCourses[i]
		outputCourse = cutCourse.dataBaseCourse
		outPutListOfCutCourses.append(outputCourse)
	
	
	#Schedule Stats
	TotalDays = schedule.getTotalDays()
    	TotalTimeGap = schedule.getTotalTimeGap()
    	crossCampusTravels = schedule.getTotalCrossCampusTravels()
    	currentChoiceStats = ChoiceStats(TotalDays, TotalTimeGap, crossCampusTravels, len(outPutListOfLockedCourses))

	
	#Oputput will be [meetingTimesInSchedule, Courses in schedule, meetingTimes not used , courses not used,  schedulestats, schedule]
	largerOutputArray = []	
	largerOutputArray.append(listMeetingTimes)
	largerOutputArray.append(outPutListOfLockedCourses)
	largerOutputArray.append(listCutMeetingTimes)
	largerOutputArray.append(outPutListOfCutCourses)
    	largerOutputArray.append(currentChoiceStats)
    	largerOutputArray.append(schedule)
	
    	return largerOutputArray

#==================================================================================================
#Main Function helpers
#===================================================================================================

#lock down every listed unavailable time to a certain point...
def handleUnavailableMeetingTimes(unavailableMeetingTimes, schedule):
	
	#if a student is busy from 8:30-9:30, they can still take 9:30 classes
	for i in range(0, len(unavailableMeetingTimes)):
		unavailableMeetingTime = unavailableMeetingTimes[i]	
		weekday = unavailableMeetingTime[0]	
		startTime = convertTimeToTimeSlot(unavailableMeetingTime[1])
		endTime = convertTimeToTimeSlot(unavailableMeetingTime[2])
		schedule.lockMeetingTimeUnavailable(startTime, endTime, weekday)


#Handles multiple labs for a course
#by creating a clone of that course for each lab
def handleLabsForCourse(inputCourse, listofCourses):
	if len(inputCourse.labs) != 0:
		for i in range (0, len(inputCourse.labs)):
			testcourse = copy.deepcopy(inputCourse)
			testcourse.addMeetingTime(inputCourse.labs[i])
			listofCourses.append(testcourse)
	else:
		listofCourses.append(inputCourse)
		

#Turns a course model object into a course object that we can use in the scheduler
#Converts : course from database --> course usable by scheduler
def convertCourseModelToCourseObject(inputCourse):
    	id = inputCourse.id		
    	listofmeetingTimes = MeetingTime.objects.filter(course = id)
    	courseInfo = inputCourse.subject
    	courseInfo += inputCourse.number
  	courseMeetingTimes = []
  	courseCampus = inputCourse.campus
  	courseCampusNumber = convertCampusModelToInt(courseCampus)
  	courseExam = []
  	courseLabs = []
  	for i in range (0, len(listofmeetingTimes)):
		meetingTime = listofmeetingTimes[i]
		if (meetingTime.type == "EXAM"):
	    		courseExam.append(meetingTime)
		elif (meetingTime.type == "LAB"):
	    		courseLabs.append(meetingTime)
		else:
	    		courseMeetingTimes.append(meetingTime)
	outputCourse = SchedulingCourse(courseInfo, id, courseMeetingTimes, courseExam, courseLabs, courseCampusNumber, inputCourse)
	return outputCourse
    
#Converts the input campus into an integer value that is recognized by the schedule
def convertCampusModelToInt(campus):
	if campus == "BRNBY":
		return 1
    	elif campus == "SURRY":
		return 2
   	elif campus == "VANCR" or campus == "GNWC":
		return 3
 	else :
		return 0

#Convert Particular time to Timeslots
#See scheduler
def convertTimeToTimeSlot(intputTime):
	timeslot = intputTime.hour * 6
 	timeslot += intputTime.minute /10
   	return timeslot



#===================================================================================================
#Course and Time Conflicts
#===================================================================================================


def checkCourseConflict(course, schedule):
	if courseExamConflict(course, schedule.poolOfLockedCourses) == True:
		return True
	else:
    		if checkCourseTimeConflict(course, schedule) == True:
	    		return True
	return False


#Checks if a courses' exams will conflict with another list of courses' exams
def courseExamConflict(course, listOfLockedCourses):
	for i in range (0, len(listOfLockedCourses)):
	    	lockedCourse = listOfLockedCourses[i]
	    	for j in range (0, len(course.exams)):
	    		courseExam = course.exams[j]
			for k in range (0, len(lockedCourse.exams)):
		    		lockedCourseExam = lockedCourse.exams[k]
		    		if examConflict(courseExam, lockedCourseExam) == True:
					return True
	return False


#check to see if the course conflicts with the schedule
def checkCourseTimeConflict(course, schedule):
	campus = course.campus
    	for i in range (0, len(course.meetingTimes)):
        	meetingTime = course.meetingTimes[i]
		startTime = convertTimeToTimeSlot(meetingTime.start_time)
		endTime = convertTimeToTimeSlot(meetingTime.end_time)
		if (schedule.checkTimeWeekConflictCampus(startTime, endTime, meetingTime.weekday, campus) == True):
        	#print "I found a course conflict"
            		return True
    	return False


#checks if a db course conflicts with a set of meeting Times
#returns the meeting times of the course....
#if it is an empty list we coudln't get the course to fit


def courseFitsWithMeetingTimeList(dbCourse, meetingTimeList):
	algorithmCourse = convertCourseModelToCourseObject(dbCourse)
	return courseFromAlgorithmFitsWithMeetingTimeList(algorithmCourse, meetingTimeList)
	
def courseFromAlgorithmFitsWithMeetingTimeList(course, meetingTimeList):
	outPutAppropriateTimes = []	
	lectureMeetingTimes = course.meetingTimes
	#Check that all of the lecture times of the course will fit with the times we are using
	#if the lecture times all work, add the lecture tiems to the output times to te output, otherwise return empty list
	if  meetingTimesListConflict(lectureMeetingTimes, meetingTimeList) == False:
		for i in range (0, len(lectureMeetingTimes)):
			outPutAppropriateTimes.append(lectureMeetingTimes[i])		
	else:
		print "courseFitsWithMeetingTimeList lecture conflict"
		return []
	#Handle the exam times: all of them have to work (fit in the schedule)
	examTimes = course.exams
	if examTimes != []:
		if  meetingTimesListConflict(examTimes, meetingTimeList) == False:
			for i in range (0, len(examTimes)):
				outPutAppropriateTimes.append(examTimes[i])		
		else:
			print "courseFitsWithMeetingTimeList Exam conflict"
			return []	
	#Handle the lab times: at least One has to work (fit in the schedule)	
	labTimes = course.labs
	if labTimes != []:
		acceptableLabTimes = meetingTimesFilter(meetingTimeList, labTimes)
		if len (acceptableLabTimes) != 0:
			for i in range (0, len(acceptableLabTimes)):
				outPutAppropriateTimes.append(acceptableLabTimes[i])
		else:
			print "courseFitsWithMeetingTimeList lab conflict"
			return []
	#return what we have	
	return outPutAppropriateTimes

#Checks if there is a conflict between two lists of meeting times
def meetingTimesListConflict(firstListOfMeetingTimes, secondListOfMeetingTimes):
	for i in range (0, len(firstListOfMeetingTimes)):
	    	meetingTimeOne = firstListOfMeetingTimes[i]
	    	for j in range (0, len(secondListOfMeetingTimes)):
	    		meetingTimeTwo = secondListOfMeetingTimes[j]
			#This function works for all courses
	    		if meetingTimesConflict(meetingTimeOne, meetingTimeTwo) == True:
				return True
	return False

#Compares two list of meeting times
#It finds out if the newSetOfTimes, can be used without conflicting with the old times
#If there is a conflict, the function will return an empty list
def meetingTimesFilter(oldTimesList, newTimesList):
	listOfNonConflictingNewTimes = []
	#For each new time 
	for i in range (0, len(newTimesList)):
	    	newTime = newTimesList[i]
		if meetingTimeConflictWithList(newTime, oldTimesList) == False:
			listOfNonConflictingNewTimes.append(newTime)
	return listOfNonConflictingNewTimes

#Checks if a single meeting time conflicts with a list of meeting times
def meetingTimeConflictWithList(meetingTimeOne, meetingTimeList):
	for i in range (0, len(meetingTimeList)):
		meetingTimeTwo = meetingTimeList[i]
		if meetingTimesConflict(meetingTimeOne, meetingTimeTwo) == True:
			return True
	return False

#checks if two meeting times conflict
def meetingTimesConflict(firstMeetingTime, secondMeetingTime):
	if (firstMeetingTime.weekday == secondMeetingTime.weekday):
		if examConflict(firstMeetingTime, secondMeetingTime) == True:
			return True
		else:
			return False
	return False
	
#Checks if two exams will conflict... 
#also works for two meeting times
def examConflict(examOne, examTwo):
    	if datetimeconflict(examOne.start_day, examOne.end_day, examTwo.start_day, examTwo.end_day) == True:
		exam1StartTime = convertTimeToTimeSlot(examOne.start_time)
		exam1EndTime = convertTimeToTimeSlot(examOne.end_time)
		exam2StartTime = convertTimeToTimeSlot(examTwo.start_time)
		exam2EndTime = convertTimeToTimeSlot(examTwo.end_time)
		if timeConflict(exam1StartTime, exam1EndTime, exam2StartTime, exam2EndTime) == True:
	    		return True
		else:
	    		return False
    	else:
		return False   



#===================================================================================================
#
#Schedule access and utility functions (allow us to modify the schedule)
#
#===================================================================================================


#locks a course into the schedule
#(time is locked and the course is added to locked courses)
def lockCourse(course, schedule, poolOfPotentialCourses):
    	#print "Locking Course"
	if (checkCourseConflict(course, schedule) == False):
        	#print "There is no course Conflict for lock"
        	# lock the course
		campus = course.campus
		#print "lockCourse - course campus = " + str(campus)
        	for i in range (0, len(course.meetingTimes)):
            		meetingTime = course.meetingTimes[i]
			startTime = convertTimeToTimeSlot(meetingTime.start_time)
			endTime = convertTimeToTimeSlot(meetingTime.end_time)
			schedule.lockMeetingTimeCampus(startTime, endTime, meetingTime.weekday, campus)
        	schedule.poolOfLockedCourses.append(course)
        	poolOfPotentialCourses.remove(course)
    	else:
		print "failed to lock course"

#unlocks the coures from the schedule (time is freed and the course is removed from locked courses)
def unlockCourse(course, schedule, poolOfPotentialCourses):
    	if (checkCourseConflict(course, schedule) == True):
		campus = course.campus
        	for i in range (0, len(course.meetingTimes)):
            		meetingTime = course.meetingTimes[i]
			startTime = convertTimeToTimeSlot(meetingTime.start_time)
			endTime = convertTimeToTimeSlot(meetingTime.end_time)
			schedule.unlockMeetingTimeCampus(startTime, endTime, meetingTime.weekday, campus)
        	poolOfPotentialCourses.append(course)
        	schedule.poolOfLockedCourses.remove(course)

#sets the course without any additional overhead
def setCourse(course, schedule):
    	if (checkCourseConflict(course, schedule) == False):
		campus = course.campus
        	for i in range (0, len(course.meetingTimes)):
            		meetingTime = course.meetingTimes[i]
			startTime = convertTimeToTimeSlot(meetingTime.start_time)
			endTime = convertTimeToTimeSlot(meetingTime.end_time)
			schedule.setMeetingTimeCampus(startTime, endTime, meetingTime.weekday, campus)

#frees the course with updating the respective list of courses
def freeCourse(course, schedule):
	campus = course.campus
        for i in range (0, len(course.meetingTimes)):
		meetingTime = course.meetingTimes[i]
		startTime = convertTimeToTimeSlot(meetingTime.start_time)
		endTime = convertTimeToTimeSlot(meetingTime.end_time)
		schedule.unlockMeetingTimeCampus(startTime, endTime, meetingTime.weekday, campus)



#===================================================================================================
#
#Want Algorithm and support functions
#
#===================================================================================================


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
		schedule.poolOfCutCourses.append(courseToDelete)
        	poolOfPotentialCourses.remove(courseToDelete)


    
#Eliminates all duplicate courses 
#i.e. if are taking cmpt 300 already... it will delete any other mentions of cmpt 300 from the potential list
def eliminateDuplicateCourses(poolOfPotentialCourses, schedule):
    	listOfCoursesToDelete = []
   	#build a list of courses for us to remove
    	for i in range (0, len(poolOfPotentialCourses)):	
		for j in range (0, len(schedule.poolOfLockedCourses)):
	    		if courseNameConflict(poolOfPotentialCourses[i], schedule.poolOfLockedCourses[j]) == True:
				listOfCoursesToDelete.append(poolOfPotentialCourses[i])
	
    	#and remove them
    	for i in range (0, len(listOfCoursesToDelete)):
        	courseToDelete = listOfCoursesToDelete[i]
		schedule.poolOfCutCourses.append(courseToDelete)
        	poolOfPotentialCourses.remove(courseToDelete)
		
#check if two courses have the same name
def courseNameConflict(courseOne, courseTwo):
	if courseOne.title == courseTwo.title:
		return True
	else:
		return False


#Algorithm for Want
#--------------------------------------------

#This is the central algorithm for wants
# it requires:
	#pool of courses the user is interested in
	#pool of locked courses for a schedule
	#a "schedule" object to handle the time grid
	#the number of courses a student wants to take

def iterateBEHEMOTH(schedule, poolOfPotentialCourses, maxSize):
	"""
	Takes a schedule, a pool of courses, and a max size
	Fills the schedule with an optimal set of courses of max size 
	that are a subset of the pool of courses
	"""   	
	if len(schedule.poolOfLockedCourses) < maxSize:
        	orignialTimeGap = schedule.getTotalTimeGap()
        	originalNumberDays =  schedule.getTotalDays()
		eliminateDuplicateCourses(poolOfPotentialCourses, schedule)#eliminate duplicate courses
        	updateCleanPotentialCourses(poolOfPotentialCourses, schedule)#eliminate other courses that conflict with the schedule
        	
		#if we have more than one option, we need to find the best option
        	if len(poolOfPotentialCourses) >= 2:
			choiceStatsList = []
            		#Gather information on all possible choices:
            		for i in range (0, len(poolOfPotentialCourses)):
				#First temporarily add the course to the schedule
                		courseWeTryToAdd = poolOfPotentialCourses[i]
                		setCourse(courseWeTryToAdd, schedule)
				# and gather stats about the new schedule
                		newTotalDays = schedule.getTotalDays()
                		newTotalTimeGap = schedule.getTotalTimeGap()
				newCrossCampusTravels = schedule.getTotalCrossCampusTravels()
                		currentChoiceStats = ChoiceStats(newTotalDays, newTotalTimeGap, newCrossCampusTravels, 1)
               			choiceStatsList.append(currentChoiceStats)
                		#free the course and clean up
                		freeCourse(courseWeTryToAdd, schedule)
			
			#evaluate the information you gathered on the choices to find the best decision 			
            		currentPositionOfChoice = 0
            		currentBestChoiceStats = choiceStatsList[currentPositionOfChoice]

            		#evaluate the stats of all potential courses we can add, and add the course that has the best stats
            		for i in range (1, len(poolOfPotentialCourses)):
                		currentChoiceStats = choiceStatsList[i]
                		# if the course has "better" stats, it becomes the new "best" option
                		if currentChoiceStats.numberOfDays <= currentBestChoiceStats.numberOfDays:
                    			if currentChoiceStats.numberOfDays < currentBestChoiceStats.numberOfDays:
                        			currentBestChoiceStats = currentChoiceStats;
                        			currentPositionOfChoice = i;
                    			elif (currentChoiceStats.crossCampusTravels <= currentBestChoiceStats.crossCampusTravels):
						if (currentChoiceStats.crossCampusTravels < currentBestChoiceStats.crossCampusTravels):
                            				currentBestChoiceStats = currentChoiceStats
                            				currentPositionOfChoice = i
		    				elif (currentChoiceStats.totalGap < currentBestChoiceStats.totalGap):
                            				currentBestChoiceStats = currentChoiceStats
                            				currentPositionOfChoice = i
			#Lock the course that has been determined to by the best choice
            		courseThatHasRisenAboveAllOthers = poolOfPotentialCourses[currentPositionOfChoice]
            		lockCourse(courseThatHasRisenAboveAllOthers, schedule, poolOfPotentialCourses)
		#if we only have one option, then just lock the course into the schedule
        	elif len(poolOfPotentialCourses) == 1:
            		onlyCourseOption = poolOfPotentialCourses[0]
	    		lockCourse(onlyCourseOption, schedule, poolOfPotentialCourses)

	else:
		print "Maxed out on behe interation numbers"

#=======================================================================================================
#Algorithms for Need
#=======================================================================================================



def regroupCoursesForPasturize(inputCoursesList):
	"""
	divide everything into groups based on the course title
	"""
	#Find out what the different titles of the courses are	
	listOfCourseTitles = []
	for i in range (0, len(inputCoursesList)):
		inputCourse = inputCoursesList[i]
		if inputCourse.title not in listOfCourseTitles:
			listOfCourseTitles.append(inputCourse.title)
	#From this we know how many groups we need to divide our input courses into	
	numberOfGroups = len(listOfCourseTitles)
	
	#We gotta have a list of lists for each course
	properlyOrganizedCourseGroupList = []
	for i in range (0, numberOfGroups):
		properlyOrganizedCourseGroupList.append([])

	#divide the courses into their proper groups
	for i in range (0, len(inputCoursesList)):
		inputCourse = inputCoursesList[i]
		groupNumber = listOfCourseTitles.index(inputCourse.title)
		properlyOrganizedCourseGroupList[groupNumber].append(inputCourse)
	#we should now have a group of properly organized courses
	return properlyOrganizedCourseGroupList


#number of courses that we need to add...
def completePasturize(inputCoursesList, schedule, numberOfCourses):
	"""
	Pasturize algorithm, finds courses that would make an optimal schedule
	"""
	regroupedCourses = regroupCoursesForPasturize(inputCoursesList)
	numberOfGroups = len(regroupedCourses)
	outPutList = []
	
	newList = []
	oldList = [[]]
	cutCourses = []
	for i in range (0, numberOfGroups):
		print "Start iteration of Pasturize, size of oldList = " + str(len(oldList))
		newList = handleOneIterationOfPasturize(regroupedCourses[i], oldList, schedule)
		if newList != []:
			oldList = newList
		else:
			cutCourses.append(regroupedCourses[i][0])
		print "End iteration of Pasturize, size of oldList = " + str(len(oldList))
	outPutList.append(oldList)
	outPutList.append(cutCourses)
	print "completePasturize len(outPutList)"
	return outPutList


def handleOneIterationOfPasturize(attemptedAddedCourseList, inputCoursePairingList, schedule):
	"""
	Uses a list of pairings of courses and a list of additional courses 

	THe list of pairings of courses represent all possible schedules of size N that we have so far
	
	For each pairing of courses, it will to find any courses from the other list that do not conflict
	It will append the courses that do not conflict to the pairing, giving a potential schedule of size N+
	"""
	outputList = []	
	#For each pairing
	for i in range (0, len(inputCoursePairingList)):
		inputCoursePairing = inputCoursePairingList[i]
		#for each course...
		for j in range (0, len(attemptedAddedCourseList)):
			courseWeAttemptToAdd = attemptedAddedCourseList[j]
			if checkCourseConflictsWithPairing(courseWeAttemptToAdd, inputCoursePairing, schedule) == False:
				#testcourse = copy.deepcopy(inputCourse)
				newCoursePairing = copy.deepcopy(inputCoursePairing)
				newCoursePairing.append(courseWeAttemptToAdd)
				outputList.append(newCoursePairing)
	#THis should be our new listofCoursePairings for future iterations	
	return outputList



#number of courses that we need to add...
def completePasturizeExtraHeavy(inputCoursesList, schedule):
	regroupedCourses = regroupCoursesForPasturize(inputCoursesList)
	numberOfGroups = len(regroupedCourses)
	potentialOutPutList = []
	newList = []
	oldList = [[]]
	for i in range (0, numberOfGroups):
		print "Start iteration of Pasturize, size of oldList = " + str(len(oldList))
		newList = handleOneIterationOfPasturizeExtraHeavy(regroupedCourses[i], oldList, schedule)
		oldList = newList
		#oldList = 
		print "End iteration of Pasturize, size of oldList = " + str(len(oldList))
	return oldList

def handleOneIterationOfPasturizeExtraHeavy(attemptedAddedCourseList, inputCoursePairingList, schedule):
	outputList = []	
	#For each pairing
	for i in range (0, len(inputCoursePairingList)):
		inputCoursePairing = inputCoursePairingList[i]
		#for each course...
		for j in range (0, len(attemptedAddedCourseList)):
			courseWeAttemptToAdd = attemptedAddedCourseList[j]
			if checkCourseConflictsWithPairing(courseWeAttemptToAdd, inputCoursePairing, schedule) == False:
				newCoursePairing = copy.deepcopy(inputCoursePairing)
				newCoursePairing.append(courseWeAttemptToAdd)
				outputList.append(newCoursePairing)
			else:
				outputList.append(inputCoursePairing)
	#THis should be our new listofCoursePairings for future iterations	
	return outputList


def checkCourseConflictsWithPairing(inputCourse, inputPairingOfCourses, schedule):
	"""
	Checks if a course can 'fit in' with another set of courses, 
	by not conflicting with them

	"""
	listCoursesToUnlock = []
	originalPairingLength = len(inputPairingOfCourses)
	#inputPairingOfCoursesClone = copy.deepcopy(inputPairingOfCourses)

	for i in range (0, originalPairingLength):
		#We choose 0 every time because the list is shrinking
		pairedCourse = inputPairingOfCourses[0]
		lockCourse(pairedCourse, schedule, inputPairingOfCourses)
		listCoursesToUnlock.append(pairedCourse)
	outputBoolean = checkCourseConflict(inputCourse, schedule)
	for i in range (0, originalPairingLength):
		pairedCourse = listCoursesToUnlock[i] 
		unlockCourse(pairedCourse, schedule, inputPairingOfCourses)
	return outputBoolean


				
def findPasturizeTopPickDarwinism(listOfPotentialSchedules, schedule):
	"""
	Finds the best solution out of the picks we have
	"""
	numberOfOptions = len(listOfPotentialSchedules)
	#gather stats
	listOfOptionsStats = []
	if numberOfOptions >= 1:	
		for i in range (numberOfOptions):
			currentOptionOfCourses = listOfPotentialSchedules[i]
			currentStats = gatherStatsOnPotentialCourseSchedule(currentOptionOfCourses, schedule)
			listOfOptionsStats.append(currentStats)

	#evaluate stats
	#only use options with the greatest number of options
	bestOptionNumber = evaluateStatsForPasturize(listOfOptionsStats, schedule)
	bestCourseOption = listOfPotentialSchedules[bestOptionNumber]
	#Act on those stats
	bestCourseOptionClone = copy.deepcopy(bestCourseOption)
	return bestCourseOption
	
#gather stats for pasturize
def gatherStatsOnPotentialCourseSchedule(potentialCourses, schedule):
	"""
	Finds the stats of all possible sets of courses outputted by the pasturize algorithm
	"""
	for i in range (0, len(potentialCourses)):
		courseWeWantToSet = potentialCourses[i]
		setCourse(courseWeWantToSet, schedule)
	#get the stats 
	newTotalDays = schedule.getTotalDays()
	newTotalTimeGap = schedule.getTotalTimeGap()
	newCrossCampusTravels = schedule.getTotalCrossCampusTravels()
	currentChoiceStats = ChoiceStats(newTotalDays, newTotalTimeGap, newCrossCampusTravels, len(potentialCourses))
	#choiceStatsList.append(currentChoiceStats)
		#free certain course
	for i in range (0, len(potentialCourses)):
		courseWeWantToFree = potentialCourses[i]
		freeCourse(courseWeWantToFree, schedule)
	return currentChoiceStats

#evaluate stats for pasturize 
# and returns what it believes to be the "best" schedule
def evaluateStatsForPasturize(listOfOptionsStats, schedule):
	#try to make the best decision as to which course we should lock
    	currentPositionOfChoice = 0
    	currentBestChoiceStats = listOfOptionsStats[currentPositionOfChoice]
	
	for i in range (1, len(listOfOptionsStats)):
        	currentChoiceStats = listOfOptionsStats[i]
        	# find the best course
		if currentChoiceStats.numberOfCourses >= currentBestChoiceStats.numberOfCourses:
			if currentChoiceStats.numberOfCourses > currentBestChoiceStats.numberOfCourses:
				currentBestChoiceStats = currentChoiceStats;
				currentPositionOfChoice = i;
			else:
				if currentChoiceStats.numberOfDays <= currentBestChoiceStats.numberOfDays:
			    		if currentChoiceStats.numberOfDays < currentBestChoiceStats.numberOfDays:
						currentBestChoiceStats = currentChoiceStats;
						currentPositionOfChoice = i;
			    		elif (currentChoiceStats.crossCampusTravels <= currentBestChoiceStats.crossCampusTravels):
						if (currentChoiceStats.crossCampusTravels < currentBestChoiceStats.crossCampusTravels):
				    			currentBestChoiceStats = currentChoiceStats
				    			currentPositionOfChoice = i
			    			elif (currentChoiceStats.totalGap < currentBestChoiceStats.totalGap):
				    			currentBestChoiceStats = currentChoiceStats
	#this is the best choice we made
	return currentPositionOfChoice
    
#Essentially this just locks courses 
#that we've already determined to be optimal into the schedule	
def pasturizeActOnTopPick(topCoursesPicks, schedule, NumberOfCourses):
	bestCourseOption = topCoursesPicks
	#Act on those stats
	bestCourseOptionClone = copy.deepcopy(bestCourseOption)
	for i in range (0, len (bestCourseOption)):
		#we lock 0 here because the list gets smaller.. it moves...
		if i < NumberOfCourses:
			lockCourse(bestCourseOption[0], schedule, bestCourseOption)


		

#Potentially obsolete code
#<MeetingTime: Monday - 10:30:00 to 12:20:00>
#parse string and turn it into a meetingtime
# same funcitonality of convertModelMeetingTimeToScheduleMeetingTime but ... instead uses a string instead of a 


#handles courses we need to take
#Potential issue!
#Say hte user wants to take cmpt 300, and we are passed all sections of cmpt 300
#This means I should group up all the sections of cmpt 300 together into one list
#NOT DONE
#Converts an input string into a date




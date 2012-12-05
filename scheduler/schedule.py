#Schedule.py

class Schedule:
    #def __init__(self):  
   	mondayS = [0] * 144
   	tuesdayS = [0] * 144
   	wednesdayS = [0] * 144
   	thursdayS = [0] * 144
   	fridayS = [0] * 144
   	saturdayS = [0] * 144
   	sundayS = [0] * 144
	poolOfLockedCourses = []
	poolOfCutCourses = []
	#TimeSlotAvailability
   	def __init__(self):  
   		self.mondayS = [0] * 144
   		self.tuesdayS = [0] * 144
   		self.wednesdayS = [0] * 144
   		self.thursdayS = [0] * 144
   		self.fridayS = [0] * 144
   		self.saturdayS = [0] * 144
   		self.sundayS = [0] * 144
		self.poolOfLockedCourses = []
		self.poolOfCutCourses = []


    #i.e. input 0 to get monday, 1 to get tuesday... 6 to get sunday
	def convertWeekDayToProperArray(self, weekday):
		if weekday ==0:
		    	return self.mondayS
		elif weekday ==1:
		    	return self.tuesdayS
		elif weekday ==2:
		    	return self.wednesdayS
		elif weekday ==3:
		   	 return self.thursdayS
		elif weekday ==4:
		   	 return self.fridayS
		elif weekday ==5:
		  	 return self.saturdayS
		elif weekday ==6:
		  	 return self.sundayS
	#checks if the given time conflits with the schedule
	def checkTimeWeekConflictCampus(self, startTime, endTime, weekday, campus):
		return checkIfTimeDayConflict(startTime, endTime, self.convertWeekDayToProperArray(weekday), campus)
    	#Locks slots start-->end, on the given workday
    	def lockMeetingTime(self, startTime, endTime, weekday):
        	lockSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))
	#basically just like lock meeting time but it only locks 
	def lockMeetingTimeUnavailable(self, startTime, endTime, weekday):
        	lockSlotThroughUnavailable(startTime, endTime, self.convertWeekDayToProperArray(weekday))
	def lockMeetingTimeCampus(self, startTime, endTime, weekday, campus):
        	lockSlotThroughCampus(startTime, endTime, self.convertWeekDayToProperArray(weekday), campus)
   	 #Frees slots start-->end, on the given workday
	def unlockMeetingTime(self, startTime, endTime, weekday):
		unlockSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))
	def unlockMeetingTimeCampus(self, startTime, endTime, weekday, campus):
		unlockSlotThroughCampus(startTime, endTime, self.convertWeekDayToProperArray(weekday), campus)
	#Sets slots start-->end, on the given workday
	def setMeetingTime(self, startTime, endTime, weekday):
		setSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))
	def setMeetingTimeCampus(self, startTime, endTime, weekday, campus):
		setSlotThroughCampus(startTime, endTime, self.convertWeekDayToProperArray(weekday), campus)
	
	def freeMeetingTime(self, startTime, endTime, weekday):
		freeSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))


	def getTotalTimeGap(self):
		weekTotalTimeGap = 0
		for i in range (0, 7):
			weekTotalTimeGap += getTimeGapForDay(self.convertWeekDayToProperArray(i))
		return weekTotalTimeGap
	def getTotalDays(self):
		totalDays = 0
		listtocompare = [1, 2, 4, 5, 7,8,10,11]
		#for i in range (0, 7):
		#	if len(list(set(listtocompare) & set(getTimeGapForDay(self.convertWeekDayToProperArray(i)))))) != 0:
	    	#		totalDays += 1
			#weekTotalTimeGap += getTimeGapForDay(self.convertWeekDayToProperArray(i))
		if len(list(set(listtocompare) & set(self.mondayS))) != 0:
	    		totalDays += 1
		if len(list(set(listtocompare) & set(self.tuesdayS))) != 0:
			totalDays += 1
		if len(list(set(listtocompare) & set(self.wednesdayS))) != 0:
			totalDays += 1
		if len(list(set(listtocompare) & set(self.thursdayS))) != 0:
			totalDays += 1
		if len(list(set(listtocompare) & set(self.fridayS))) != 0:
			totalDays += 1
		if len(list(set(listtocompare) & set(self.saturdayS))) != 0:
			totalDays += 1
		if len(list(set(listtocompare) & set(self.sundayS))) != 0:
			totalDays += 1
		return totalDays
    
	def getTotalCrossCampusTravels(self):
		weekTotalCampusTravels = 0
		for i in range (0, 7):
			weekTotalCampusTravels += getNumberCampusTripsForDay(self.convertWeekDayToProperArray(i))
		return weekTotalCampusTravels

    	def totalPurge(self):
		self.mondayS = [0] * 144
		self.tuesdayS = [0] * 144
		self.wednesdayS = [0] * 144
		self.thursdayS = [0] * 144
		self.fridayS = [0] * 144
		self.saturdayS = [0] * 144
		self.sundayS = [0] * 144
	#needs to be reworked for ... multiple campuses    	
	def clearSchedule(self):
        	for i in range (0, len(self.mondayS)):
          		if self.mondayS[i] in [1, 4, 7, 10]:
                		self.mondayS[i] = 0 
        	for i in range (0, len(self.tuesdayS)):
           		if self.tuesdayS[i] in [1, 4, 7, 10]:
                		self.tuesdayS[i] = 0
		for i in range (0, len(self.wednesdayS)):
		    	if self.wednesdayS[i] in [1, 4, 7, 10]:
		        	self.wednesdayS[i] = 0
		for i in range (0, len(self.thursdayS)):
			if self.thursdayS[i] in [1, 4, 7, 10]:
				self.thursdayS[i] = 0
		for i in range (0, len(self.fridayS)):
		    	if self.fridayS[i] in [1, 4, 7, 10]:
		        	self.fridayS[i] = 0
		for i in range (0, len(self.saturdayS)):
		    	if self.saturdayS[i] in [1, 4, 7, 10]:
		       		self.saturdayS[i] = 0
		for i in range (0, len(self.sundayS)):
			if self.sundayS[i] in [1, 4, 7, 10]:
		       		self.sundayS[i] = 0
                
    #totalPurge and clear schedule should be methods here




#==================================================================================================
#Finds if times will conflict with schedule
#===================================================================================================

# 0=burnaby,1=surrey, 2 = vancouver
# we can place them we just need to solidify what happens after
def checkIfTimeDayConflict(startTime, endTime, timeSlotArray, campus):
	#burnaby	
	if campus == 1:
		#make sure we can set the course
		for i in range (startTime, endTime+1):
        		if timeSlotArray[i] != 0 and timeSlotArray[i] != 3:
            			return True
		#make sure that if we set the course we aren't preventing the student from getting to later classes	
		for i in range (endTime+1, endTime+7):
			if i < 144:
				burnabyListOfPossibleSlots = [0,1,2,3,4,5,12]
				if timeSlotArray[i] not in burnabyListOfPossibleSlots:
		    			return True
		return False	        
	#surrey
	elif campus == 2:
	        for i in range (startTime, endTime+1):
	                if timeSlotArray[i] != 0 and timeSlotArray[i] != 6 :
	                        #here the timeslot can = 0 or ... 4
	                        return True
	        return False
		
		for i in range (endTime+1, endTime+7):
			if i < 144:
				surreyListOfPossibleSlots = [0,1,2,6,7,8, 12]
				if timeSlotArray[i] not in surreyListOfPossibleSlots:
		    			return True
		return False	
	#vancouver
	elif campus == 3:
	        for i in range (startTime, endTime+1):
	                if timeSlotArray[i] != 0 and timeSlotArray[i] != 9 :
	                        return True
	        return False
		
		for i in range (endTime+1, endTime+7):
			if i < 144:
				vancouverListOfPossibleSlots = [0,1,2,9,10,11, 12]
				if timeSlotArray[i] not in vancouverListOfPossibleSlots:
		    			return True
		return False	
	else:
		for i in range (startTime, endTime+1):
			if timeSlotArray[i] != 0:
		    		return True
    		return False
	
	#check ot make sure that we can get to this course...

	#check that we can get from it... i.e. if we have courses afterwards taht we can 



#==================================================================================================
#Find schedule utility functions (let us alter the schedule)
#===================================================================================================


def lockSlotThroughCampus(startTime, endTime, timeSlotArray, campus):
	if campus == 1:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 5
		#cover the hour following this time... for travel reasons
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 0:	
				timeSlotArray[x] = 3
	elif campus == 2:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 8
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 0:	
				timeSlotArray[x] = 6
	elif campus == 3:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 11
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 0:	
				timeSlotArray[x] = 9
	else:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 2

def setSlotThroughCampus(startTime, endTime, timeSlotArray, campus):
    	if campus == 1:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 4
		#cover other parts ... i.e. the hour following this time
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 0:	
				timeSlotArray[x] = 3
	elif campus == 2:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 7
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 0:				
				timeSlotArray[x] = 6
	elif campus == 3:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 10
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 0:	
				timeSlotArray[x] = 9
	else:
		for x in range (startTime, endTime+1):
			timeSlotArray[x] = 1

#unlocks a period of time with campus in mind... the order of it may seem strange at first
def unlockSlotThroughCampus(startTime, endTime, timeSlotArray, campus):
	#present		
	for x in range (startTime, endTime+1):
		timeSlotArray[x] = 0	
	
	if campus == 1:
		#future
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 3:	
				timeSlotArray[x] = 0
	elif campus == 2:
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 6:	
				timeSlotArray[x] = 0
	elif campus == 3:
		for x in range (endTime+1, endTime+7):
			if timeSlotArray[x] == 9:	
				timeSlotArray[x] = 0
	#past				
	for x in range (startTime-6, startTime):
		if timeSlotArray[x] in [4,5]:
			timeSlotArray[x+6] = 3
		elif timeSlotArray[x] in [7,8]:
			timeSlotArray[x+6] = 6
		elif timeSlotArray[x] in [10,11]:
			timeSlotArray[x+6] = 9


def lockSlotThrough(startTime, endTime, timeSlotArray):	
	for x in range (startTime, endTime+1):
		timeSlotArray[x] = 2
def lockSlotThroughUnavailable(startTime, endTime, timeSlotArray):	
	for x in range (startTime, endTime):
		timeSlotArray[x] = 12#12 = unavailable...

def setSlotThrough(startTime, endTime, timeSlotArray):
    	for x in range (startTime, endTime+1):
        	timeSlotArray[x] = 1

def unlockSlotThrough(startTime, endTime, timeSlotArray):
	for x in range (startTime, endTime+1):
		timeSlotArray[x] = 0
        
def freeSlotThrough(startTime, endTime, timeSlotArray):
    	for x in range (startTime, endTime+1):
        	if timeSlotArray[x] != 2:
           		timeSlotArray[x] = 0
        

def checkSlot(slotNumber, timeSlotArray):
	return timeSlotArray[slotNumber]



#==================================================================================================
#Find stats on schedule (such as number of days etc)
#===================================================================================================



#Finds the total amout of gap in the schedule for one timeSlotArray
def getTimeGapForDay(timeSlotArray):
	totalGap = 0
	marker = -1
    	for i in range (0, len(timeSlotArray)):
        	if (marker != -1):
            		if checkSlot(i, timeSlotArray) not in [0, 3, 6, 9]:
                		totalGap += (i-marker-1)
                		marker = i       
        	else :
			if checkSlot(i, timeSlotArray) not in [0, 3, 6, 9]:
                		marker = i
    	return totalGap

#finds the number of campuses we travel to in a day
def getNumberCampusesForDay(timeSlotArray):
	totalCampuses = 0 
	if 4 in timeSlotArray or 5 in timeSlotArray:
		totalCampuses += 1
	if 7 in timeSlotArray or 8 in timeSlotArray:
		totalCampuses += 1
	if 10 in timeSlotArray or 11 in timeSlotArray:
		totalCampuses += 1
	return totalCampuses


def getNumberCampusTripsForDay(timeSlotArray):
	totalCampusTrips = 0 
	burnabyFlag = False #whether or not we are in burnaby
	surreyFlag = False #whether or not we are in surrey
	vancouverFlag = False #whether or not we are in vancouver
	for i in range (0, len(timeSlotArray)):
		if timeSlotArray[i] in [4,5]:
			if burnabyFlag == False:#if we just arrived in buraby
				burnabyFlag = True#let the system know we are in burnaby		
				if surreyFlag == True:
					surreyFlag = False
					totalCampusTrips += 1 # we just travelled from surrey to burnaby
				elif vancouverFlag == True:			
					vancouverFlag = False
					totalCampusTrips += 1 # we just travelled from vancouver to burnaby
		elif timeSlotArray[i] in [7,8]: 
			if surreyFlag == False:#if we just arrived in surrey
				surreyFlag = True#let the system know we are in surrey		
				if burnabyFlag == True:
					burnabyFlag = False
					totalCampusTrips += 1 # we just travelled from  burnaby to surrey
				elif vancouverFlag == True:			
					vancouverFlag = False
					totalCampusTrips += 1 # we just travelled from vancouver to surrey
		elif timeSlotArray[i] in [10,11]:
			if vancouverFlag == False:#if we just arrived in vancouver
				vancouverFlag = True#let the system know we are in surrey		
				if burnabyFlag == True:
					burnabyFlag = False
					totalCampusTrips += 1 # we just travelled from burnaby to vancouver 
				elif surreyFlag == True:			
					surreyFlag = False
					totalCampusTrips += 1 # we just travelled from surrey to vancouver 
	return totalCampusTrips


#Schedule.py



class Schedule:
    mondayTimeSlotAvailability = [0] * 144
    tuesdayTimeSlotAvailability = [0] * 144
    wednesdayTimeSlotAvailability = [0] * 144
    thursdayTimeSlotAvailability = [0] * 144
    fridayTimeSlotAvailability = [0] * 144
    saturdayTimeSlotAvailability = [0] * 144
    sundayTimeSlotAvailability = [0] * 144
    #def getTotalDays(self):

    #see if the timeslice conflicts with the current weekly schedule
    def checkTimeWeekConflict(self, startTime, endTime, weekday):
        if weekday ==0:
            return checkIfTimeDayConflict(startTime, endTime, self.mondayTimeSlotAvailability)
        elif weekday ==1:
            return checkIfTimeDayConflict(startTime, endTime, self.tuesdayTimeSlotAvailability)
        elif weekday ==2:
            return checkIfTimeDayConflict(startTime, endTime, self.wednesdayTimeSlotAvailability)
    
        elif weekday ==3:
            return checkIfTimeDayConflict(startTime, endTime, self.thursdayTimeSlotAvailability)

        elif weekday ==4:
            return checkIfTimeDayConflict(startTime, endTime, self.fridayTimeSlotAvailability)

        elif weekday ==5:
            return checkIfTimeDayConflict(startTime, endTime, self.saturdayTimeSlotAvailability)

        elif weekday ==6:
            return checkIfTimeDayConflict(startTime, endTime, self.sundayTimeSlotAvailability)

    #i.e. input 0 to get monday, 1 to get tuesday... 6 to get sunday
    def convertWeekDayToProperArray(self, weekday):
        if weekday ==0:
            return self.mondayTimeSlotAvailability
        elif weekday ==1:
            return self.tuesdayTimeSlotAvailability
        elif weekday ==2:
            return self.wednesdayTimeSlotAvailability
        elif weekday ==3:
            return self.thursdayTimeSlotAvailability
        elif weekday ==4:
            return self.fridayTimeSlotAvailability
        elif weekday ==5:
           return self.saturdayTimeSlotAvailability
        elif weekday ==6:
           return self.sundayTimeSlotAvailability

    #Locks slots start-->end, on the given workday
    def lockMeetingTime(self, startTime, endTime, weekday):
        lockSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))
    #Frees slots start-->end, on the given workday
    def unlockMeetingTime(self, startTime, endTime, weekday):
        unlockSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))
    #Sets slots start-->end, on the given workday
    def setMeetingTime(self, startTime, endTime, weekday):
        setSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))
    def freeMeetingTime(self, startTime, endTime, weekday):
        freeSlotThrough(startTime, endTime, self.convertWeekDayToProperArray(weekday))

    
    def getTotalTimeGap(self):
        weekTotalTimeGap = 0
        weekTotalTimeGap += getTimeGapForDay(self.mondayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForDay(self.tuesdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForDay(self.thursdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForDay(self.wednesdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForDay(self.fridayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForDay(self.saturdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForDay(self.sundayTimeSlotAvailability)
        return weekTotalTimeGap
    def getTotalDays(self):
        totalDays = 0
        if 1 in self.mondayTimeSlotAvailability or 2 in self.mondayTimeSlotAvailability:
            totalDays += 1
        if 1 in self.tuesdayTimeSlotAvailability or 2 in self.tuesdayTimeSlotAvailability:
            totalDays += 1
        if 1 in self.wednesdayTimeSlotAvailability or 2 in self.wednesdayTimeSlotAvailability:
            totalDays += 1
        if 1 in self.thursdayTimeSlotAvailability or 2 in self.thursdayTimeSlotAvailability:
            totalDays += 1
        if 1 in self.fridayTimeSlotAvailability or 2 in self.fridayTimeSlotAvailability:
            totalDays += 1
        if 1 in self.saturdayTimeSlotAvailability or 2 in self.saturdayTimeSlotAvailability:
            totalDays += 1
        if 1 in self.sundayTimeSlotAvailability or 2 in self.sundayTimeSlotAvailability:
            totalDays += 1
        #print totalDays
        return totalDays
        
    def totalPurge(self):
        self.mondayTimeSlotAvailability = [0] * 144
        self.tuesdayTimeSlotAvailability = [0] * 144
        self.wednesdayTimeSlotAvailability = [0] * 144
        self.thursdayTimeSlotAvailability = [0] * 144
        self.fridayTimeSlotAvailability = [0] * 144
        self.saturdayTimeSlotAvailability = [0] * 144
        self.sundayTimeSlotAvailability = [0] * 144
    def clearSchedule(self):
        for i in range (0, len(self.mondayTimeSlotAvailability)):
            if self.mondayTimeSlotAvailability[i] == 1:
                self.mondayTimeSlotAvailability[i] = 0 
        for i in range (0, len(self.tuesdayTimeSlotAvailability)):
            if self.tuesdayTimeSlotAvailability[i] == 1:
                self.tuesdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.wednesdayTimeSlotAvailability)):
            if self.wednesdayTimeSlotAvailability[i] == 1:
                self.wednesdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.thursdayTimeSlotAvailability)):
            if self.thursdayTimeSlotAvailability[i] == 1:
                self.thursdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.fridayTimeSlotAvailability)):
            if self.fridayTimeSlotAvailability[i] == 1:
                self.fridayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.saturdayTimeSlotAvailability)):
            if self.saturdayTimeSlotAvailability[i] == 1:
                self.saturdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.sundayTimeSlotAvailability)):
            if self.sundayTimeSlotAvailability[i] == 1:
                self.sundayTimeSlotAvailability[i] = 0
                
    #totalPurge and clear schedule should be methods here

def checkIfTimeDayConflict(startTime, endTime, timeSlotArray):
    for i in range (startTime, endTime+1):
        if timeSlotArray[i] != 0:
            return True
    return False

#def checkIfTimeSpaceOpen(startTime, endTime, timeSlotArray):
##     for i in range (startTime, endTime):
 #       if timeSlotArray[i] != 0:
 #           return true
 #   return f


def lockSlotThrough(startTime, endTime, timeSlotArray):
    for x in range (startTime, endTime+1):
        timeSlotArray[x] = 2

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

#Finds the total amout of gap in the schedule for one timeSlotArray
def getTimeGapForDay(timeSlotArray):
    totalGap = 0
    marker = -1
    for i in range (0, len(timeSlotArray)):
        if (marker != -1):
            if checkSlot(i, timeSlotArray) != 0:
                totalGap += (i-marker-1)
                marker = i       
        else :
            if checkSlot(i, timeSlotArray) != 0:
                marker = i
    return totalGap
        


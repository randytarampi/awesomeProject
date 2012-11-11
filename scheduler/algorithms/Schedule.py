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

    def getTotalTimeGap(self):
        weekTotalTimeGap = 0
        weekTotalTimeGap += getTimeGapForSchedule(self.mondayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForSchedule(self.tuesdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForSchedule(self.thursdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForSchedule(self.wednesdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForSchedule(self.fridayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForSchedule(self.saturdayTimeSlotAvailability)
        weekTotalTimeGap += getTimeGapForSchedule(self.sundayTimeSlotAvailability)
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
        for i in range (0, len(self.mondayTimeSlotAvailability):
            if self.mondayTimeSlotAvailability[i] == 1:
                self.mondayTimeSlotAvailability[i] = 0 
        for i in range (0, len(self.tuesdayTimeSlotAvailability):
            if self.tuesdayTimeSlotAvailability[i] == 1:
                self.tuesdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.wednesdayTimeSlotAvailability):
            if self.wednesdayTimeSlotAvailability[i] == 1:
                self.wednesdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.thursdayTimeSlotAvailability):
            if self.thursdayTimeSlotAvailability[i] == 1:
                self.thursdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.fridayTimeSlotAvailability):
            if self.fridayTimeSlotAvailability[i] == 1:
                self.fridayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.saturdayTimeSlotAvailability):
            if self.saturdayTimeSlotAvailability[i] == 1:
                self.saturdayTimeSlotAvailability[i] = 0
        for i in range (0, len(self.sundayTimeSlotAvailability):
            if self.sundayTimeSlotAvailability[i] == 1:
                self.sundayTimeSlotAvailability[i] = 0
                
    #totalPurge and clear schedule should be methods here

def lockSlotThrough(startTime, endTime, timeSlotArray):
    for x in range (startTime, endTime):
        timeSlotArray[x] = 2

def setSlotThrough(startTime, endTime, timeSlotArray):
    for x in range (startTime, endTime):
        timeSlotArray[x] = 1

def freeSlotThrough(startTime, endTime, timeSlotArray):
    for x in range (startTime, endTime):
        timeSlotArray[x] = 0

def checkSlot(slotNumber, timeSlotArray):
    return timeSlotArray[slotNumber]

#Finds the total amout of gap in the schedule for one timeSlotArray
def getTimeGapForSchedule(timeSlotArray):
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
        
#def freeSlotThrough(startTime, endTime, timeSlotArray):
#    for x in range (startTime, endTime):
#        timeSlotArray[x] = 0

#def 

# get total gap



#This is just a python file with some useful functions that allow us to convert and parse strings 
# that we get from the datebase into useful information

from datetime import datetime

b = "2012-10-12"

#function1()
if 1 > 2:
        print 'True'
if 1 < 2:
        print 'True'

#later dates are greater than earlier dates
# more recent dates > older dates
def comparedate(date1, date2): 
    if date1 > date2:
        print 'Date 1 is more recent'

#Ensures properinputs
def ensuresproperinputs(startdate1, enddate1):
    if startdate1 <= enddate1:
        print 'True'
    else:
        print 'False'

def convertStringToDate(inputString):
    outputdate = datetime.strptime(inputString, '%Y-%m-%d')
    #print outputdate
    return outputdate

def convertStringToTime(inputString):
    outputdate = datetime.strptime(inputString, '%H:%M:%S')
    #print outputdate
    return outputdate


#Tests two sets of start and end dates to see if they overlap and conflict
# This can work for time and for dates
def datetimeconflict(startdate1, enddate1, startdate2, enddate2):
    if startdate1 <= enddate1 and startdate2 <= enddate2:
        if startdate1 < startdate2:
            if enddate1 < startdate2:
                print 'No Conflict first dates happen before second dates'
            else :
                print 'There is a conflict'
        else:
            if enddate2 < startdate1:
                print 'No Conflict dates 2 happen first'
            else:
                print 'There is a conflict'
    else:
         print 'Improper inputs'



#This checks for conflicts in the schedule in terms of dates
def dayconflict(day1, day2):
    if int(day1) == int(day2):
        print 'We have a day conflict'
    else:
        print 'We do not have a day conflict'

#first check dates,....... then day, then time"
# i.e.
    #if date conflict:
        #check for day conflict
        #if time conflict
            #then we have an actual conflict
    # else ... then we do not have a conflict
#I still need to factor in the travel time in between campuses
#I also need to factor in the time to get between classes

def sameCampusTravelConflict(time1, time2):
    if (time1-time2).seconds <= 600 or (time2-time1).seconds <= 600:
        return True
    else:
        return False

def DifferentCampusTravelConflict(time1, time2):
    if (time1-time2).seconds <= 3600 or (time2-time1).seconds <= 3600:
        return True
    else:
        return False
#(time2-time1).seconds = 600
#(time2-time1).seconds = 3600

#
def timeConflict(starttime1, endtime1, starttime2, endtime2):
    if starttime1 <= endtime1 and starttime2 <= endtime2:
        if starttime1 < starttime2:
            if endtime1 < starttime2:
                print 'No Conflict first time happens before second dates'
                if (starttime2-endtime1).seconds < 3600:
                    print 'We can not travel between campuses'
            else :
                print 'There is a conflict'
        else:
            if endtime2 < starttime1:
                print 'No Conflict time 2 happens before time 1'
                if (endtime2-starttime1).seconds < 3600:
                    print 'We can not travel between campuses'
            else:
                print 'There is a conflict'
    else:
         print 'Improper inputs'

